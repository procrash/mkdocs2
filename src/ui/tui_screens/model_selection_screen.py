"""Model selection screen - choose analysts and judge."""
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
    Static,
)

from ...config.schema import AppConfig
from ...discovery.model_classifier import ClassifiedModel


class ModelSelectionScreen(Screen):
    """Select which models to use as analysts and judge."""

    CSS = """
    ModelSelectionScreen {
        align: center middle;
    }
    #selection-box {
        width: 90;
        height: auto;
        max-height: 85%;
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
    #btn-row {
        margin-top: 1;
        align: center middle;
        height: 3;
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

        previously_selected = set(self.config.preferences.selected_analysts)
        previous_judge = self.config.preferences.selected_judge

        with Center():
            with Vertical(id="selection-box"):
                yield Label("[bold]Modellauswahl[/bold]", classes="section-title")
                yield Label("Wähle die Analysten-Modelle und optional einen Richter.")

                # Analysts section
                yield Label("\n[bold cyan]Analysten[/bold cyan] (mehrere möglich):", classes="section-title")
                for m in self.classified:
                    caps = ", ".join(c.value for c in m.capabilities)
                    pre_selected = m.id in previously_selected if previously_selected else True
                    yield Checkbox(
                        f"{m.id} [{m.size_class}, ctx:{m.estimated_context}, {caps}]",
                        value=pre_selected,
                        id=f"analyst-{m.id}",
                        classes="model-row",
                    )

                # Judge section
                yield Label("\n[bold yellow]Richter[/bold yellow] (einer oder keiner):", classes="section-title")
                judge_buttons = [RadioButton("Kein Richter", value=(previous_judge == ""))]
                for m in self.classified:
                    is_prev_judge = (m.id == previous_judge)
                    judge_buttons.append(
                        RadioButton(
                            f"{m.id} [{m.size_class}]",
                            value=is_prev_judge,
                        )
                    )
                yield RadioSet(*judge_buttons, id="judge-radio")

                with Center(id="btn-row"):
                    yield Button("Weiter", variant="primary", id="btn-next")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            # Collect selected analysts
            selected_analysts: list[str] = []
            for m in self.classified:
                cb = self.query_one(f"#analyst-{m.id}", Checkbox)
                if cb.value:
                    selected_analysts.append(m.id)

            # Collect judge
            judge_radio = self.query_one("#judge-radio", RadioSet)
            judge_idx = judge_radio.pressed_index
            selected_judge = ""
            if judge_idx > 0:  # 0 = "Kein Richter"
                selected_judge = self.classified[judge_idx - 1].id

            # Persist preferences
            self.config.preferences.selected_analysts = selected_analysts
            self.config.preferences.selected_judge = selected_judge

            self.dismiss({
                "selected_analysts": selected_analysts,
                "selected_judge": selected_judge,
            })

    def action_go_back(self) -> None:
        self.dismiss(None)
