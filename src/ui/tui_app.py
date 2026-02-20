"""Textual-based multi-screen TUI application for mkdocsOnSteroids.

Orchestrates the full workflow: welcome → discovery → model selection →
skeleton suggestions → skeleton → generation → chat.
All user decisions are persisted in config.yaml for resume support.
"""
from __future__ import annotations
import asyncio
import logging
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
        self.auto_mode = auto_mode or config.automation.enabled

        # Runtime state
        self._classified: list[ClassifiedModel] = []
        self._assignment: RoleAssignment = RoleAssignment()
        self._selected_analysts: list[str] = []
        self._selected_judge: str = ""
        self._mkdocs_url: str = ""
        self._mkdocs_server = None
        self._file_listing: str = ""

    def on_mount(self) -> None:
        self.title = "mkdocsOnSteroids"
        self.sub_title = self.config.project.name

        # Check resume state to decide starting screen
        resume = self.config.resume
        if resume.last_screen and not self.auto_mode:
            self._resume_from(resume.last_screen)
        elif self.auto_mode:
            self._start_discovery()
        else:
            self._start_welcome()

    def _save_config(self) -> None:
        """Persist current config to YAML."""
        try:
            save_config(self.config, self.config_path)
        except Exception as exc:
            logger.error("Failed to save config: %s", exc)

    def _update_resume(self, screen_name: str) -> None:
        """Update resume state and persist."""
        self.config.resume.last_screen = screen_name
        self._save_config()

    # ── Screen Flow ──────────────────────────────────────────────────

    def _start_welcome(self) -> None:
        """Screen 1: Welcome & automation mode."""
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
        self._start_discovery()

    def _start_discovery(self) -> None:
        """Screen 2: LLM server probe."""
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

        # Build file listing for suggestions
        self._build_file_listing()

        if self.auto_mode:
            # Auto: use all models, skip selection
            self._selected_analysts = [m.id for m in self._classified]
            self._selected_judge = self._assignment.judge.id if self._assignment.judge else ""
            self._apply_model_config()
            self._start_skeleton()
        else:
            self._start_model_selection()

    def _start_model_selection(self) -> None:
        """Screen 3: Model selection (manual only)."""
        self._update_resume("model_selection")
        self.push_screen(
            ModelSelectionScreen(self.config, self._classified),
            callback=self._on_model_selection_result,
        )

    def _on_model_selection_result(self, result: dict | None) -> None:
        if result is None:
            self._start_discovery()
            return

        self._selected_analysts = result.get("selected_analysts", [])
        self._selected_judge = result.get("selected_judge", "")
        self._apply_model_config()
        self._save_config()
        self._start_skeleton_suggestions()

    def _start_skeleton_suggestions(self) -> None:
        """Screen 4: LLM skeleton suggestions."""
        self._update_resume("skeleton_suggestions")
        self.push_screen(
            SkeletonSuggestionsScreen(
                self.config,
                file_listing=self._file_listing,
                model_ids=self._selected_analysts,
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
        """Screen 5: Skeleton preview & MkDocs start."""
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

        # Create skeleton
        from ..generator.skeleton_builder import create_skeleton, create_suggestion_files
        create_skeleton(self.config.project.output_dir, self.config.project.name)
        create_suggestion_files(self.config.project.output_dir, self.config.preferences.skeleton_suggestions)
        self.config.resume.skeleton_created = True

        # Generate mkdocs.yml for skeleton
        from ..generator.mkdocs_builder import write_mkdocs_config
        write_mkdocs_config(self.config, self.config.project.output_dir)

        # Start MkDocs server
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
        """Screen 6: Generation with live progress."""
        self._update_resume("generation")
        gen_screen = GenerationScreen(self.config, mkdocs_url=self._mkdocs_url)
        self.push_screen(gen_screen, callback=self._on_generation_result)

        # Start pipeline in background
        self.run_worker(self._run_pipeline(gen_screen), exclusive=True)

    async def _run_pipeline(self, gen_screen: GenerationScreen) -> None:
        """Run the documentation generation pipeline."""
        from ..analyzer.file_classifier import classify_file
        from ..analyzer.scanner import scan_directory
        from ..discovery.model_classifier import ClassifiedModel as CM
        from ..discovery.role_assigner import RoleAssignment as RA
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

        # Build assignment from selected models
        assignment = self._build_assignment()

        # Determine completed tasks for resume
        completed_ids = set(self.config.resume.completed_tasks)

        # Create failure callback
        async def failure_cb(model_id: str, error: str) -> str | None:
            if self.auto_mode:
                # Auto: disable and pick replacement
                self._auto_handle_failure(model_id, error)
                return self._find_replacement(model_id)
            else:
                # Manual: show failure dialog
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

        # Track completed tasks for resume
        for r in pipeline_result.results:
            if r.success:
                tid = engine.task_id(r.task)
                self.config.resume.completed_tasks.append(tid)

        self.config.resume.generation_finished = True
        self._save_config()

        gen_screen.log_message("Schreibe Ausgabedateien...")

        # Write outputs
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

        gen_screen.mark_finished(pipeline_result)

    def _on_generation_result(self, result: dict | None) -> None:
        # Stop MkDocs server if it was started
        if result and result.get("interrupted"):
            self._save_config()
        # Offer chat screen
        if not self.auto_mode:
            self._start_chat()
        else:
            self._cleanup_and_exit()

    def _start_chat(self) -> None:
        """Screen 7: Project chat."""
        self._update_resume("chat")
        all_models = self._selected_analysts.copy()
        if self._selected_judge and self._selected_judge not in all_models:
            all_models.insert(0, self._selected_judge)
        self.push_screen(
            ChatScreen(self.config, available_models=all_models),
            callback=self._on_chat_result,
        )

    def _on_chat_result(self, result: dict | None) -> None:
        self._cleanup_and_exit()

    def _cleanup_and_exit(self) -> None:
        """Clean up resources and exit."""
        if self._mkdocs_server:
            self._mkdocs_server.stop()
        # Reset resume state for fresh start next time
        self.config.resume.last_screen = ""
        self._save_config()
        self.exit()

    # ── Helpers ───────────────────────────────────────────────────────

    def _apply_model_config(self) -> None:
        """Apply selected analysts/judge to config.models."""
        from ..config.schema import ModelConfig
        self.config.models.analysts = [
            ModelConfig(id=mid) for mid in self._selected_analysts
        ]
        if self._selected_judge:
            self.config.models.judge = ModelConfig(id=self._selected_judge)
        else:
            self.config.models.judge = None

    def _build_assignment(self) -> RoleAssignment:
        """Build RoleAssignment from selected models."""
        from ..discovery.model_classifier import ClassifiedModel, classify_model
        analysts = [classify_model(mid) for mid in self._selected_analysts]
        judge = classify_model(self._selected_judge) if self._selected_judge else None
        return RoleAssignment(analysts=analysts, judge=judge)

    def _build_file_listing(self) -> None:
        """Build a short file listing for LLM context."""
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
        """Get set of disabled model IDs from health config."""
        return {e.model_id for e in self.config.model_health.entries if not e.enabled}

    def _find_replacement(self, failed_model_id: str) -> str | None:
        """Find a replacement model for a failed one."""
        # Check health config for explicit replacement
        for e in self.config.model_health.entries:
            if e.model_id == failed_model_id and e.replacement_model_id:
                return e.replacement_model_id
        # Pick first available non-disabled analyst
        disabled = self._get_disabled_models()
        disabled.add(failed_model_id)
        for mid in self._selected_analysts:
            if mid not in disabled:
                return mid
        return None

    def _auto_handle_failure(self, model_id: str, error: str) -> None:
        """Automatically handle model failure in automation mode."""
        entry = ModelHealthEntry(
            model_id=model_id, enabled=False, failure_count=1,
        )
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
        logger.info("Auto-disabled model %s, replacement: %s", model_id, replacement or "none")

    async def _show_failure_dialog(self, model_id: str, error: str) -> str | None:
        """Show failure modal and wait for user decision."""
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
                available_models=self._selected_analysts,
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

        # Retry = return same model
        return model_id

    def _resume_from(self, screen_name: str) -> None:
        """Resume from the given screen."""
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

        # Restore runtime state from config
        if self.config.preferences.selected_analysts:
            self._selected_analysts = list(self.config.preferences.selected_analysts)
        if self.config.preferences.selected_judge:
            self._selected_judge = self.config.preferences.selected_judge

        starter()

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark


def run_tui(config: AppConfig, config_path: Path = Path("config.yaml"), auto: bool = False) -> None:
    """Launch the TUI application."""
    app = MkDocsTUI(config, config_path=config_path, auto_mode=auto)
    app.run()
