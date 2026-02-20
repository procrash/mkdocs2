"""Textual-based TUI application for mkdocsOnSteroids."""
from __future__ import annotations
import asyncio
import logging

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Footer,
    Header,
    Label,
    Log,
    ProgressBar,
    Static,
)

from ..config.schema import AppConfig
from .cli_runner import run_cli_pipeline

logger = logging.getLogger(__name__)


class StatsPanel(Static):
    """Panel showing generation statistics."""

    def compose(self) -> ComposeResult:
        yield Label("Files: 0 | Tasks: 0 | Done: 0 | Failed: 0", id="stats-label")

    def update_stats(self, files: int, tasks: int, done: int, failed: int) -> None:
        label = self.query_one("#stats-label", Label)
        label.update(f"Files: {files} | Tasks: {tasks} | Done: {done} | Failed: {failed}")


class MkDocsTUI(App):
    """Main TUI application."""

    CSS = """
    Screen {
        layout: grid;
        grid-size: 1 3;
        grid-rows: 3 1fr 3;
    }

    #top-bar {
        dock: top;
        height: 3;
        background: $primary;
        color: $text;
        content-align: center middle;
    }

    #main-content {
        layout: grid;
        grid-size: 2 1;
        grid-columns: 2fr 1fr;
    }

    #log-panel {
        border: solid $primary;
        height: 100%;
    }

    #stats-panel {
        border: solid $accent;
        height: 100%;
    }

    #progress-bar {
        dock: bottom;
        height: 3;
        margin: 0 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "toggle_dark", "Toggle Dark"),
    ]

    def __init__(self, config: AppConfig):
        super().__init__()
        self.config = config
        self._pipeline_task: asyncio.Task | None = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="main-content"):
            yield Log(id="log-panel", highlight=True)
            yield StatsPanel(id="stats-panel")
        yield ProgressBar(id="progress-bar", total=100, show_eta=True)
        yield Footer()

    def on_mount(self) -> None:
        self.title = "mkdocsOnSteroids"
        self.sub_title = self.config.project.name
        self._pipeline_task = asyncio.create_task(self._run_pipeline())

    async def _run_pipeline(self) -> None:
        log = self.query_one("#log-panel", Log)
        log.write_line("Starting documentation pipeline...")

        try:
            report = await run_cli_pipeline(self.config)
            log.write_line(f"\nPipeline complete: {report.successful} successful, {report.failed} failed")
            stats = self.query_one("#stats-panel", StatsPanel)
            stats.update_stats(
                report.total_files_scanned,
                report.total_tasks,
                report.successful,
                report.failed,
            )
            progress = self.query_one("#progress-bar", ProgressBar)
            progress.update(total=100, progress=100)
        except Exception as exc:
            log.write_line(f"\n[ERROR] Pipeline failed: {exc}")

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark


def run_tui(config: AppConfig) -> None:
    """Launch the TUI application."""
    app = MkDocsTUI(config)
    app.run()
