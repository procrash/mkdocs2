"""Skeleton suggestions screen - LLM proposes additional doc sections, user selects."""
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
    Label,
    LoadingIndicator,
    Static,
)

from ...config.schema import AppConfig, SkeletonSuggestionEntry
from ...orchestrator.opencode_runner import configure_http_fallback, run_opencode

SUGGESTION_PROMPT = """Du bist ein Dokumentationsexperte. Analysiere das folgende Projektverzeichnis und schlage zusätzliche sinnvolle Dokumentationsabschnitte vor, die in ein MkDocs-Skelett aufgenommen werden sollten.

Projektname: {project_name}
Sprachen: {languages}
Quellverzeichnis: {source_dir}

Gefundene Dateien (Auszug):
{file_listing}

Antworte AUSSCHLIESSLICH im folgenden Format (eine Zeile pro Vorschlag):
PATH|TITLE|DESCRIPTION

Beispiel:
getting-started/docker.md|Docker-Setup|Anleitung zur Nutzung mit Docker
generated/developer/testing.md|Test-Guide|Überblick über die Teststrategie
architecture/security.md|Sicherheitskonzept|Sicherheitsarchitektur und Maßnahmen

Schlage 5-15 sinnvolle, projektspezifische Abschnitte vor. Keine generischen Platzhalter."""


class SkeletonSuggestionsScreen(Screen):
    """LLM suggests additional skeleton sections, user selects which to include."""

    CSS = """
    SkeletonSuggestionsScreen {
        align: center middle;
    }
    #suggestions-box {
        width: 90;
        height: auto;
        max-height: 85%;
        border: solid $primary;
        padding: 1 2;
        overflow-y: auto;
    }
    .suggestion-item {
        height: auto;
        padding: 0 1;
        margin-bottom: 0;
    }
    .suggestion-desc {
        margin-left: 4;
        color: $text-muted;
    }
    #btn-row {
        margin-top: 1;
        align: center middle;
        height: 5;
    }
    #btn-row Button {
        margin: 0 2;
    }
    """

    BINDINGS = [
        ("escape", "go_back", "Zurück"),
        ("a", "select_all", "Alle auswählen"),
        ("n", "select_none", "Keine auswählen"),
    ]

    def __init__(self, config: AppConfig, file_listing: str = "", model_ids: list[str] | None = None):
        super().__init__()
        self.config = config
        self.file_listing = file_listing
        self.model_ids = model_ids or []
        self._suggestions: list[SkeletonSuggestionEntry] = []
        self._loaded = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        # Use previously stored suggestions if available
        prev_suggestions = self.config.preferences.skeleton_suggestions

        with Center():
            with Vertical(id="suggestions-box"):
                yield Label("[bold]Skelett-Vorschläge vom LLM[/bold]")
                yield Label(
                    "Das Sprachmodell analysiert dein Projekt und schlägt\n"
                    "zusätzliche Dokumentationsabschnitte vor.",
                )
                yield LoadingIndicator(id="spinner")
                yield Vertical(id="suggestions-list")
                with Horizontal(id="btn-row"):
                    yield Button("← Zurück", variant="default", id="btn-back")
                    yield Button("Ausgewählte übernehmen & Weiter →", variant="primary", id="btn-next", disabled=True)
        yield Footer()

    def on_mount(self) -> None:
        prev = self.config.preferences.skeleton_suggestions
        if prev and self.config.resume.suggestions_fetched:
            # Re-use previous suggestions
            self._suggestions = list(prev)
            self._render_suggestions()
            self.query_one("#spinner", LoadingIndicator).display = False
            self.query_one("#btn-next", Button).disabled = False
            self._loaded = True
        else:
            self.run_worker(self._fetch_suggestions(), exclusive=True)

    async def _fetch_suggestions(self) -> None:
        spinner = self.query_one("#spinner", LoadingIndicator)

        configure_http_fallback(
            server_url=self.config.server.url,
            api_key=self.config.server.api_key,
            timeout_read=self.config.server.timeout_read,
        )

        # Pick first available model for suggestions
        model_id = self.model_ids[0] if self.model_ids else "mock-model"
        mock_mode = self.config.system.mock_mode or not self.model_ids

        prompt = SUGGESTION_PROMPT.format(
            project_name=self.config.project.name,
            languages=", ".join(self.config.project.languages),
            source_dir=str(self.config.project.source_dir),
            file_listing=self.file_listing[:3000],
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
            self._suggestions = _parse_suggestions(result.output)
        else:
            self._suggestions = _default_suggestions()

        self.config.resume.suggestions_fetched = True
        spinner.display = False
        self._render_suggestions()
        self.query_one("#btn-next", Button).disabled = False
        self._loaded = True

    def _render_suggestions(self) -> None:
        container = self.query_one("#suggestions-list", Vertical)
        container.remove_children()

        for i, s in enumerate(self._suggestions):
            cb = Checkbox(
                f"{s.title}  [dim]{s.path}[/dim]",
                value=s.accepted,
                id=f"sugg-{i}",
                classes="suggestion-item",
            )
            container.mount(cb)
            desc = Label(f"  {s.description}", classes="suggestion-desc")
            container.mount(desc)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-back":
            self.dismiss(None)
            return
        if event.button.id == "btn-next":
            # Collect selections
            for i, s in enumerate(self._suggestions):
                try:
                    cb = self.query_one(f"#sugg-{i}", Checkbox)
                    s.accepted = cb.value
                except Exception:
                    pass

            # Persist
            self.config.preferences.skeleton_suggestions = self._suggestions
            self.dismiss({"suggestions": self._suggestions})

    def action_go_back(self) -> None:
        self.dismiss(None)

    def action_select_all(self) -> None:
        if not self._loaded:
            return
        for i in range(len(self._suggestions)):
            try:
                self.query_one(f"#sugg-{i}", Checkbox).value = True
            except Exception:
                pass

    def action_select_none(self) -> None:
        if not self._loaded:
            return
        for i in range(len(self._suggestions)):
            try:
                self.query_one(f"#sugg-{i}", Checkbox).value = False
            except Exception:
                pass


def _parse_suggestions(output: str) -> list[SkeletonSuggestionEntry]:
    """Parse LLM output into suggestion entries."""
    suggestions: list[SkeletonSuggestionEntry] = []
    for line in output.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "|" not in line:
            continue
        parts = line.split("|", 2)
        if len(parts) < 2:
            continue
        path = parts[0].strip()
        title = parts[1].strip()
        desc = parts[2].strip() if len(parts) > 2 else ""
        if path and title:
            suggestions.append(SkeletonSuggestionEntry(
                path=path, title=title, description=desc, accepted=True,
            ))
    return suggestions


def _default_suggestions() -> list[SkeletonSuggestionEntry]:
    """Fallback suggestions when LLM is unavailable."""
    return [
        SkeletonSuggestionEntry(path="getting-started/configuration.md", title="Konfiguration", description="Konfigurationsoptionen und Einstellungen", accepted=True),
        SkeletonSuggestionEntry(path="getting-started/docker.md", title="Docker-Setup", description="Nutzung mit Docker und Docker Compose", accepted=True),
        SkeletonSuggestionEntry(path="architecture/design-decisions.md", title="Design-Entscheidungen", description="Architektur-Entscheidungen und Begründungen", accepted=True),
        SkeletonSuggestionEntry(path="generated/developer/testing.md", title="Test-Guide", description="Überblick über Teststrategie und Testausführung", accepted=False),
        SkeletonSuggestionEntry(path="manual/troubleshooting.md", title="Fehlerbehebung", description="Häufige Probleme und Lösungen", accepted=True),
    ]
