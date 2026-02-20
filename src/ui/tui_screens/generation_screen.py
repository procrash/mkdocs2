"""Generation screen - live progress, log, and server status during doc generation."""
from __future__ import annotations
import asyncio
import time
import webbrowser

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import (
    Button,
    Footer,
    Header,
    Label,
    Log,
    ProgressBar,
    Static,
)

from ...config.schema import AppConfig
from ...orchestrator.engine import GenerationResult, PipelineResult


class GenerationScreen(Screen):
    """Live progress display during documentation generation."""

    CSS = """
    GenerationScreen {
        layout: grid;
        grid-size: 1 4;
        grid-rows: 3 1fr 6 3;
    }
    #gen-header {
        dock: top;
        height: 3;
        padding: 0 2;
        background: $primary;
        color: $text;
    }
    #main-area {
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
        padding: 1;
    }
    #server-panel {
        height: 6;
        border: dashed $success;
        padding: 0 2;
    }
    #progress-section {
        dock: bottom;
        height: 3;
        margin: 0 1;
    }
    """

    BINDINGS = [
        ("p", "toggle_pause", "Pause"),
        ("o", "open_browser", "Browser öffnen"),
        ("q", "request_quit", "Beenden"),
    ]

    def __init__(self, config: AppConfig, mkdocs_url: str = ""):
        super().__init__()
        self.config = config
        self.mkdocs_url = mkdocs_url
        self._paused = False
        self._start_time = 0.0
        self._total_tasks = 0
        self._completed = 0
        self._failed = 0
        self._finished = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(id="main-area"):
            yield Log(id="log-panel", highlight=True)
            yield Static(id="stats-panel")
        yield Static(id="server-panel")
        yield ProgressBar(id="progress-section", total=100, show_eta=True)
        yield Footer()

    def on_mount(self) -> None:
        self._start_time = time.monotonic()
        self._update_stats()
        self._update_server_panel()

    def log_message(self, msg: str) -> None:
        """Write a message to the log panel."""
        try:
            log = self.query_one("#log-panel", Log)
            log.write_line(msg)
        except Exception:
            pass

    def update_progress(self, result: GenerationResult, pipeline: PipelineResult) -> None:
        """Called by the engine for each completed task."""
        self._total_tasks = pipeline.total_tasks
        self._completed = pipeline.successful
        self._failed = pipeline.failed
        done = self._completed + self._failed

        # Update progress bar
        try:
            pb = self.query_one("#progress-section", ProgressBar)
            pb.update(total=self._total_tasks, progress=done)
        except Exception:
            pass

        # Log result
        status = "[green]OK[/green]" if result.success else f"[red]FEHLER[/red] {result.error}"
        self.log_message(
            f"[{done}/{self._total_tasks}] "
            f"{result.task.stakeholder}/{result.task.doc_type}/"
            f"{result.task.file.relative_path}: {status}"
        )

        self._update_stats()

    def mark_finished(self, pipeline: PipelineResult) -> None:
        """Called when generation is complete."""
        self._finished = True
        self._total_tasks = pipeline.total_tasks
        self._completed = pipeline.successful
        self._failed = pipeline.failed
        duration = time.monotonic() - self._start_time

        self.log_message(f"\n[bold green]Generierung abgeschlossen![/bold green]")
        self.log_message(f"Erfolg: {self._completed} | Fehler: {self._failed} | Dauer: {duration:.1f}s")
        self._update_stats()

    def _update_stats(self) -> None:
        duration = time.monotonic() - self._start_time if self._start_time else 0
        done = self._completed + self._failed
        try:
            stats = self.query_one("#stats-panel", Static)
            stats.update(
                f"[bold]Statistik[/bold]\n\n"
                f"Gesamt:  {self._total_tasks}\n"
                f"Fertig:  [green]{self._completed}[/green]\n"
                f"Fehler:  [red]{self._failed}[/red]\n"
                f"Offen:   {max(0, self._total_tasks - done)}\n"
                f"Dauer:   {duration:.0f}s\n"
                f"Status:  {'Pause' if self._paused else 'Fertig' if self._finished else 'Läuft...'}"
            )
        except Exception:
            pass

    def _update_server_panel(self) -> None:
        try:
            panel = self.query_one("#server-panel", Static)
            if self.mkdocs_url:
                panel.update(
                    f"[bold]MkDocs-Server[/bold]: [green]{self.mkdocs_url}[/green]  |  "
                    f"Drücke [bold]o[/bold] um im Browser zu öffnen"
                )
            else:
                panel.update("[bold]MkDocs-Server[/bold]: [dim]Nicht gestartet[/dim]")
        except Exception:
            pass

    def action_toggle_pause(self) -> None:
        self._paused = not self._paused
        state = "Pause" if self._paused else "Fortgesetzt"
        self.log_message(f"[yellow]{state}[/yellow]")
        self._update_stats()

    def action_open_browser(self) -> None:
        if self.mkdocs_url:
            try:
                webbrowser.open(self.mkdocs_url)
                self.log_message(f"Browser geöffnet: {self.mkdocs_url}")
            except Exception as exc:
                self.log_message(f"[red]Browser-Fehler: {exc}[/red]")

    def action_request_quit(self) -> None:
        self.dismiss({"interrupted": not self._finished})
