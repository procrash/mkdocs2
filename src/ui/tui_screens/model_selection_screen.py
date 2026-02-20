"""Model selection screen - choose master and slave models with persistent exclusion."""
from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
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


class ModelSelectionScreen(Screen):
    """Select master and slave models. Allow persistent exclusion."""

    CSS = """
    ModelSelectionScreen {
        align: center middle;
    }
    #selection-box {
        width: 95;
        height: auto;
        max-height: 90%;
        border: solid $primary;
        padding: 1 2;
        overflow-y: auto;
    }
    .section-title {
        margin-top: 1;
        margin-bottom: 0;
    }
    .model-row {
        height: 3;
        padding: 0 1;
    }
    .exclude-row {
        height: 3;
        padding: 0 1;
    }
    #btn-row {
        margin-top: 1;
        align: center middle;
        height: 3;
    }
    .hint-text {
        color: $text-muted;
        margin-bottom: 1;
    }
    """

    BINDINGS = [
        ("escape", "go_back", "Zurück"),
    ]

    def __init__(self, config: AppConfig, classified: list[ClassifiedModel]):
        super().__init__()
        self.config = config
        self.classified = classified

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        prev_slaves = set(self.config.preferences.selected_analysts)
        prev_master = self.config.preferences.selected_judge
        disabled_ids = {
            e.model_id for e in self.config.model_health.entries if not e.enabled
        }

        with Center():
            with Vertical(id="selection-box"):
                yield Label("[bold]Modellauswahl — Master / Slave[/bold]", classes="section-title")
                yield Label(
                    "Wähle ein Master-Modell (bewertet & synthetisiert Ergebnisse) und\n"
                    "Slave-Modelle (erzeugen die Dokumentation). Das Master-Modell\n"
                    "kann auch als Slave eingesetzt werden.",
                    classes="hint-text",
                )

                # ── Master Selection ────────────────────────────────
                yield Label("[bold yellow]Master-Modell[/bold yellow] (eines auswählen):", classes="section-title")
                master_buttons = [RadioButton("Kein Master (kein Ensemble)", value=(prev_master == ""))]
                for m in self.classified:
                    if m.id in disabled_ids:
                        continue
                    is_prev = (m.id == prev_master)
                    caps = ", ".join(c.value for c in m.capabilities)
                    master_buttons.append(
                        RadioButton(
                            f"{m.id} [{m.size_class}, ctx:{m.estimated_context:,}, {caps}]",
                            value=is_prev,
                        )
                    )
                yield RadioSet(*master_buttons, id="master-radio")

                yield Rule()

                # ── Slave Selection ─────────────────────────────────
                yield Label(
                    "[bold cyan]Slave-Modelle[/bold cyan] (mehrere möglich, Master kann auch Slave sein):",
                    classes="section-title",
                )
                for m in self.classified:
                    if m.id in disabled_ids:
                        continue
                    caps = ", ".join(c.value for c in m.capabilities)
                    pre_selected = m.id in prev_slaves if prev_slaves else True
                    yield Checkbox(
                        f"{m.id} [{m.size_class}, ctx:{m.estimated_context:,}, {caps}]",
                        value=pre_selected,
                        id=f"slave-{m.id}",
                        classes="model-row",
                    )

                yield Rule()

                # ── Persistent Exclusion ────────────────────────────
                yield Label(
                    "[bold red]Modelle dauerhaft ausschließen[/bold red] (werden in config.yaml gespeichert):",
                    classes="section-title",
                )
                yield Label(
                    "Ausgeschlossene Modelle werden bei zukünftigen Starts ignoriert.",
                    classes="hint-text",
                )
                for m in self.classified:
                    is_excluded = m.id in disabled_ids
                    yield Checkbox(
                        f"{m.id} ausschließen",
                        value=is_excluded,
                        id=f"exclude-{m.id}",
                        classes="exclude-row",
                    )

                with Center(id="btn-row"):
                    yield Button("Weiter", variant="primary", id="btn-next")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            self._apply_and_dismiss()

    def _apply_and_dismiss(self) -> None:
        # Build set of non-excluded model IDs (for filtering)
        available_ids = [m.id for m in self.classified]

        # ── Collect exclusions ──────────────────────────────
        newly_excluded: set[str] = set()
        for m in self.classified:
            try:
                cb = self.query_one(f"#exclude-{m.id}", Checkbox)
                if cb.value:
                    newly_excluded.add(m.id)
            except Exception:
                pass

        # Update model_health entries in config
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
        # Re-enable models that were un-checked
        for e in self.config.model_health.entries:
            if e.model_id in available_ids and e.model_id not in newly_excluded:
                e.enabled = True

        # ── Collect master ──────────────────────────────────
        master_radio = self.query_one("#master-radio", RadioSet)
        master_idx = master_radio.pressed_index
        selected_master = ""
        # Index 0 = "Kein Master", rest map to non-excluded classified models
        non_excluded = [m for m in self.classified if m.id not in newly_excluded]
        if master_idx > 0 and master_idx <= len(non_excluded):
            selected_master = non_excluded[master_idx - 1].id

        # ── Collect slaves ──────────────────────────────────
        selected_slaves: list[str] = []
        for m in self.classified:
            if m.id in newly_excluded:
                continue
            try:
                cb = self.query_one(f"#slave-{m.id}", Checkbox)
                if cb.value:
                    selected_slaves.append(m.id)
            except Exception:
                pass

        # If no slaves selected, select all non-excluded as fallback
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
