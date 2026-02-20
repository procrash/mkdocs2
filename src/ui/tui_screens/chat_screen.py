"""Chat screen - ask questions about the project or implement changes.

Supports:
- Read-only mode (analysis, explanations, no file changes)
- Implementation mode: Slave LLMs produce proposals, Master evaluates & synthesizes,
  user reviews diff and approves/rejects each file change
- Multiple LLMs individually selectable
- Master LLM selectable
"""
from __future__ import annotations
import asyncio
import logging
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import (
    Button,
    Checkbox,
    Footer,
    Header,
    Input,
    Label,
    Log,
    Select,
    Static,
)

from ...config.schema import AppConfig
from ...orchestrator.opencode_runner import configure_http_fallback, run_opencode
from .diff_review_screen import DiffReviewScreen, FileChange, parse_file_changes

logger = logging.getLogger(__name__)


EVALUATE_PROMPT = """Du bist ein Master-Evaluator. Mehrere Sprachmodelle haben folgende Frage beantwortet:

FRAGE: {question}

Hier sind die Antworten:

{answers}

Bewerte die Antworten und erstelle eine optimale Synthese. Markiere die beste Antwort und ergänze fehlende Punkte aus den anderen. Antworte auf Deutsch."""


IMPLEMENT_SLAVE_PROMPT = """Du bist ein erfahrener Software-Entwickler. Du arbeitest am Projekt '{project_name}'.
Projektverzeichnis: {source_dir}
Sprachen: {languages}

Aufgabe: {question}

{file_context}

Erstelle konkreten, funktionierenden Code. Gib deine Antwort in folgendem Format:

Für JEDE Datei die du änderst oder erstellst:

<<<FILE pfad/zur/datei.py
DESCRIPTION: Kurze Beschreibung was diese Änderung tut
>>>
Hier der vollständige neue Dateiinhalt
<<<END>>>

WICHTIG:
- Gib den KOMPLETTEN Dateiinhalt an, nicht nur die Änderungen
- Pfade sind relativ zum Projektverzeichnis {source_dir}
- Nur Dateien angeben die tatsächlich geändert werden müssen
- Code muss korrekt und lauffähig sein"""


IMPLEMENT_MASTER_PROMPT = """Du bist ein Master-Architekt und Code-Reviewer. Mehrere Entwickler-LLMs haben Implementierungsvorschläge für folgende Aufgabe erstellt:

AUFGABE: {question}

Projekt: {project_name}
Verzeichnis: {source_dir}

Hier sind die Vorschläge:

{proposals}

Deine Aufgabe:
1. Bewerte jeden Vorschlag auf Korrektheit, Vollständigkeit und Code-Qualität
2. Erstelle die BESTE Implementierung, indem du die besten Teile kombinierst
3. Korrigiere Fehler die du in den Vorschlägen findest

Gib deine finale Implementierung in folgendem Format:

Für JEDE Datei:

<<<FILE pfad/zur/datei.py
DESCRIPTION: Was diese Datei tut / was geändert wurde
>>>
Vollständiger Dateiinhalt hier
<<<END>>>

WICHTIG: Gib NUR die <<<FILE ... <<<END>>> Blöcke aus, keine weiteren Erklärungen davor oder danach."""


class ChatScreen(Screen):
    """Interactive chat: read-only analysis or full implementation with multi-LLM."""

    CSS = """
    ChatScreen {
        layout: grid;
        grid-size: 1 4;
        grid-rows: auto 1fr auto 3;
    }
    #chat-config {
        height: auto;
        max-height: 12;
        padding: 0 2;
        border-bottom: solid $primary;
    }
    #chat-log {
        border: solid $primary;
        height: 100%;
    }
    #input-row {
        height: auto;
        padding: 1 2;
    }
    #chat-input {
        width: 1fr;
    }
    .model-check {
        height: 2;
    }
    #mode-label {
        margin: 0 2;
    }
    #mode-info {
        color: $text-muted;
        margin-top: 0;
    }
    """

    BINDINGS = [
        ("escape", "go_back", "Zurück"),
        ("ctrl+l", "clear_log", "Log löschen"),
    ]

    def __init__(self, config: AppConfig, available_models: list[str]):
        super().__init__()
        self.config = config
        self.available_models = available_models
        self._read_only = True
        self._applied_changes: list[FileChange] = []

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Vertical(id="chat-config"):
            yield Label("[bold]Projekt-Chat[/bold] - Fragen stellen & Implementieren")
            with Horizontal():
                yield Checkbox("Read-Only Modus", value=True, id="readonly-check")
                yield Label("  |  Master-LLM: ", id="mode-label")
                if self.available_models:
                    options = [(m, m) for m in self.available_models]
                    yield Select(options, value=self.available_models[0], id="master-select")
            yield Label(
                "[dim]Read-Only: Nur Analyse. | Impl.: Slaves schreiben Code → Master bewertet → Du bestätigst Diff[/dim]",
                id="mode-info",
            )
            with Horizontal():
                yield Label("Slave-LLMs: ")
            with Horizontal():
                for m in self.available_models:
                    yield Checkbox(m, value=True, id=f"chat-model-{m}", classes="model-check")

        yield Log(id="chat-log", highlight=True)

        with Horizontal(id="input-row"):
            yield Input(placeholder="Frage oder Implementierungsauftrag eingeben...", id="chat-input")
            yield Button("Senden", variant="primary", id="btn-send")
            yield Button("Zurück", variant="default", id="btn-back")

        yield Footer()

    def on_mount(self) -> None:
        log = self.query_one("#chat-log", Log)
        log.write_line("[bold]Projekt-Chat[/bold]")
        log.write_line("")
        log.write_line("[cyan]Read-Only Modus:[/cyan] Fragen zum Projekt stellen, Code erklären lassen.")
        log.write_line("[cyan]Implementierungs-Modus:[/cyan] (Read-Only deaktivieren)")
        log.write_line("  1. Slave-LLMs erstellen Implementierungsvorschläge")
        log.write_line("  2. Master-LLM bewertet und erstellt beste Synthese")
        log.write_line("  3. Du siehst einen Diff und wählst welche Dateien geändert werden")
        log.write_line("")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-send":
            self._send_question()
        elif event.button.id == "btn-back":
            self.dismiss({"applied_changes": self._applied_changes})

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "chat-input":
            self._send_question()

    def _send_question(self) -> None:
        inp = self.query_one("#chat-input", Input)
        question = inp.value.strip()
        if not question:
            return
        inp.value = ""

        self._read_only = self.query_one("#readonly-check", Checkbox).value

        # Collect selected slave models
        selected_models: list[str] = []
        for m in self.available_models:
            try:
                cb = self.query_one(f"#chat-model-{m}", Checkbox)
                if cb.value:
                    selected_models.append(m)
            except Exception:
                pass

        # Get master model
        master_model = ""
        try:
            master_select = self.query_one("#master-select", Select)
            if master_select.value and master_select.value != Select.BLANK:
                master_model = str(master_select.value)
        except Exception:
            if selected_models:
                master_model = selected_models[0]

        if not selected_models:
            log = self.query_one("#chat-log", Log)
            log.write_line("[red]Kein Modell ausgewählt![/red]")
            return

        log = self.query_one("#chat-log", Log)
        mode = "[Read-Only]" if self._read_only else "[Implementierung]"
        log.write_line(f"\n[bold cyan]Du {mode}:[/bold cyan] {question}")

        if self._read_only:
            self.run_worker(
                self._query_readonly(question, selected_models, master_model),
                exclusive=True,
            )
        else:
            self.run_worker(
                self._query_implement(question, selected_models, master_model),
                exclusive=True,
            )

    # ── Read-Only Mode ────────────────────────────────────────────

    async def _query_readonly(
        self,
        question: str,
        selected_models: list[str],
        master_model: str,
    ) -> None:
        log = self.query_one("#chat-log", Log)

        configure_http_fallback(
            server_url=self.config.server.url,
            api_key=self.config.server.api_key,
            timeout_read=self.config.server.timeout_read,
        )

        prompt = (
            f"Du analysierst ein Softwareprojekt namens '{self.config.project.name}'.\n"
            f"Projektverzeichnis: {self.config.project.source_dir}\n"
            f"Sprachen: {', '.join(self.config.project.languages)}\n"
            f"Antworte nur mit Analyse und Erklärungen, schlage KEINE Code-Änderungen vor.\n\n"
            f"Frage: {question}"
        )

        mock_mode = self.config.system.mock_mode
        answers: dict[str, str] = {}

        for model_id in selected_models:
            log.write_line(f"[dim]  Frage {model_id}...[/dim]")
            result = await run_opencode(
                prompt=prompt,
                model_id=model_id,
                timeout=self.config.system.global_timeout_seconds,
                max_retries=2,
                retry_delay=2,
                mock_mode=mock_mode,
            )
            if result.success and result.output.strip():
                answers[model_id] = result.output.strip()
                log.write_line(f"[green]  {model_id} hat geantwortet[/green]")
            else:
                log.write_line(f"[red]  {model_id} Fehler: {result.error}[/red]")

        if not answers:
            log.write_line("[red]Keine Antworten erhalten.[/red]")
            return

        # Single model or no master: show directly
        if len(answers) == 1 or not master_model:
            for model_id, answer in answers.items():
                log.write_line(f"\n[bold yellow]{model_id}:[/bold yellow]")
                for line in answer.splitlines():
                    log.write_line(f"  {line}")
            return

        # Multiple: master evaluates
        log.write_line(f"\n[dim]  Master ({master_model}) bewertet...[/dim]")
        answers_text = ""
        for i, (model_id, answer) in enumerate(answers.items(), 1):
            answers_text += f"\n--- Modell {i} ({model_id}) ---\n{answer}\n"

        eval_result = await run_opencode(
            prompt=EVALUATE_PROMPT.format(question=question, answers=answers_text),
            model_id=master_model,
            timeout=self.config.system.global_timeout_seconds,
            max_retries=2,
            retry_delay=2,
            mock_mode=mock_mode,
        )

        if eval_result.success and eval_result.output.strip():
            log.write_line(f"\n[bold green]Master-Bewertung ({master_model}):[/bold green]")
            for line in eval_result.output.strip().splitlines():
                log.write_line(f"  {line}")
        else:
            log.write_line(f"\n[yellow]Master fehlgeschlagen, zeige Einzelantworten:[/yellow]")
            for model_id, answer in answers.items():
                log.write_line(f"\n[bold yellow]{model_id}:[/bold yellow]")
                for line in answer.splitlines():
                    log.write_line(f"  {line}")

    # ── Implementation Mode ───────────────────────────────────────

    async def _query_implement(
        self,
        question: str,
        selected_models: list[str],
        master_model: str,
    ) -> None:
        """Full implementation workflow: slaves propose → master synthesizes → user reviews diff."""
        log = self.query_one("#chat-log", Log)

        configure_http_fallback(
            server_url=self.config.server.url,
            api_key=self.config.server.api_key,
            timeout_read=self.config.server.timeout_read,
        )

        source_dir = str(self.config.project.source_dir)
        mock_mode = self.config.system.mock_mode

        # Step 1: Read relevant file context
        file_context = await self._gather_file_context(question)

        log.write_line(f"\n[bold]Phase 1:[/bold] Slave-LLMs erstellen Implementierungsvorschläge...")

        # Step 2: Query all slave models
        proposals: dict[str, str] = {}
        for model_id in selected_models:
            log.write_line(f"[dim]  Slave {model_id} arbeitet...[/dim]")

            prompt = IMPLEMENT_SLAVE_PROMPT.format(
                project_name=self.config.project.name,
                source_dir=source_dir,
                languages=", ".join(self.config.project.languages),
                question=question,
                file_context=file_context,
            )

            result = await run_opencode(
                prompt=prompt,
                model_id=model_id,
                timeout=self.config.system.global_timeout_seconds,
                max_retries=2,
                retry_delay=2,
                mock_mode=mock_mode,
            )

            if result.success and result.output.strip():
                proposals[model_id] = result.output.strip()
                # Count proposed files
                changes = parse_file_changes(result.output, base_dir=source_dir)
                log.write_line(
                    f"[green]  {model_id}: {len(changes)} Dateiänderungen vorgeschlagen[/green]"
                )
            else:
                log.write_line(f"[red]  {model_id} Fehler: {result.error}[/red]")

        if not proposals:
            log.write_line("[red]Keine Implementierungsvorschläge erhalten.[/red]")
            return

        # Step 3: Master evaluates and creates final implementation
        if len(proposals) > 1 and master_model:
            log.write_line(f"\n[bold]Phase 2:[/bold] Master ({master_model}) bewertet und erstellt finale Implementierung...")

            proposals_text = ""
            for i, (model_id, proposal) in enumerate(proposals.items(), 1):
                proposals_text += f"\n=== Vorschlag {i} von {model_id} ===\n{proposal}\n"

            master_prompt = IMPLEMENT_MASTER_PROMPT.format(
                question=question,
                project_name=self.config.project.name,
                source_dir=source_dir,
                proposals=proposals_text,
            )

            master_result = await run_opencode(
                prompt=master_prompt,
                model_id=master_model,
                timeout=self.config.system.global_timeout_seconds,
                max_retries=2,
                retry_delay=2,
                mock_mode=mock_mode,
            )

            if master_result.success and master_result.output.strip():
                final_output = master_result.output.strip()
                log.write_line(f"[green]  Master hat finale Implementierung erstellt[/green]")
            else:
                # Fallback to best slave proposal (longest)
                log.write_line(f"[yellow]  Master fehlgeschlagen, verwende besten Slave-Vorschlag[/yellow]")
                final_output = max(proposals.values(), key=len)
        else:
            # Single model: use directly
            final_output = list(proposals.values())[0]

        # Step 4: Parse file changes
        changes = parse_file_changes(final_output, base_dir=source_dir)

        if not changes:
            log.write_line("\n[yellow]Keine strukturierten Dateiänderungen erkannt.[/yellow]")
            log.write_line("[dim]Antwort des LLMs:[/dim]")
            for line in final_output.splitlines()[:40]:
                log.write_line(f"  {line}")
            return

        log.write_line(f"\n[bold]Phase 3:[/bold] {len(changes)} Dateiänderungen zur Überprüfung...")
        for c in changes:
            action = "NEU" if c.is_new_file else "ÄNDERN"
            log.write_line(f"  [{action}] {c.file_path}")
            if c.description:
                log.write_line(f"        {c.description}")

        # Step 5: Show diff review modal
        log.write_line("\n[bold cyan]Öffne Diff-Vorschau...[/bold cyan]")

        def on_review_result(result: dict | None):
            if result and result.get("applied", 0) > 0:
                self._applied_changes.extend(
                    c for c in result.get("changes", []) if c.accepted
                )
                log.write_line(
                    f"\n[bold green]{result['applied']} Dateien erfolgreich geändert![/bold green]"
                )
                if result.get("failed", 0):
                    log.write_line(f"[red]{result['failed']} Dateien fehlgeschlagen[/red]")
            else:
                log.write_line("\n[yellow]Keine Änderungen angewendet.[/yellow]")

        self.app.push_screen(DiffReviewScreen(changes), callback=on_review_result)

    async def _gather_file_context(self, question: str) -> str:
        """Read relevant source files for context based on the question."""
        source_dir = Path(str(self.config.project.source_dir))
        if not source_dir.exists():
            return "(Quellverzeichnis nicht erreichbar)"

        context_parts: list[str] = []
        max_context_chars = 8000

        # Heuristic: include a listing + a few key files
        try:
            from ...analyzer.scanner import scan_directory
            scan = scan_directory(
                source_dir,
                self.config.project.languages,
                self.config.project.ignore_patterns,
            )

            # File listing
            file_list = "\n".join(str(f.relative_path) for f in scan.files[:30])
            context_parts.append(f"Projektdateien:\n{file_list}")

            # Try to find files mentioned in the question
            question_lower = question.lower()
            relevant_files = [
                f for f in scan.files
                if any(
                    keyword in str(f.relative_path).lower()
                    for keyword in question_lower.split()
                    if len(keyword) > 3
                )
            ][:5]

            for sf in relevant_files:
                try:
                    content = sf.path.read_text(encoding="utf-8", errors="replace")
                    if len(content) > 2000:
                        content = content[:2000] + "\n... (gekürzt)"
                    context_parts.append(f"\n--- {sf.relative_path} ---\n{content}")
                except Exception:
                    pass

        except Exception as exc:
            context_parts.append(f"(Fehler beim Lesen: {exc})")

        full_context = "\n".join(context_parts)
        if len(full_context) > max_context_chars:
            full_context = full_context[:max_context_chars] + "\n... (Kontext gekürzt)"

        return full_context

    def action_go_back(self) -> None:
        self.dismiss({"applied_changes": self._applied_changes})

    def action_clear_log(self) -> None:
        log = self.query_one("#chat-log", Log)
        log.clear()
