"""Failure screen - modal dialog when an LLM model fails."""
from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.screen import ModalScreen
from textual.widgets import (
    Button,
    Checkbox,
    Footer,
    Label,
    RadioButton,
    RadioSet,
    Select,
    Static,
)

from ...config.schema import AppConfig, ModelHealthEntry


class FailureScreen(ModalScreen):
    """Modal dialog displayed when an LLM model fails."""

    CSS = """
    FailureScreen {
        align: center middle;
    }
    #failure-box {
        width: 70;
        height: auto;
        border: solid $error;
        padding: 1 2;
        background: $surface;
    }
    .error-detail {
        color: $error;
        margin: 1 0;
    }
    #action-section {
        margin-top: 1;
        padding: 1;
        border: dashed $warning;
    }
    #btn-row {
        margin-top: 1;
        align: center middle;
        height: 3;
    }
    """

    def __init__(
        self,
        config: AppConfig,
        failed_model_id: str,
        error_message: str,
        available_models: list[str],
    ):
        super().__init__()
        self.config = config
        self.failed_model_id = failed_model_id
        self.error_message = error_message
        self.available_models = [m for m in available_models if m != failed_model_id]

    def compose(self) -> ComposeResult:
        with Center():
            with Vertical(id="failure-box"):
                yield Label("[bold red]Modell-Ausfall[/bold red]")
                yield Label(f"Modell: [bold]{self.failed_model_id}[/bold]")
                yield Label(f"Fehler: {self.error_message[:200]}", classes="error-detail")

                with Vertical(id="action-section"):
                    yield Label("[bold]Wie soll weitergemacht werden?[/bold]")
                    yield RadioSet(
                        RadioButton("Weiter versuchen (Retry)", value=True),
                        RadioButton("Modell deaktivieren", value=False),
                        id="action-radio",
                    )

                    if self.available_models:
                        yield Label("\nErsatzmodell:")
                        options = [(m, m) for m in self.available_models]
                        yield Select(
                            options,
                            id="replacement-select",
                            prompt="Kein Ersatz",
                            allow_blank=True,
                        )

                    yield Checkbox(
                        "Entscheidung in config.yaml speichern",
                        value=True,
                        id="persist-check",
                    )

                with Center(id="btn-row"):
                    yield Button("Bestätigen", variant="primary", id="btn-confirm")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-confirm":
            radio = self.query_one("#action-radio", RadioSet)
            retry = radio.pressed_index == 0
            persist = self.query_one("#persist-check", Checkbox).value

            replacement = ""
            try:
                select = self.query_one("#replacement-select", Select)
                if select.value and select.value != Select.BLANK:
                    replacement = str(select.value)
            except Exception:
                pass

            if persist and not retry:
                # Save to model health config
                entry = ModelHealthEntry(
                    model_id=self.failed_model_id,
                    enabled=False,
                    replacement_model_id=replacement,
                    failure_count=1,
                )
                # Update or append
                found = False
                for i, e in enumerate(self.config.model_health.entries):
                    if e.model_id == self.failed_model_id:
                        self.config.model_health.entries[i] = entry
                        found = True
                        break
                if not found:
                    self.config.model_health.entries.append(entry)

            self.dismiss({
                "retry": retry,
                "disable": not retry,
                "replacement": replacement,
                "persist": persist,
            })
