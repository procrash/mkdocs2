"""Model selection screen - choose master and slave models with persistent exclusion."""
from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import (
    Button,
    Checkbox,
    Footer,
    Header,
    Label,
    RadioButton,
    RadioSet,
    Rule,
    Static,
)

from ...config.schema import AppConfig, ModelHealthEntry
from ...discovery.model_classifier import ClassifiedModel
from . import sanitize_widget_id as _sanitize_id


class ModelSelectionScreen(Screen):
    """Select master and slave models. Allow persistent exclusion."""

    CSS = """
    ModelSelectionScreen {
        align: center middle;
    }
    #selection-box {
        width: 1fr;
        max-width: 120;
        height: 1fr;
        max-height: 95%;
        border: solid $primary;
        padding: 1 2;
        margin: 0 2;
    }
    #scroll-area {
        height: 1fr;
    }
    .section-title {
        margin-top: 1;
        margin-bottom: 0;
    }
    .hint-text {
        color: $text-muted;
        margin-bottom: 1;
    }
    #nav-row {
        margin-top: 1;
        align: center middle;
        height: 3;
        dock: bottom;
    }
    #nav-row Button {
        margin: 0 2;
    }
    """

    BINDINGS = [
        ("escape", "go_back", "Zurück"),
    ]

    def __init__(self, config: AppConfig, classified: list[ClassifiedModel]):
        super().__init__()
        self.config = config
        self.classified = classified
        # Build lookup: model_id → index in classified list
        self._model_index = {m.id: i for i, m in enumerate(classified)}

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        prev_slaves = set(self.config.preferences.selected_analysts)
        prev_master = self.config.preferences.selected_judge
        disabled_ids = {
            e.model_id for e in self.config.model_health.entries if not e.enabled
        }

        with Center():
            with Vertical(id="selection-box"):
                yield Label(
                    f"[bold]Modellauswahl — Master / Slave[/bold]  "
                    f"({len(self.classified)} Modelle verfügbar)",
                    classes="section-title",
                )
                yield Label(
                    "Master bewertet & synthetisiert, Slaves erzeugen Dokumentation.\n"
                    "Master kann auch als Slave eingesetzt werden.",
                    classes="hint-text",
                )

                with VerticalScroll(id="scroll-area"):
                    # ── Master Selection ────────────────────────────
                    yield Label("[bold yellow]Master[/bold yellow]", classes="section-title")
                    master_radio = RadioSet(id="master-radio")
                    with master_radio:
                        yield RadioButton(
                            "Kein Master",
                            value=(prev_master == ""),
                        )
                        for m in self.classified:
                            is_prev = (m.id == prev_master)
                            tag = " [red][X][/red]" if m.id in disabled_ids else ""
                            caps = ", ".join(c.value for c in m.capabilities)
                            yield RadioButton(
                                f"{m.id}{tag}  {m.size_class} {m.estimated_context:,} [{caps}]",
                                value=is_prev,
                            )

                    yield Rule()

                    # ── Slave Selection ─────────────────────────────
                    yield Label("[bold cyan]Slaves[/bold cyan] (mehrere möglich)", classes="section-title")
                    for m in self.classified:
                        tag = " [red][X][/red]" if m.id in disabled_ids else ""
                        caps = ", ".join(c.value for c in m.capabilities)
                        pre_selected = m.id in prev_slaves if prev_slaves else (m.id not in disabled_ids)
                        yield Checkbox(
                            f"{m.id}{tag}  {m.size_class} {m.estimated_context:,} [{caps}]",
                            value=pre_selected,
                            id=f"slave-{_sanitize_id(m.id)}",
                        )

                    yield Rule()

                    # ── Exclusion ───────────────────────────────────
                    yield Label("[bold red]Ausschließen[/bold red]", classes="section-title")
                    for m in self.classified:
                        yield Checkbox(
                            m.id,
                            value=(m.id in disabled_ids),
                            id=f"exclude-{_sanitize_id(m.id)}",
                        )

                with Horizontal(id="nav-row"):
                    yield Button("Zurück", id="btn-back")
                    yield Button("Weiter", variant="primary", id="btn-next")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            self._apply_and_dismiss()
        elif event.button.id == "btn-back":
            self.dismiss(None)

    def _apply_and_dismiss(self) -> None:
        available_ids = [m.id for m in self.classified]

        # ── Collect exclusions ──────────────────────────────
        newly_excluded: set[str] = set()
        for m in self.classified:
            try:
                cb = self.query_one(f"#exclude-{_sanitize_id(m.id)}", Checkbox)
                if cb.value:
                    newly_excluded.add(m.id)
            except Exception:
                pass

        # Update model_health entries
        existing_ids = {e.model_id for e in self.config.model_health.entries}
        for m_id in newly_excluded:
            if m_id in existing_ids:
                for e in self.config.model_health.entries:
                    if e.model_id == m_id:
                        e.enabled = False
                        break
            else:
                self.config.model_health.entries.append(
                    ModelHealthEntry(model_id=m_id, enabled=False)
                )
        # Re-enable un-checked models
        for e in self.config.model_health.entries:
            if e.model_id in available_ids and e.model_id not in newly_excluded:
                e.enabled = True

        # ── Collect master ──────────────────────────────────
        master_radio = self.query_one("#master-radio", RadioSet)
        master_idx = master_radio.pressed_index
        selected_master = ""
        # Index 0 = "Kein Master", indices 1..N map to self.classified
        if master_idx is not None and master_idx > 0 and master_idx <= len(self.classified):
            selected_master = self.classified[master_idx - 1].id
            # Don't select excluded model as master
            if selected_master in newly_excluded:
                selected_master = ""

        # ── Collect slaves ──────────────────────────────────
        selected_slaves: list[str] = []
        for m in self.classified:
            if m.id in newly_excluded:
                continue
            try:
                cb = self.query_one(f"#slave-{_sanitize_id(m.id)}", Checkbox)
                if cb.value:
                    selected_slaves.append(m.id)
            except Exception:
                pass

        # Fallback: select all non-excluded
        if not selected_slaves:
            selected_slaves = [m.id for m in self.classified if m.id not in newly_excluded]

        # Persist preferences
        self.config.preferences.selected_analysts = selected_slaves
        self.config.preferences.selected_judge = selected_master

        self.dismiss({
            "selected_slaves": selected_slaves,
            "selected_master": selected_master,
        })

    def action_go_back(self) -> None:
        self.dismiss(None)
