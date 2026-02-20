"""LLM Enhancement screen - shows progress while ensemble analyzes documentation."""
from __future__ import annotations

import asyncio
import logging

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import (
    Button,
    Footer,
    Header,
    Label,
    ProgressBar,
    RichLog,
)

from ...config.schema import AppConfig

logger = logging.getLogger(__name__)


class LlmEnhanceScreen(Screen):
    """Progress screen for the KI-gesteuerte Verbesserung ensemble process.

    Shows which models are running, their results, and overall progress.
    Dismisses with list[FileChange] on success, None on cancel/failure.
    """

    CSS = """
    LlmEnhanceScreen {
        layout: grid;
        grid-size: 1 5;
        grid-rows: auto auto auto 1fr auto;
    }
    #enhance-title {
        padding: 1 2;
        text-align: center;
    }
    #status-label {
        padding: 0 2;
        height: 3;
    }
    #progress {
        margin: 0 2;
        height: 3;
    }
    #enhance-log {
        border: solid $primary;
        margin: 1 2;
        height: 1fr;
    }
    #btn-row {
        height: 3;
        align: center middle;
        margin: 0 2;
    }
    """

    BINDINGS = [
        ("escape", "cancel", "Abbrechen"),
    ]

    def __init__(self, config: AppConfig, slaves: list[str], master: str):
        super().__init__()
        self.config = config
        self.slaves = slaves
        self.master = master
        self._cancelled = False
        self._task: asyncio.Task | None = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Label("[bold]KI-gesteuerte Verbesserung[/bold]", id="enhance-title")
        yield Label("Starte Analyse...", id="status-label")
        yield ProgressBar(id="progress", total=len(self.slaves))
        yield RichLog(id="enhance-log", highlight=True)
        with Horizontal(id="btn-row"):
            yield Button("Abbrechen", variant="error", id="btn-cancel")
        yield Footer()

    def on_mount(self) -> None:
        self.run_worker(self._run_enhancement(), exclusive=True)

    async def _run_enhancement(self) -> None:
        """Run the ensemble enhancement as a Textual worker."""
        from ...generator.llm_enhancer import run_llm_enhancement
        from ...orchestrator.semaphore import WorkerPool

        log = self.query_one("#enhance-log", RichLog)
        log.write(f"Modelle: {', '.join(self.slaves)}")
        if self.master:
            log.write(f"Master: {self.master}")
        log.write(f"Starte Ensemble-Analyse mit {len(self.slaves)} Modellen...\n")

        pool = WorkerPool(max_workers=3)

        def progress_cb(completed: int, total: int, model_id: str, status: str) -> None:
            if self._cancelled:
                return
            self.call_from_thread(self._update_progress, completed, total, model_id, status)

        try:
            changes = await run_llm_enhancement(
                config=self.config,
                slaves=self.slaves,
                master=self.master,
                pool=pool,
                progress_cb=progress_cb,
                mock_mode=False,
            )

            if self._cancelled:
                return

            if changes:
                self.call_from_thread(self._log_message, f"\n[green]{len(changes)} Änderungsvorschläge erhalten[/green]")
                self.call_from_thread(self.dismiss, changes)
            else:
                self.call_from_thread(self._log_message, "\n[yellow]Keine Änderungsvorschläge erhalten[/yellow]")
                self.call_from_thread(self._show_no_results)

        except asyncio.CancelledError:
            self.call_from_thread(self._log_message, "[yellow]Abgebrochen[/yellow]")
            self.call_from_thread(self.dismiss, None)
        except Exception as exc:
            logger.error("Enhancement failed: %s", exc, exc_info=True)
            self.call_from_thread(self._log_message, f"\n[red]Fehler: {exc}[/red]")
            self.call_from_thread(self._show_error, str(exc))

    def _update_progress(self, completed: int, total: int, model_id: str, status: str) -> None:
        """Update progress display (called from worker thread via call_from_thread)."""
        try:
            label = self.query_one("#status-label", Label)
            label.update(f"[bold]{status}[/bold]")
        except Exception:
            pass

        try:
            pb = self.query_one("#progress", ProgressBar)
            pb.update(total=total, progress=completed)
        except Exception:
            pass

        if model_id or status:
            self._log_message(f"  {status}" + (f" ({model_id})" if model_id else ""))

    def _log_message(self, msg: str) -> None:
        """Write a message to the log panel."""
        try:
            log = self.query_one("#enhance-log", RichLog)
            log.write(msg)
        except Exception:
            pass

    def _show_no_results(self) -> None:
        """Show no-results state and allow going back."""
        try:
            label = self.query_one("#status-label", Label)
            label.update("[yellow]Keine Verbesserungen vorgeschlagen[/yellow]")
            btn = self.query_one("#btn-cancel", Button)
            btn.label = "Zurück"
        except Exception:
            pass

    def _show_error(self, error: str) -> None:
        """Show error state."""
        try:
            label = self.query_one("#status-label", Label)
            label.update(f"[red]Fehler: {error[:80]}[/red]")
            btn = self.query_one("#btn-cancel", Button)
            btn.label = "Zurück"
        except Exception:
            pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-cancel":
            self._cancelled = True
            self.dismiss(None)

    def action_cancel(self) -> None:
        self._cancelled = True
        self.dismiss(None)
