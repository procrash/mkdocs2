"""Discovery screen - probe LLM server and display available models."""
from __future__ import annotations
import asyncio

from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Header, Label, LoadingIndicator, Static

from ...config.schema import AppConfig
from ...discovery.model_classifier import ClassifiedModel, classify_models
from ...discovery.role_assigner import RoleAssignment, assign_roles
from ...discovery.server_probe import DiscoveredModel, probe_server, probe_all_context_lengths


class DiscoveryScreen(Screen):
    """Probe LLM server and display discovered models."""

    CSS = """
    DiscoveryScreen {
        align: center middle;
    }
    #discovery-box {
        width: 95;
        height: auto;
        max-height: 85%;
        border: solid $primary;
        padding: 1 2;
        overflow-y: auto;
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
        height: 5;
    }
    #btn-row Button {
        margin: 0 2;
    }
    #probe-status {
        margin-top: 1;
        color: $text-muted;
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
        self._discovered: list[DiscoveredModel] = []
        self._detected_contexts: dict[str, int] = {}

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
                yield Label("", id="probe-status")
                with Horizontal(id="btn-row"):
                    yield Button("← Zurück", variant="default", id="btn-back")
                    yield Button(
                        "Kontextfenster diagnostizieren",
                        variant="warning",
                        id="btn-probe-ctx",
                        disabled=True,
                    )
                    yield Button("Weiter →", variant="primary", id="btn-next", disabled=True)
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#model-table", DataTable)
        table.add_columns("Modell", "Größe", "Context", "Quelle", "Capabilities")
        table.display = False
        self.query_one("#probe-status", Label).display = False
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

            self._discovered = await probe_server(
                self.config.server.url,
                self.config.server.api_key,
                self.config.server.timeout_connect,
            )

            if not self._discovered:
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

            # Build detected context map from server probe results
            model_ids = [m.id for m in self._discovered]
            self._detected_contexts = {
                m.id: m.context_length for m in self._discovered if m.context_length > 0
            }

            self._classified = classify_models(model_ids, self._detected_contexts)
            self._assignment = assign_roles(self._classified)

            self._refresh_table()

            spinner.display = False

            # Show how many have detected vs heuristic context
            n_detected = len(self._detected_contexts)
            n_heuristic = len(self._discovered) - n_detected
            ctx_info = ""
            if n_detected > 0:
                ctx_info = f"  ({n_detected} vom Server, {n_heuristic} geschätzt)"
            else:
                ctx_info = "  (alle Werte geschätzt — Diagnose empfohlen)"

            status.update(
                f"[bold]LLM-Server-Erkennung[/bold]\n"
                f"[green]{len(self._discovered)} Modelle gefunden[/green]{ctx_info}\n"
                f"[dim]→ Weiter: Master/Slave-Rollenzuweisung[/dim]"
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
        if self._discovered:
            self.query_one("#btn-probe-ctx", Button).disabled = False

        # Auto-advance in automation mode
        if self.config.automation.enabled and self._classified:
            await asyncio.sleep(2)
            self._finish()

    def _refresh_table(self) -> None:
        """Rebuild the DataTable with current classification data."""
        disabled_ids = {
            e.model_id for e in self.config.model_health.entries if not e.enabled
        }

        table = self.query_one("#model-table", DataTable)
        table.clear()

        for m in self._classified:
            caps = ", ".join(c.value for c in m.capabilities)
            disabled_mark = " [red][X][/red]" if m.id in disabled_ids else ""
            ctx_display = f"{m.estimated_context:,}"

            # Indicate source of context value
            if m.id in self._detected_contexts:
                ctx_source = "Server/API"
            else:
                ctx_source = "[dim]Heuristik[/dim]"

            table.add_row(
                f"{m.id}{disabled_mark}", m.size_class,
                ctx_display, ctx_source, caps,
            )

        table.display = True

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            self._finish()
        elif event.button.id == "btn-back":
            self.dismiss(None)
        elif event.button.id == "btn-probe-ctx":
            event.button.disabled = True
            self.run_worker(self._run_context_probe(), exclusive=True)

    async def _run_context_probe(self) -> None:
        """Actively probe context lengths for all models via chat completions."""
        probe_label = self.query_one("#probe-status", Label)
        probe_label.display = True

        def on_progress(model_id: str, current_test: int, msg: str):
            try:
                probe_label.update(f"[yellow]{model_id}[/yellow]: {msg}")
            except Exception:
                pass

        probe_label.update("[yellow]Starte aktive Kontextfenster-Diagnose...[/yellow]")

        probed = await probe_all_context_lengths(
            self.config.server.url,
            self._discovered,
            self.config.server.api_key,
            timeout=30,
            progress_callback=on_progress,
        )

        # Merge probed values into detected contexts
        self._detected_contexts.update(probed)

        # Re-classify with real context lengths
        model_ids = [m.id for m in self._discovered]
        self._classified = classify_models(model_ids, self._detected_contexts)
        self._assignment = assign_roles(self._classified)

        self._refresh_table()

        n_probed = sum(1 for v in probed.values() if v > 0)
        probe_label.update(
            f"[green]Diagnose abgeschlossen: {n_probed} Modelle aktiv getestet[/green]"
        )

        status = self.query_one("#status-label", Label)
        status.update(
            f"[bold]LLM-Server-Erkennung[/bold]\n"
            f"[green]{len(self._discovered)} Modelle gefunden[/green]  "
            f"(Kontextfenster aktiv diagnostiziert)"
        )

    def _finish(self) -> None:
        self.dismiss({
            "classified": self._classified,
            "assignment": self._assignment,
        })

    def action_go_back(self) -> None:
        self.dismiss(None)
