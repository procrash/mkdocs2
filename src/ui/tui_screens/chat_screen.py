"""Chat screen - ask questions about the project or get implementation suggestions.

Supports read-only mode and multi-model querying with a master LLM evaluator.
"""
from __future__ import annotations
import asyncio

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
    RadioButton,
    RadioSet,
    Select,
    Static,
)

from ...config.schema import AppConfig
from ...orchestrator.opencode_runner import configure_http_fallback, run_opencode


EVALUATE_PROMPT = """Du bist ein Master-Evaluator. Mehrere Sprachmodelle haben folgende Frage beantwortet:

FRAGE: {question}

Hier sind die Antworten:

{answers}

Bewerte die Antworten und erstelle eine optimale Synthese. Markiere die beste Antwort und ergänze fehlende Punkte aus den anderen. Antworte auf Deutsch."""


class ChatScreen(Screen):
    """Interactive chat for project questions and implementation suggestions.

    Features:
    - Read-only mode (no code changes)
    - Multiple LLMs answerable individually
    - Master LLM evaluates and synthesizes answers
    - All models selectable by user
    """

    CSS = """
    ChatScreen {
        layout: grid;
        grid-size: 1 4;
        grid-rows: auto 1fr auto 3;
    }
    #chat-config {
        height: auto;
        max-height: 10;
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

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Vertical(id="chat-config"):
            yield Label("[bold]Projekt-Chat[/bold] - Fragen stellen & Implementierungsvorschläge")
            with Horizontal():
                yield Checkbox("Read-Only Modus", value=True, id="readonly-check")
                yield Label("  |  Master-LLM: ", id="mode-label")
                if self.available_models:
                    options = [(m, m) for m in self.available_models]
                    yield Select(options, value=self.available_models[0], id="master-select")
            with Horizontal():
                yield Label("Modelle für Antworten: ")
            with Horizontal():
                for m in self.available_models:
                    yield Checkbox(m, value=True, id=f"chat-model-{m}", classes="model-check")

        yield Log(id="chat-log", highlight=True)

        with Horizontal(id="input-row"):
            yield Input(placeholder="Frage eingeben...", id="chat-input")
            yield Button("Senden", variant="primary", id="btn-send")
            yield Button("Zurück", variant="default", id="btn-back")

        yield Footer()

    def on_mount(self) -> None:
        log = self.query_one("#chat-log", Log)
        log.write_line("[bold]Willkommen im Projekt-Chat![/bold]")
        log.write_line("Stelle Fragen zum Projekt oder frage nach Implementierungsvorschlägen.")
        log.write_line("Im Read-Only Modus werden keine Änderungen am Code vorgenommen.")
        log.write_line("")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-send":
            self._send_question()
        elif event.button.id == "btn-back":
            self.dismiss(None)

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

        # Collect selected models
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

        self.run_worker(
            self._query_models(question, selected_models, master_model),
            exclusive=True,
        )

    async def _query_models(
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

        mode_hint = (
            "Antworte nur mit Analyse und Erklärungen, schlage KEINE Code-Änderungen vor."
            if self._read_only
            else "Du darfst Implementierungsvorschläge mit konkretem Code machen."
        )

        prompt_prefix = (
            f"Du analysierst ein Softwareprojekt namens '{self.config.project.name}'.\n"
            f"Projektverzeichnis: {self.config.project.source_dir}\n"
            f"Sprachen: {', '.join(self.config.project.languages)}\n"
            f"{mode_hint}\n\n"
            f"Frage: {question}"
        )

        mock_mode = self.config.system.mock_mode

        # Query all selected models
        answers: dict[str, str] = {}
        for model_id in selected_models:
            log.write_line(f"[dim]  Frage {model_id}...[/dim]")
            result = await run_opencode(
                prompt=prompt_prefix,
                model_id=model_id,
                timeout=self.config.system.global_timeout_seconds,
                max_retries=2,
                retry_delay=2,
                mock_mode=mock_mode,
            )
            if result.success and result.output.strip():
                answers[model_id] = result.output.strip()
                log.write_line(f"[green]  {model_id} hat geantwortet ({len(result.output)} Zeichen)[/green]")
            else:
                log.write_line(f"[red]  {model_id} Fehler: {result.error}[/red]")

        if not answers:
            log.write_line("[red]Keine Antworten erhalten.[/red]")
            return

        # If only one model or no master, show directly
        if len(answers) == 1 or not master_model:
            for model_id, answer in answers.items():
                log.write_line(f"\n[bold yellow]{model_id}:[/bold yellow]")
                for line in answer.splitlines():
                    log.write_line(f"  {line}")
            return

        # Multiple answers: let master evaluate
        log.write_line(f"\n[dim]  Master-LLM ({master_model}) bewertet Antworten...[/dim]")

        answers_text = ""
        for i, (model_id, answer) in enumerate(answers.items(), 1):
            answers_text += f"\n--- Modell {i} ({model_id}) ---\n{answer}\n"

        eval_prompt = EVALUATE_PROMPT.format(
            question=question,
            answers=answers_text,
        )

        eval_result = await run_opencode(
            prompt=eval_prompt,
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
            # Fallback: show individual answers
            log.write_line(f"\n[yellow]Master-Bewertung fehlgeschlagen, zeige Einzelantworten:[/yellow]")
            for model_id, answer in answers.items():
                log.write_line(f"\n[bold yellow]{model_id}:[/bold yellow]")
                for line in answer.splitlines():
                    log.write_line(f"  {line}")

    def action_go_back(self) -> None:
        self.dismiss(None)

    def action_clear_log(self) -> None:
        log = self.query_one("#chat-log", Log)
        log.clear()
