"""Welcome screen - project info and automation mode selection."""
from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import Button, Checkbox, Footer, Header, Label, RadioButton, RadioSet, Static

from ...config.schema import AppConfig


class WelcomeScreen(Screen):
    """First screen: project overview and automation question."""

    CSS = """
    WelcomeScreen {
        align: center middle;
    }
    #welcome-box {
        width: 80;
        height: auto;
        border: solid $primary;
        padding: 1 2;
    }
    #project-info {
        margin-bottom: 1;
    }
    #automation-section {
        margin-top: 1;
        padding: 1;
        border: dashed $accent;
    }
    #btn-row {
        margin-top: 1;
        align: center middle;
        height: 3;
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
                    f"Ausgabe: {self.config.project.output_dir}\n\n"
                    f"[dim]Ablauf: Server-Erkennung → Master/Slave-Auswahl →\n"
                    f"Skelett-Vorschläge vom LLM → Skelett erstellen → Generierung → Chat[/dim]",
                    id="project-info",
                )
                with Vertical(id="automation-section"):
                    yield Label("[bold]Automatisierungsmodus[/bold]")
                    yield Label("Soll das Verhalten automatisiert gesteuert werden?")
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
                with Center(id="btn-row"):
                    yield Button("Weiter", variant="primary", id="btn-next")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            radio_set = self.query_one("#automation-radio", RadioSet)
            remember = self.query_one("#remember-check", Checkbox).value
            # Index 1 = Automatisch
            automation_enabled = radio_set.pressed_index == 1

            self.config.automation.enabled = automation_enabled

            if remember:
                self.dismiss({"automation_enabled": automation_enabled, "persist": True})
            else:
                self.dismiss({"automation_enabled": automation_enabled, "persist": False})

    def action_quit(self) -> None:
        self.app.exit()
