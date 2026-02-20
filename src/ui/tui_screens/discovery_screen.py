"""Discovery screen - probe LLM server and display available models.

Supports three modes:
- cached:  Load previously saved model data (no server probe)
- full:    Re-discover all models from scratch
- new:     Only probe models not yet in cache
"""
from __future__ import annotations
import asyncio
import logging

logger = logging.getLogger(__name__)

from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import (
    Button, DataTable, Footer, Header, Label,
    LoadingIndicator, RadioButton, RadioSet, Static,
)

from ...config.schema import AppConfig, ModelHealthEntry
from ...discovery.model_classifier import ClassifiedModel, classify_models
from ...discovery.role_assigner import RoleAssignment, assign_roles
from ...discovery.server_probe import (
    DiscoveredModel, probe_server,
    probe_all_context_lengths, probe_all_capabilities,
)


class DiscoveryScreen(Screen):
    """Probe LLM server and display discovered models."""

    CSS = """
    DiscoveryScreen {
        align: center middle;
    }
    #discovery-box {
        width: 1fr;
        max-width: 120;
        height: auto;
        max-height: 95%;
        border: solid $primary;
        padding: 1 2;
        margin: 0 2;
        overflow-y: auto;
    }
    #status-label {
        margin-bottom: 1;
    }
    #mode-section {
        padding: 1;
        border: dashed $accent;
        margin-bottom: 1;
    }
    #model-table {
        height: auto;
        max-height: 25;
    }
    #btn-row {
        margin-top: 1;
        align: center middle;
        height: auto;
        min-height: 3;
    }
    #btn-row Button {
        margin: 0 1;
        min-width: 14;
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
        self._detected_capabilities: dict[str, set[str]] = {}
        self._cached_model_ids: set[str] = set()  # IDs from previous sessions

    @property
    def _has_cached_data(self) -> bool:
        return len(self.config.model_health.entries) > 0

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Center():
            with Vertical(id="discovery-box"):
                yield Label(
                    f"[bold]LLM-Server-Erkennung[/bold]\n"
                    f"Server: {self.config.server.url}",
                    id="status-label",
                )
                # Mode selection — only shown when cached data exists
                with Vertical(id="mode-section"):
                    yield Label("[bold]Erkennungsmodus[/bold]")
                    yield RadioSet(
                        RadioButton("Gespeicherte Daten laden (kein Server-Zugriff)", value=True),
                        RadioButton("Alle Modelle neu erkennen"),
                        RadioButton("Nur neue Modelle erkennen (bereits bekannte überspringen)"),
                        id="mode-radio",
                    )
                    yield Button("Starten", variant="primary", id="btn-start-probe")
                yield LoadingIndicator(id="spinner")
                yield DataTable(id="model-table")
                yield Label("", id="probe-status")
                with Horizontal(id="btn-row"):
                    yield Button("Zurück", id="btn-back")
                    yield Button("Alle proben", variant="warning", id="btn-probe-all", disabled=True)
                    yield Button("Neue proben", variant="warning", id="btn-probe-new", disabled=True)
                    yield Button("Weiter", variant="primary", id="btn-next", disabled=True)
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#model-table", DataTable)
        table.add_columns("Modell", "Größe", "Context", "Quelle", "Capabilities")
        table.display = False
        self.query_one("#probe-status", Label).display = False
        self.query_one("#spinner", LoadingIndicator).display = False

        # Build set of previously known model IDs
        self._cached_model_ids = {e.model_id for e in self.config.model_health.entries}

        if self._has_cached_data:
            # Show mode selection
            n = len(self.config.model_health.entries)
            self.query_one("#status-label", Label).update(
                f"[bold]LLM-Server-Erkennung[/bold]\n"
                f"Server: {self.config.server.url}\n"
                f"[green]{n} Modelle aus vorheriger Sitzung gespeichert[/green]"
            )
        else:
            # No cached data — hide mode section, start full probe immediately
            self.query_one("#mode-section", Vertical).display = False
            self.query_one("#spinner", LoadingIndicator).display = True
            self.run_worker(self._probe(mode="full"), exclusive=True)

        # In auto mode, skip the selection
        if self.config.automation.enabled:
            self.query_one("#mode-section", Vertical).display = False
            if self._has_cached_data:
                self.run_worker(self._probe(mode="cached"), exclusive=True)
            else:
                self.query_one("#spinner", LoadingIndicator).display = True
                self.run_worker(self._probe(mode="full"), exclusive=True)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        bid = event.button.id
        if bid == "btn-start-probe":
            radio = self.query_one("#mode-radio", RadioSet)
            idx = radio.pressed_index
            if idx is None or idx < 0:
                idx = 0
            mode = ["cached", "full", "new"][idx]
            # Hide mode section, show spinner
            self.query_one("#mode-section", Vertical).display = False
            if mode != "cached":
                self.query_one("#spinner", LoadingIndicator).display = True
            self.run_worker(self._probe(mode=mode), exclusive=True)
        elif bid == "btn-next":
            self._finish()
        elif bid == "btn-back":
            self.dismiss(None)
        elif bid == "btn-probe-all":
            event.button.disabled = True
            self.run_worker(self._run_full_probe(new_only=False), exclusive=True)
        elif bid == "btn-probe-new":
            event.button.disabled = True
            self.run_worker(self._run_full_probe(new_only=True), exclusive=True)

    # ── Discovery Modes ───────────────────────────────────────────

    async def _probe(self, mode: str = "full") -> None:
        """Run discovery in the given mode: 'cached', 'full', or 'new'."""
        status = self.query_one("#status-label", Label)
        spinner = self.query_one("#spinner", LoadingIndicator)

        try:
            if mode == "cached":
                await self._load_from_cache(status)
            else:
                await self._discover_from_server(status, spinner, mode)
        except Exception as exc:
            status.update(
                f"[bold]LLM-Server-Erkennung[/bold]\n"
                f"[red]Fehler: {exc}[/red]"
            )
            spinner.display = False

        self.query_one("#btn-next", Button).disabled = False
        if self._discovered or self._classified:
            self.query_one("#btn-probe-all", Button).disabled = False
            self.query_one("#btn-probe-new", Button).disabled = False

        # Auto-advance in automation mode
        if self.config.automation.enabled and self._classified:
            await asyncio.sleep(1)
            self._finish()

    async def _load_from_cache(self, status: Label) -> None:
        """Load all model data from config (no server contact)."""
        entries = self.config.model_health.entries

        # Build context + capability maps from stored data
        for entry in entries:
            if entry.context_length > 0:
                self._detected_contexts[entry.model_id] = entry.context_length
            if entry.detected_capabilities:
                self._detected_capabilities[entry.model_id] = set(entry.detected_capabilities)
            # Create synthetic DiscoveredModel for each entry
            self._discovered.append(DiscoveredModel(
                id=entry.model_id,
                context_length=entry.context_length,
            ))

        model_ids = [e.model_id for e in entries]
        self._classified = classify_models(
            model_ids, self._detected_contexts, self._detected_capabilities,
        )
        self._assignment = assign_roles(self._classified)

        self._refresh_table()
        self._update_status_summary(status, from_cache=True)

    async def _discover_from_server(
        self, status: Label, spinner: LoadingIndicator, mode: str,
    ) -> None:
        """Probe server for models. mode='full' or 'new'."""
        status.update(
            f"[bold]LLM-Server-Erkennung[/bold]\n"
            f"Server: {self.config.server.url}\n"
            f"[yellow]Suche Modelle...[/yellow]"
        )
        spinner.display = True

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
                self._classified = [ClassifiedModel(
                    id="mock-model", capabilities=[], estimated_context=32768,
                )]
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

        self._discovered = discovered
        model_ids = [m.id for m in discovered]

        # Context from server probe
        self._detected_contexts = {
            m.id: m.context_length for m in discovered if m.context_length > 0
        }

        # Load saved data for ALL models (fill gaps)
        for entry in self.config.model_health.entries:
            if entry.context_length > 0 and entry.model_id not in self._detected_contexts:
                self._detected_contexts[entry.model_id] = entry.context_length
            if entry.detected_capabilities:
                self._detected_capabilities[entry.model_id] = set(entry.detected_capabilities)

        # Determine which models need capability probing
        if mode == "new":
            models_to_probe = [m for m in discovered if m.id not in self._cached_model_ids]
            n_new = len(models_to_probe)
            n_cached = len(discovered) - n_new
        else:
            models_to_probe = discovered
            n_new = len(discovered)
            n_cached = 0

        # Probe capabilities for selected models
        if models_to_probe:
            status.update(
                f"[bold]LLM-Server-Erkennung[/bold]\n"
                f"Server: {self.config.server.url}\n"
                f"[yellow]{len(discovered)} Modelle gefunden — "
                f"prüfe Capabilities für {len(models_to_probe)} Modelle...[/yellow]"
            )
            try:
                probed_caps = await probe_all_capabilities(
                    self.config.server.url,
                    models_to_probe,
                    self.config.server.api_key,
                    timeout=15,
                )
                self._detected_capabilities.update(probed_caps)
            except Exception as exc:
                logger.warning("Capability probe failed: %s", exc)

        self._classified = classify_models(
            model_ids, self._detected_contexts, self._detected_capabilities,
        )
        self._assignment = assign_roles(self._classified)

        self._refresh_table()
        spinner.display = False

        self._update_status_summary(status, n_new=n_new, n_cached=n_cached)

        # Save server URL preference
        self.config.preferences.last_server_url = self.config.server.url

    # ── Status Display ─────────────────────────────────────────────

    def _update_status_summary(
        self, status: Label,
        from_cache: bool = False,
        n_new: int = 0,
        n_cached: int = 0,
    ) -> None:
        """Update the status label with a summary of the current state."""
        total = len(self._classified)
        n_ctx = len(self._detected_contexts)
        n_instruct = sum(
            1 for m in self._classified
            if any(c.value == "instruct" for c in m.capabilities)
        )
        n_tool = sum(
            1 for m in self._classified
            if any(c.value == "tool_use" for c in m.capabilities)
        )
        n_heuristic_ctx = total - n_ctx

        if from_cache:
            source_info = "[dim](aus gespeicherten Daten)[/dim]"
        elif n_cached > 0:
            source_info = f"[dim]({n_new} neu erkannt, {n_cached} aus Cache)[/dim]"
        else:
            source_info = ""

        ctx_info = ""
        if n_ctx > 0 and n_heuristic_ctx > 0:
            ctx_info = f"Context: {n_ctx} erkannt, {n_heuristic_ctx} geschätzt"
        elif n_ctx > 0:
            ctx_info = f"Context: alle {n_ctx} erkannt"
        else:
            ctx_info = "Context: alle geschätzt — Diagnose empfohlen"

        status.update(
            f"[bold]LLM-Server-Erkennung[/bold]\n"
            f"[green]{total} Modelle[/green] {source_info}\n"
            f"[dim]{ctx_info}[/dim]\n"
            f"[dim]Instruct: {n_instruct}, Tool-Use: {n_tool}[/dim]\n"
            f"[dim]→ Weiter: Master/Slave-Rollenzuweisung[/dim]"
        )

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

    # ── Combined Probe (Context + Capabilities) ─────────────────

    async def _run_full_probe(self, new_only: bool = False) -> None:
        """Probe context lengths AND capabilities for models."""
        probe_label = self.query_one("#probe-status", Label)
        probe_label.display = True

        if new_only:
            ctx_models = [
                m for m in self._discovered
                if m.id not in self._cached_model_ids
                or self._detected_contexts.get(m.id, 0) == 0
            ]
            cap_models = [
                m for m in self._discovered
                if m.id not in self._detected_capabilities
            ]
            label_suffix = " (nur neue)"
        else:
            ctx_models = list(self._discovered)
            cap_models = list(self._discovered)
            label_suffix = ""

        def on_progress(model_id: str, current_test: int, msg: str):
            try:
                probe_label.update(f"[yellow]{model_id}[/yellow]: {msg}")
            except Exception:
                pass

        # 1. Context probe
        if ctx_models:
            probe_label.update(
                f"[yellow]Kontextfenster{label_suffix}: "
                f"{len(ctx_models)} Modelle...[/yellow]"
            )
            probed_ctx = await probe_all_context_lengths(
                self.config.server.url,
                ctx_models,
                self.config.server.api_key,
                timeout=30,
                progress_callback=on_progress,
            )
            self._detected_contexts.update(probed_ctx)

        # 2. Capability probe
        if cap_models:
            probe_label.update(
                f"[yellow]Capabilities{label_suffix}: "
                f"{len(cap_models)} Modelle...[/yellow]"
            )
            probed_caps = await probe_all_capabilities(
                self.config.server.url,
                cap_models,
                self.config.server.api_key,
                timeout=15,
                progress_callback=on_progress,
            )
            self._detected_capabilities.update(probed_caps)

        # Re-classify and update
        model_ids = [m.id for m in self._discovered]
        self._classified = classify_models(
            model_ids, self._detected_contexts, self._detected_capabilities,
        )
        self._assignment = assign_roles(self._classified)

        self._refresh_table()
        self._save_model_data()

        n_ctx = len(ctx_models)
        n_cap = len(cap_models)
        probe_label.update(
            f"[green]Fertig: {n_ctx} Ctx + {n_cap} Capabilities geprüft{label_suffix}[/green]"
        )
        status = self.query_one("#status-label", Label)
        self._update_status_summary(status)

    # ── Persistence ────────────────────────────────────────────────

    def _save_model_data(self) -> None:
        """Persist detected context lengths and capabilities into model_health.entries."""
        existing = {e.model_id: e for e in self.config.model_health.entries}

        all_ids = set(self._detected_contexts.keys()) | set(self._detected_capabilities.keys())
        for model_id in all_ids:
            ctx = self._detected_contexts.get(model_id, 0)
            caps = list(self._detected_capabilities.get(model_id, set()))

            if model_id in existing:
                entry = existing[model_id]
                if ctx > 0:
                    entry.context_length = ctx
                if caps:
                    entry.detected_capabilities = caps
            else:
                self.config.model_health.entries.append(
                    ModelHealthEntry(
                        model_id=model_id,
                        context_length=ctx,
                        detected_capabilities=caps,
                    )
                )
        try:
            self.app._save_config()
        except Exception:
            pass

    def _finish(self) -> None:
        self._save_model_data()
        self.dismiss({
            "classified": self._classified,
            "assignment": self._assignment,
        })

    def action_go_back(self) -> None:
        self.dismiss(None)
