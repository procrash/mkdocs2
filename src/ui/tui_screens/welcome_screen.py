"""Welcome screen - project info, action selection and automation mode."""
from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Checkbox, Footer, Header, Label, RadioButton, RadioSet, Static

from ...config.schema import AppConfig


# All available actions, matching CLI commands
ACTIONS = [
    ("run", "Voller Workflow", "Server-Erkennung → Modellauswahl → Skelett → Generierung → Chat"),
    ("discover", "Server-Erkennung", "Modelle erkennen und Rollen zuweisen"),
    ("generate", "Generierung", "Dokumentation aus Quellcode generieren"),
    ("init", "Skeleton erstellen", "Dokumentations-Skelett mit Inhaltsrichtlinien aufbauen"),
    ("enhance", "Enhance", "MkDocs-Plugins, Extensions und Skeleton-Inhalte erweitern"),
    ("enhance_llm", "KI-Verbesserung", "Alle Modelle analysieren mkdocs.yml und schlagen Verbesserungen vor"),
    ("restructure", "Restrukturierung", "Dokumentationsstruktur analysieren und Verbesserungen vorschlagen"),
    ("serve", "Dokumentation anzeigen", "MkDocs-Server starten und Dokumentation im Browser öffnen"),
    ("report", "Bericht anzeigen", "Letzten Generierungsbericht anzeigen"),
]


class WelcomeScreen(Screen):
    """First screen: project overview, action selection, and automation question."""

    CSS = """
    WelcomeScreen {
        align: center middle;
    }
    #welcome-box {
        width: 90;
        height: auto;
        max-height: 90%;
        border: solid $primary;
        padding: 1 2;
        overflow-y: auto;
    }
    #project-info {
        margin-bottom: 1;
    }
    #action-section {
        margin-top: 1;
        padding: 1;
        border: dashed $accent;
    }
    #automation-section {
        margin-top: 1;
        padding: 1;
        border: dashed $accent;
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
        ("escape", "quit", "Beenden"),
    ]

    def __init__(self, config: AppConfig):
        super().__init__()
        self.config = config

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Center():
            with Vertical(id="welcome-box"):
                yield Label(
                    f"[bold blue]mkdocsOnSteroids[/bold blue]\n\n"
                    f"Projekt: [bold]{self.config.project.name}[/bold]\n"
                    f"Quellverzeichnis: {self.config.project.source_dir}\n"
                    f"Ausgabe: {self.config.project.output_dir}",
                    id="project-info",
                )
                with Vertical(id="action-section"):
                    yield Label("[bold]Aktion wählen[/bold]")
                    action_set = RadioSet(id="action-radio")
                    with action_set:
                        for i, (key, label, desc) in enumerate(ACTIONS):
                            yield RadioButton(
                                f"{label} — [dim]{desc}[/dim]",
                                value=(i == 0),
                            )
                with Vertical(id="automation-section"):
                    yield Label("[bold]Modus[/bold]")
                    yield RadioSet(
                        RadioButton("Manuell (alle Schritte bestätigen)", value=not self.config.automation.enabled),
                        RadioButton("Automatisch (durchlaufen ohne Rückfragen)", value=self.config.automation.enabled),
                        id="automation-radio",
                    )
                    yield Checkbox(
                        "Auswahl für nächsten Start merken",
                        value=True,
                        id="remember-check",
                    )
                with Horizontal(id="btn-row"):
                    yield Button("Beenden", variant="default", id="btn-quit")
                    yield Button("Starten →", variant="primary", id="btn-next")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            action_radio = self.query_one("#action-radio", RadioSet)
            automation_radio = self.query_one("#automation-radio", RadioSet)
            remember = self.query_one("#remember-check", Checkbox).value
            automation_enabled = automation_radio.pressed_index == 1

            action_index = action_radio.pressed_index
            if action_index is None or action_index < 0:
                action_index = 0
            action_key = ACTIONS[action_index][0]

            self.config.automation.enabled = automation_enabled

            self.dismiss({
                "action": action_key,
                "automation_enabled": automation_enabled,
                "persist": remember,
            })
        elif event.button.id == "btn-quit":
            self.dismiss(None)

    def action_quit(self) -> None:
        self.dismiss(None)
