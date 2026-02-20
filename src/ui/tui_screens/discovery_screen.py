"""Discovery screen - probe LLM server and display available models."""
from __future__ import annotations
import asyncio

from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Header, Label, LoadingIndicator, Static

from ...config.schema import AppConfig
from ...discovery.model_classifier import ClassifiedModel, classify_models
from ...discovery.role_assigner import RoleAssignment, assign_roles
from ...discovery.server_probe import probe_server


class DiscoveryScreen(Screen):
    """Probe LLM server and display discovered models."""

    CSS = """
    DiscoveryScreen {
        align: center middle;
    }
    #discovery-box {
        width: 90;
        height: auto;
        max-height: 80%;
        border: solid $primary;
        padding: 1 2;
    }
    #status-label {
        margin-bottom: 1;
    }
    #model-table {
        height: auto;
        max-height: 20;
    }
    #btn-row {
        margin-top: 1;
        align: center middle;
        height: 3;
    }
    """

    BINDINGS = [
        ("escape", "go_back", "Zurück"),
    ]

    def __init__(self, config: AppConfig):
        super().__init__()
        self.config = config
        self._classified: list[ClassifiedModel] = []
        self._assignment: RoleAssignment = RoleAssignment()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Center():
            with Vertical(id="discovery-box"):
                yield Label(
                    f"[bold]LLM-Server-Erkennung[/bold]\n"
                    f"Server: {self.config.server.url}",
                    id="status-label",
                )
                yield LoadingIndicator(id="spinner")
                yield DataTable(id="model-table")
                with Center(id="btn-row"):
                    yield Button("Weiter", variant="primary", id="btn-next", disabled=True)
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#model-table", DataTable)
        table.add_columns("Modell", "Rolle", "Größe", "Context", "Capabilities")
        table.display = False
        self.run_worker(self._probe(), exclusive=True)

    async def _probe(self) -> None:
        status = self.query_one("#status-label", Label)
        spinner = self.query_one("#spinner", LoadingIndicator)

        try:
            status.update(
                f"[bold]LLM-Server-Erkennung[/bold]\n"
                f"Server: {self.config.server.url}\n"
                f"[yellow]Suche Modelle...[/yellow]"
            )

            discovered = await probe_server(
                self.config.server.url,
                self.config.server.api_key,
                self.config.server.timeout_connect,
            )

            if not discovered:
                if self.config.system.mock_mode:
                    status.update(
                        f"[bold]LLM-Server-Erkennung[/bold]\n"
                        f"[yellow]Kein Server erreichbar - Mock-Modus aktiv[/yellow]"
                    )
                    from ...discovery.model_classifier import ClassifiedModel
                    self._classified = [ClassifiedModel(id="mock-model", capabilities=[], estimated_context=32768)]
                    self._assignment = RoleAssignment(analysts=self._classified)
                else:
                    status.update(
                        f"[bold]LLM-Server-Erkennung[/bold]\n"
                        f"[red]Keine Modelle gefunden bei {self.config.server.url}[/red]\n"
                        f"Prüfe Server-URL oder aktiviere Mock-Modus."
                    )
                spinner.display = False
                self.query_one("#btn-next", Button).disabled = False
                return

            model_ids = [m.id for m in discovered]
            self._classified = classify_models(model_ids)
            self._assignment = assign_roles(self._classified)

            # Check model health entries for disabled models
            disabled_ids = {
                e.model_id for e in self.config.model_health.entries if not e.enabled
            }

            table = self.query_one("#model-table", DataTable)
            for m in self._classified:
                role = "Judge" if self._assignment.judge and m.id == self._assignment.judge.id else "Analyst"
                caps = ", ".join(c.value for c in m.capabilities)
                disabled_mark = " [red][X][/red]" if m.id in disabled_ids else ""
                table.add_row(
                    f"{m.id}{disabled_mark}", role, m.size_class,
                    str(m.estimated_context), caps,
                )

            table.display = True
            spinner.display = False

            status.update(
                f"[bold]LLM-Server-Erkennung[/bold]\n"
                f"[green]{len(discovered)} Modelle gefunden[/green]"
            )

            # Save server URL preference
            self.config.preferences.last_server_url = self.config.server.url

        except Exception as exc:
            status.update(
                f"[bold]LLM-Server-Erkennung[/bold]\n"
                f"[red]Fehler: {exc}[/red]"
            )
            spinner.display = False

        self.query_one("#btn-next", Button).disabled = False

        # Auto-advance in automation mode
        if self.config.automation.enabled and self._classified:
            await asyncio.sleep(2)
            self._finish()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            self._finish()

    def _finish(self) -> None:
        self.dismiss({
            "classified": self._classified,
            "assignment": self._assignment,
        })

    def action_go_back(self) -> None:
        self.dismiss(None)
