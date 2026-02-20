"""Textual-based multi-screen TUI application for mkdocsOnSteroids.

Orchestrates the full workflow: welcome → discovery → model selection →
skeleton suggestions → skeleton → generation → chat.

All user decisions are persisted in config.yaml for resume support.
All logging is captured into the TUI – nothing leaks to the raw console.
"""
from __future__ import annotations
import asyncio
import logging
import os
from pathlib import Path

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from ..config.loader import save_config
from ..config.schema import AppConfig, ModelHealthEntry
from ..discovery.model_classifier import ClassifiedModel
from ..discovery.role_assigner import RoleAssignment
from .tui_screens import (
    ChatScreen,
    DiscoveryScreen,
    FailureScreen,
    GenerationScreen,
    ModelSelectionScreen,
    SkeletonScreen,
    SkeletonSuggestionsScreen,
    WelcomeScreen,
)

logger = logging.getLogger(__name__)


# ── Logging into the TUI ─────────────────────────────────────────────


class _TuiLogHandler(logging.Handler):
    """Routes all log records into the currently-active GenerationScreen log widget.

    Falls back to /dev/null – never to stdout/stderr, so the TUI stays clean.
    """

    def __init__(self) -> None:
        super().__init__()
        self._target_widget = None          # set by GenerationScreen when active
        self._buffer: list[str] = []        # buffer while no widget is attached

    def attach(self, log_widget) -> None:
        self._target_widget = log_widget
        # flush buffer
        for line in self._buffer:
            try:
                self._target_widget.write_line(line)
            except Exception:
                pass
        self._buffer.clear()

    def detach(self) -> None:
        self._target_widget = None

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            if self._target_widget is not None:
                self._target_widget.write_line(f"[dim]{msg}[/dim]")
            else:
                self._buffer.append(msg)
                # Keep buffer bounded
                if len(self._buffer) > 500:
                    self._buffer = self._buffer[-200:]
        except Exception:
            pass                            # never crash, never print


def _redirect_logging_to_tui() -> _TuiLogHandler:
    """Replace every stdlib log handler with our TUI handler.

    This is the key to keeping the terminal clean: nothing goes to
    stdout/stderr anymore once this is called.
    """
    handler = _TuiLogHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%H:%M:%S")
    )
    root = logging.getLogger()
    for h in root.handlers[:]:
        root.removeHandler(h)
    root.addHandler(handler)
    root.setLevel(logging.INFO)
    return handler


# ── Main TUI App ─────────────────────────────────────────────────────


class MkDocsTUI(App):
    """Main multi-screen TUI application."""

    CSS = """
    Screen {
        background: $surface;
    }
    """

    BINDINGS = [
        ("q", "quit", "Beenden"),
        ("d", "toggle_dark", "Dark/Light"),
    ]

    def __init__(self, config: AppConfig, config_path: Path = Path("config.yaml"), auto_mode: bool = False):
        super().__init__()
        self.config = config
        self.config_path = config_path
        self._cli_auto = auto_mode          # Only True when --auto flag was passed
        self.auto_mode = auto_mode           # Will be set by WelcomeScreen choice
        self._log_handler: _TuiLogHandler | None = None

        # Runtime state
        self._classified: list[ClassifiedModel] = []
        self._assignment: RoleAssignment = RoleAssignment()
        self._selected_slaves: list[str] = []
        self._selected_master: str = ""
        self._mkdocs_url: str = ""
        self._mkdocs_server = None
        self._file_listing: str = ""

    def on_mount(self) -> None:
        self.title = "mkdocsOnSteroids"
        self.sub_title = self.config.project.name

        resume = self.config.resume
        if self._cli_auto:
            # --auto CLI flag: skip welcome, go straight to discovery
            self.auto_mode = True
            self._start_discovery()
        elif resume.last_screen:
            self._resume_from(resume.last_screen)
        else:
            # Always show welcome screen so user can choose manual/auto
            self._start_welcome()

    def _save_config(self) -> None:
        try:
            save_config(self.config, self.config_path)
        except Exception as exc:
            logger.error("Failed to save config: %s", exc)

    def _update_resume(self, screen_name: str) -> None:
        self.config.resume.last_screen = screen_name
        self._save_config()

    # ── Screen Flow ──────────────────────────────────────────────────

    def _start_welcome(self) -> None:
        self._update_resume("welcome")
        self.push_screen(WelcomeScreen(self.config), callback=self._on_welcome_result)

    def _on_welcome_result(self, result: dict | None) -> None:
        if result is None:
            self.exit()
            return
        if result.get("persist"):
            self.config.automation.enabled = result["automation_enabled"]
            self._save_config()
        self.auto_mode = result.get("automation_enabled", False)

        action = result.get("action", "run")
        self._dispatch_action(action)

    def _dispatch_action(self, action: str) -> None:
        """Route an action from the welcome screen to the corresponding flow."""
        if action == "run":
            self._start_discovery()
        elif action == "discover":
            self._start_discovery()
        elif action == "generate":
            # Skip to generation (reuse existing model config if available)
            self._restore_model_config()
            self._start_generation()
        elif action == "init":
            self._run_init_skeleton()
        elif action == "enhance":
            self._run_enhance()
        elif action == "restructure":
            self._run_restructure()
        elif action == "serve":
            self._run_serve()
        elif action == "report":
            self._run_report()
        else:
            self._start_discovery()

    def _restore_model_config(self) -> None:
        """Restore model selections from preferences (for actions that skip discovery)."""
        if self.config.preferences.selected_analysts:
            self._selected_slaves = list(self.config.preferences.selected_analysts)
        if self.config.preferences.selected_judge:
            self._selected_master = self.config.preferences.selected_judge

    def _run_init_skeleton(self) -> None:
        """Create skeleton and show result."""
        from ..generator.skeleton_builder import create_skeleton, create_suggestion_files
        from ..generator.mkdocs_builder import write_mkdocs_config

        output_dir = self.config.project.output_dir
        created = create_skeleton(output_dir, self.config.project.name)
        if self.config.preferences.skeleton_suggestions:
            create_suggestion_files(output_dir, self.config.preferences.skeleton_suggestions)
        write_mkdocs_config(self.config, output_dir)
        self.config.resume.skeleton_created = True
        self._save_config()
        self.notify(f"Skeleton: {len(created)} Dateien erstellt", title="Init", severity="information")
        self._start_welcome()

    def _run_enhance(self) -> None:
        """Enhance mkdocs.yml with plugins and extensions."""
        from ..generator.mkdocs_enhancer import enhance_mkdocs_config
        mkdocs_path = self.config.project.output_dir / "mkdocs.yml"
        if not mkdocs_path.exists():
            self.notify("mkdocs.yml nicht gefunden — zuerst Skeleton erstellen", severity="error")
            self._start_welcome()
            return
        result = enhance_mkdocs_config(mkdocs_path, plugins=True, extensions=True)
        added = len(result["plugins"]) + len(result["extensions"])
        if added:
            self.notify(f"+{len(result['plugins'])} Plugins, +{len(result['extensions'])} Extensions", title="Enhance")
        else:
            self.notify("Alles bereits aktiv — nichts hinzugefügt", title="Enhance")
        self._start_welcome()

    def _run_restructure(self) -> None:
        """Show restructuring suggestions via notification."""
        docs_dir = self.config.project.output_dir / "docs"
        if not docs_dir.exists():
            self.notify("Kein docs/-Verzeichnis gefunden", severity="error")
            self._start_welcome()
            return
        md_files = list(docs_dir.rglob("*.md"))
        empty = sum(1 for f in md_files if f.stat().st_size < 100)
        large = sum(1 for f in md_files if f.stat().st_size > 50000)
        self.notify(
            f"{len(md_files)} Dateien, {empty} fast leer, {large} sehr groß",
            title="Restrukturierung",
        )
        self._start_welcome()

    def _run_serve(self) -> None:
        """Start MkDocs dev server."""
        from ..generator.mkdocs_server import MkDocsServer
        output_dir = self.config.project.output_dir
        port = self.config.preferences.preferred_port or 8000
        mkdocs_yml = output_dir / "mkdocs.yml"
        if not mkdocs_yml.exists():
            self.notify("mkdocs.yml nicht gefunden", severity="error")
            self._start_welcome()
            return
        try:
            self._mkdocs_server = MkDocsServer(output_dir, port=port)
            self._mkdocs_url = self._mkdocs_server.start()
            self.notify(f"Server läuft: {self._mkdocs_url}", title="MkDocs Serve")
        except Exception as exc:
            self.notify(f"Server-Start fehlgeschlagen: {exc}", severity="error")
        self._start_welcome()

    def _run_report(self) -> None:
        """Show generation report."""
        report_path = self.config.project.output_dir / "generation_report.md"
        if report_path.exists():
            content = report_path.read_text(encoding="utf-8")[:500]
            self.notify(content, title="Generierungsbericht", timeout=10)
        else:
            self.notify("Kein Bericht gefunden — zuerst 'Generierung' ausführen", severity="warning")
        self._start_welcome()

    def _start_discovery(self) -> None:
        self._update_resume("discovery")
        self.push_screen(DiscoveryScreen(self.config), callback=self._on_discovery_result)

    def _on_discovery_result(self, result: dict | None) -> None:
        if result is None:
            if self.auto_mode:
                self.exit()
            else:
                self._start_welcome()
            return

        self._classified = result.get("classified", [])
        self._assignment = result.get("assignment", RoleAssignment())
        self._build_file_listing()

        if self.auto_mode:
            # In auto mode: auto-assign models but still respect exclusions
            disabled = self._get_disabled_models()
            self._selected_slaves = [m.id for m in self._classified if m.id not in disabled]
            if self._assignment.judge and self._assignment.judge.id not in disabled:
                self._selected_master = self._assignment.judge.id
            else:
                self._selected_master = ""
            self._apply_model_config()
            # Still fetch skeleton suggestions (use defaults if LLM unavailable)
            if not self.config.resume.suggestions_fetched:
                self._start_skeleton_suggestions()
            else:
                self._start_skeleton()
        else:
            self._start_model_selection()

    def _start_model_selection(self) -> None:
        self._update_resume("model_selection")
        self.push_screen(
            ModelSelectionScreen(self.config, self._classified),
            callback=self._on_model_selection_result,
        )

    def _on_model_selection_result(self, result: dict | None) -> None:
        if result is None:
            self._start_discovery()
            return

        self._selected_slaves = result.get("selected_slaves", [])
        self._selected_master = result.get("selected_master", "")
        self._apply_model_config()
        self._save_config()
        self._start_skeleton_suggestions()

    def _start_skeleton_suggestions(self) -> None:
        self._update_resume("skeleton_suggestions")
        self.push_screen(
            SkeletonSuggestionsScreen(
                self.config,
                file_listing=self._file_listing,
                model_ids=self._selected_slaves,
            ),
            callback=self._on_suggestions_result,
        )

    def _on_suggestions_result(self, result: dict | None) -> None:
        if result is None:
            self._start_model_selection()
            return
        self.config.preferences.skeleton_suggestions = result.get("suggestions", [])
        self._save_config()
        self._start_skeleton()

    def _start_skeleton(self) -> None:
        self._update_resume("skeleton")
        self.push_screen(SkeletonScreen(self.config), callback=self._on_skeleton_result)

    def _on_skeleton_result(self, result: dict | None) -> None:
        if result is None:
            if self.auto_mode:
                self._start_discovery()
            else:
                self._start_skeleton_suggestions()
            return

        start_mkdocs = result.get("start_mkdocs", False)
        port = result.get("port", 8000)

        from ..generator.skeleton_builder import create_skeleton, create_suggestion_files
        create_skeleton(self.config.project.output_dir, self.config.project.name)
        create_suggestion_files(self.config.project.output_dir, self.config.preferences.skeleton_suggestions)
        self.config.resume.skeleton_created = True

        from ..generator.mkdocs_builder import write_mkdocs_config
        write_mkdocs_config(self.config, self.config.project.output_dir)

        # Enhance mkdocs.yml with plugins + extensions if requested
        enhance = result.get("enhance_mkdocs", False)
        if enhance:
            from ..generator.mkdocs_enhancer import enhance_mkdocs_config
            mkdocs_path = self.config.project.output_dir / "mkdocs.yml"
            enhance_mkdocs_config(mkdocs_path, plugins=True, extensions=True)

        if start_mkdocs:
            from ..generator.mkdocs_server import MkDocsServer
            self._mkdocs_server = MkDocsServer(self.config.project.output_dir, port=port)
            try:
                self._mkdocs_url = self._mkdocs_server.start()
                self.config.resume.mkdocs_server_started = True
            except Exception as exc:
                logger.error("MkDocs server start failed: %s", exc)
                self._mkdocs_url = ""

        self._save_config()
        self._start_generation()

    def _start_generation(self) -> None:
        self._update_resume("generation")
        gen_screen = GenerationScreen(self.config, mkdocs_url=self._mkdocs_url)
        self.push_screen(gen_screen, callback=self._on_generation_result)

        # Attach the TUI log handler to the generation screen's log widget
        if self._log_handler:
            # Will be attached once the screen mounts and the widget exists
            self.call_later(self._attach_log_to_gen_screen, gen_screen)

        self.run_worker(self._run_pipeline(gen_screen), exclusive=True)

    def _attach_log_to_gen_screen(self, gen_screen: GenerationScreen) -> None:
        """Attach the log handler to the generation screen's log widget."""
        if self._log_handler:
            try:
                from textual.widgets import Log as LogWidget
                log_widget = gen_screen.query_one("#log-panel", LogWidget)
                self._log_handler.attach(log_widget)
            except Exception:
                pass

    async def _run_pipeline(self, gen_screen: GenerationScreen) -> None:
        from ..analyzer.file_classifier import classify_file
        from ..analyzer.scanner import scan_directory
        from ..generator.index_generator import generate_index_pages
        from ..generator.markdown_writer import write_markdown, write_manual_placeholder
        from ..generator.mkdocs_builder import write_mkdocs_config
        from ..orchestrator.engine import OrchestrationEngine, GenerationResult, PipelineResult
        from ..reporting.report import PipelineReport, FileReport

        gen_screen.log_message("Scanne Quellverzeichnis...")

        scan_result = scan_directory(
            self.config.project.source_dir,
            self.config.project.languages,
            self.config.project.ignore_patterns,
        )
        classified_files = [
            classify_file(sf.path, sf.relative_path, sf.language)
            for sf in scan_result.files
        ]
        gen_screen.log_message(f"Gefunden: {scan_result.total_files} Dateien")

        assignment = self._build_assignment()
        completed_ids = set(self.config.resume.completed_tasks)

        async def failure_cb(model_id: str, error: str) -> str | None:
            if self.auto_mode:
                self._auto_handle_failure(model_id, error)
                return self._find_replacement(model_id)
            else:
                return await self._show_failure_dialog(model_id, error)

        engine = OrchestrationEngine(
            config=self.config,
            assignment=assignment,
            scan_result=scan_result,
            classified_files=classified_files,
            progress_callback=lambda r, p: gen_screen.update_progress(r, p),
            failure_callback=failure_cb,
            disabled_models=self._get_disabled_models(),
            completed_task_ids=completed_ids,
        )

        self.config.resume.generation_started = True
        self._save_config()

        gen_screen.log_message("Starte Generierung...")
        pipeline_result = await engine.run()

        for r in pipeline_result.results:
            if r.success:
                tid = engine.task_id(r.task)
                self.config.resume.completed_tasks.append(tid)

        self.config.resume.generation_finished = True
        self._save_config()

        gen_screen.log_message("Schreibe Ausgabedateien...")

        output_dir = self.config.project.output_dir
        for result in pipeline_result.results:
            if result.success and result.content and result.content != "[resumed - already completed]":
                write_markdown(
                    content=result.content,
                    output_dir=output_dir,
                    stakeholder=result.task.stakeholder,
                    doc_type=result.task.doc_type,
                    name=result.task.file.doc_name,
                )

        generate_index_pages(output_dir, self.config.project.name)
        write_manual_placeholder(output_dir, "index.md", "Manual")
        write_manual_placeholder(output_dir, "changelog.md", "Changelog")
        write_manual_placeholder(output_dir, "contributing.md", "Contributing")
        write_manual_placeholder(output_dir, "faq.md", "FAQ")
        write_mkdocs_config(self.config, output_dir)

        # Detach log handler
        if self._log_handler:
            self._log_handler.detach()

        gen_screen.mark_finished(pipeline_result)

    def _on_generation_result(self, result: dict | None) -> None:
        if result and result.get("interrupted"):
            self._save_config()
        if not self.auto_mode:
            self._start_chat()
        else:
            self._cleanup_and_exit()

    def _start_chat(self) -> None:
        self._update_resume("chat")
        all_models = self._selected_slaves.copy()
        if self._selected_master and self._selected_master not in all_models:
            all_models.insert(0, self._selected_master)
        self.push_screen(
            ChatScreen(self.config, available_models=all_models),
            callback=self._on_chat_result,
        )

    def _on_chat_result(self, result: dict | None) -> None:
        self._cleanup_and_exit()

    def _cleanup_and_exit(self) -> None:
        if self._mkdocs_server:
            self._mkdocs_server.stop()
        self.config.resume.last_screen = ""
        self._save_config()
        self.exit()

    # ── Helpers ───────────────────────────────────────────────────────

    def _apply_model_config(self) -> None:
        from ..config.schema import ModelConfig
        self.config.models.analysts = [
            ModelConfig(id=mid) for mid in self._selected_slaves
        ]
        if self._selected_master:
            self.config.models.judge = ModelConfig(id=self._selected_master)
        else:
            self.config.models.judge = None

        # Persist to preferences
        self.config.preferences.selected_analysts = list(self._selected_slaves)
        self.config.preferences.selected_judge = self._selected_master

    def _build_assignment(self) -> RoleAssignment:
        from ..discovery.model_classifier import ClassifiedModel, classify_model
        analysts = [classify_model(mid) for mid in self._selected_slaves]
        judge = classify_model(self._selected_master) if self._selected_master else None
        return RoleAssignment(analysts=analysts, judge=judge)

    def _build_file_listing(self) -> None:
        try:
            from ..analyzer.scanner import scan_directory
            scan = scan_directory(
                self.config.project.source_dir,
                self.config.project.languages,
                self.config.project.ignore_patterns,
            )
            lines = [str(f.relative_path) for f in scan.files[:50]]
            self._file_listing = "\n".join(lines)
            if scan.total_files > 50:
                self._file_listing += f"\n... und {scan.total_files - 50} weitere Dateien"
        except Exception:
            self._file_listing = "(Verzeichnis nicht lesbar)"

    def _get_disabled_models(self) -> set[str]:
        return {e.model_id for e in self.config.model_health.entries if not e.enabled}

    def _find_replacement(self, failed_model_id: str) -> str | None:
        for e in self.config.model_health.entries:
            if e.model_id == failed_model_id and e.replacement_model_id:
                return e.replacement_model_id
        disabled = self._get_disabled_models()
        disabled.add(failed_model_id)
        for mid in self._selected_slaves:
            if mid not in disabled:
                return mid
        return None

    def _auto_handle_failure(self, model_id: str, error: str) -> None:
        entry = ModelHealthEntry(model_id=model_id, enabled=False, failure_count=1)
        replacement = self._find_replacement(model_id)
        if replacement:
            entry.replacement_model_id = replacement
        found = False
        for i, e in enumerate(self.config.model_health.entries):
            if e.model_id == model_id:
                e.failure_count += 1
                e.enabled = False
                if replacement:
                    e.replacement_model_id = replacement
                found = True
                break
        if not found:
            self.config.model_health.entries.append(entry)
        self._save_config()

    async def _show_failure_dialog(self, model_id: str, error: str) -> str | None:
        future: asyncio.Future = asyncio.get_event_loop().create_future()

        def on_result(result: dict | None):
            if result and not future.done():
                future.set_result(result)
            elif not future.done():
                future.set_result(None)

        self.push_screen(
            FailureScreen(
                config=self.config,
                failed_model_id=model_id,
                error_message=error,
                available_models=self._selected_slaves,
            ),
            callback=on_result,
        )
        result = await future
        if result is None:
            return None
        if result.get("disable"):
            if result.get("persist"):
                self._save_config()
            return result.get("replacement") or None
        return model_id

    def _resume_from(self, screen_name: str) -> None:
        screen_map = {
            "welcome": self._start_welcome,
            "discovery": self._start_discovery,
            "model_selection": self._start_model_selection,
            "skeleton_suggestions": self._start_skeleton_suggestions,
            "skeleton": self._start_skeleton,
            "generation": self._start_generation,
            "chat": self._start_chat,
        }
        starter = screen_map.get(screen_name, self._start_welcome)
        if self.config.preferences.selected_analysts:
            self._selected_slaves = list(self.config.preferences.selected_analysts)
        if self.config.preferences.selected_judge:
            self._selected_master = self.config.preferences.selected_judge
        starter()

def run_tui(config: AppConfig, config_path: Path = Path("config.yaml"), auto: bool = False) -> None:
    """Launch the TUI application."""
    # Redirect ALL logging into our TUI handler BEFORE the app starts.
    # This prevents any logging.info / print from corrupting the terminal.
    log_handler = _redirect_logging_to_tui()

    app = MkDocsTUI(config, config_path=config_path, auto_mode=auto)
    app._log_handler = log_handler
    app.run()
