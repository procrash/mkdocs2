"""Tests for TUI workflow components: skeleton, config persistence, server, resume."""
from __future__ import annotations
import socket
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from src.config.schema import (
    AppConfig,
    AutomationConfig,
    ModelHealthConfig,
    ModelHealthEntry,
    ResumeStateConfig,
    SkeletonConfig,
    SkeletonSuggestionEntry,
    UserPreferencesConfig,
)
from src.config.loader import save_config, load_config
from src.generator.skeleton_builder import (
    create_skeleton,
    create_suggestion_files,
    get_skeleton_tree,
)
from src.generator.mkdocs_server import (
    MkDocsServer,
    find_available_port,
    is_port_available,
)


# ── Config Schema Tests ──────────────────────────────────────────────


class TestConfigSchemaExtensions:
    """Test new config schema models."""

    def test_automation_config_defaults(self):
        cfg = AutomationConfig()
        assert cfg.enabled is False
        assert cfg.auto_start_mkdocs is True
        assert cfg.auto_assign_roles is True

    def test_model_health_entry(self):
        entry = ModelHealthEntry(model_id="test-model")
        assert entry.enabled is True
        assert entry.failure_count == 0
        assert entry.replacement_model_id == ""

    def test_model_health_config(self):
        cfg = ModelHealthConfig(entries=[
            ModelHealthEntry(model_id="m1", enabled=False, failure_count=3),
            ModelHealthEntry(model_id="m2", enabled=True),
        ])
        assert len(cfg.entries) == 2
        assert cfg.entries[0].enabled is False
        assert cfg.entries[1].model_id == "m2"

    def test_skeleton_config_defaults(self):
        cfg = SkeletonConfig()
        assert cfg.create_before_generation is True

    def test_skeleton_suggestion_entry(self):
        entry = SkeletonSuggestionEntry(
            path="getting-started/docker.md",
            title="Docker Setup",
            description="Docker instructions",
            accepted=True,
        )
        assert entry.accepted is True
        assert entry.path == "getting-started/docker.md"

    def test_user_preferences_config_defaults(self):
        cfg = UserPreferencesConfig()
        assert cfg.selected_analysts == []
        assert cfg.selected_judge == ""
        assert cfg.preferred_port == 8000
        assert cfg.language == "de"
        assert cfg.skeleton_suggestions == []

    def test_resume_state_config_defaults(self):
        cfg = ResumeStateConfig()
        assert cfg.last_screen == ""
        assert cfg.completed_tasks == []
        assert cfg.generation_started is False
        assert cfg.generation_finished is False

    def test_app_config_has_new_fields(self):
        cfg = AppConfig()
        assert hasattr(cfg, "automation")
        assert hasattr(cfg, "model_health")
        assert hasattr(cfg, "skeleton")
        assert hasattr(cfg, "preferences")
        assert hasattr(cfg, "resume")
        assert isinstance(cfg.automation, AutomationConfig)
        assert isinstance(cfg.preferences, UserPreferencesConfig)
        assert isinstance(cfg.resume, ResumeStateConfig)


# ── Config Persistence Tests ─────────────────────────────────────────


class TestConfigPersistence:
    """Test that config saves and loads correctly with new fields."""

    def test_save_and_load_with_preferences(self, tmp_path: Path):
        config = AppConfig()
        config.preferences.selected_analysts = ["model-a", "model-b"]
        config.preferences.selected_judge = "model-c"
        config.preferences.preferred_port = 8080
        config.automation.enabled = True
        config.resume.last_screen = "generation"
        config.resume.completed_tasks = ["task1", "task2"]

        config_path = tmp_path / "config.yaml"
        save_config(config, config_path)

        loaded = load_config(config_path)
        assert loaded.preferences.selected_analysts == ["model-a", "model-b"]
        assert loaded.preferences.selected_judge == "model-c"
        assert loaded.preferences.preferred_port == 8080
        assert loaded.automation.enabled is True
        assert loaded.resume.last_screen == "generation"
        assert loaded.resume.completed_tasks == ["task1", "task2"]

    def test_save_and_load_model_health(self, tmp_path: Path):
        config = AppConfig()
        config.model_health.entries = [
            ModelHealthEntry(model_id="m1", enabled=False, failure_count=5, replacement_model_id="m2"),
        ]

        config_path = tmp_path / "config.yaml"
        save_config(config, config_path)

        loaded = load_config(config_path)
        assert len(loaded.model_health.entries) == 1
        assert loaded.model_health.entries[0].model_id == "m1"
        assert loaded.model_health.entries[0].enabled is False
        assert loaded.model_health.entries[0].failure_count == 5

    def test_save_and_load_skeleton_suggestions(self, tmp_path: Path):
        config = AppConfig()
        config.preferences.skeleton_suggestions = [
            SkeletonSuggestionEntry(
                path="arch/security.md", title="Security", description="Sec docs", accepted=True
            ),
            SkeletonSuggestionEntry(
                path="manual/ops.md", title="Operations", accepted=False
            ),
        ]

        config_path = tmp_path / "config.yaml"
        save_config(config, config_path)

        loaded = load_config(config_path)
        assert len(loaded.preferences.skeleton_suggestions) == 2
        assert loaded.preferences.skeleton_suggestions[0].accepted is True
        assert loaded.preferences.skeleton_suggestions[1].accepted is False

    def test_backward_compatible_load(self, tmp_path: Path):
        """Old config without new fields should still load."""
        old_yaml = tmp_path / "config.yaml"
        old_yaml.write_text(
            "project:\n  name: Test\nserver:\n  url: http://localhost:11434\n",
            encoding="utf-8",
        )
        config = load_config(old_yaml)
        assert config.project.name == "Test"
        assert config.automation.enabled is False
        assert config.resume.last_screen == ""


# ── Skeleton Builder Tests ───────────────────────────────────────────


class TestSkeletonBuilder:
    """Test documentation skeleton creation."""

    def test_create_skeleton(self, tmp_path: Path):
        output_dir = tmp_path / "output"
        created = create_skeleton(output_dir, "TestProject")

        assert len(created) > 0
        docs_dir = output_dir / "docs"
        assert (docs_dir / "index.md").exists()
        assert (docs_dir / "getting-started" / "installation.md").exists()
        assert (docs_dir / "getting-started" / "quickstart.md").exists()
        assert (docs_dir / "user-guide" / "overview.md").exists()
        assert (docs_dir / "manual" / "overview.md").exists()
        assert (docs_dir / "formats" / "overview.md").exists()
        assert (docs_dir / "architecture" / "overview.md").exists()
        assert (docs_dir / "api" / "overview.md").exists()
        assert (docs_dir / "generated" / "developer" / "index.md").exists()
        assert (docs_dir / "development" / "contributing.md").exists()
        assert (docs_dir / "operations" / "deployment.md").exists()
        assert (docs_dir / "reference" / "faq.md").exists()

    def test_skeleton_contains_project_name(self, tmp_path: Path):
        output_dir = tmp_path / "output"
        create_skeleton(output_dir, "MeinProjekt")

        index = (output_dir / "docs" / "index.md").read_text(encoding="utf-8")
        assert "MeinProjekt" in index

    def test_skeleton_no_overwrite(self, tmp_path: Path):
        output_dir = tmp_path / "output"
        docs_dir = output_dir / "docs"
        docs_dir.mkdir(parents=True)
        (docs_dir / "index.md").write_text("# Custom\n", encoding="utf-8")

        create_skeleton(output_dir, "Test")
        assert (docs_dir / "index.md").read_text(encoding="utf-8") == "# Custom\n"

    def test_create_suggestion_files(self, tmp_path: Path):
        output_dir = tmp_path / "output"
        suggestions = [
            SkeletonSuggestionEntry(path="extras/docker.md", title="Docker", description="Docker stuff", accepted=True),
            SkeletonSuggestionEntry(path="extras/k8s.md", title="K8s", accepted=False),
        ]
        created = create_suggestion_files(output_dir, suggestions)

        assert len(created) == 1
        assert (output_dir / "docs" / "extras" / "docker.md").exists()
        assert not (output_dir / "docs" / "extras" / "k8s.md").exists()

    def test_get_skeleton_tree(self, tmp_path: Path):
        output_dir = tmp_path / "output"
        create_skeleton(output_dir, "Test")
        tree = get_skeleton_tree(output_dir)

        assert len(tree) > 0
        # Should contain dirs and files
        dir_entries = [name for name, _ in tree if name.endswith("/")]
        file_entries = [name for name, _ in tree if not name.endswith("/")]
        assert len(dir_entries) > 0
        assert len(file_entries) > 0


# ── MkDocs Server Tests ─────────────────────────────────────────────


class TestMkDocsServer:
    """Test MkDocs server management."""

    def test_is_port_available(self):
        # Port 1 should not be available (privileged)
        assert is_port_available(1) is False
        # Very high port should be available (usually)
        result = is_port_available(59999)
        assert isinstance(result, bool)

    def test_find_available_port(self):
        port = find_available_port(50000)
        assert 50000 <= port < 50020

    def test_find_available_port_occupied(self):
        """Test that find_available_port skips occupied ports."""
        # Find a free port first, then occupy it
        base_port = find_available_port(51000)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("0.0.0.0", base_port))
            port = find_available_port(base_port)
            assert port > base_port

    def test_server_init(self, tmp_path: Path):
        server = MkDocsServer(tmp_path, port=8080)
        assert server.port == 8080
        assert server.running is False
        assert server.url == ""

    def test_server_start_no_mkdocs_yml(self, tmp_path: Path):
        server = MkDocsServer(tmp_path)
        with pytest.raises(FileNotFoundError):
            server.start()

    def test_server_stop_when_not_running(self, tmp_path: Path):
        server = MkDocsServer(tmp_path)
        server.stop()  # Should not raise


# ── Resume State Tests ───────────────────────────────────────────────


class TestResumeState:
    """Test resume/checkpoint functionality."""

    def test_resume_state_roundtrip(self, tmp_path: Path):
        config = AppConfig()
        config.resume.last_screen = "generation"
        config.resume.generation_started = True
        config.resume.completed_tasks = ["dev:classes:foo.py:0", "api:endpoints:bar.py:0"]
        config.resume.total_tasks = 10

        config_path = tmp_path / "config.yaml"
        save_config(config, config_path)

        loaded = load_config(config_path)
        assert loaded.resume.last_screen == "generation"
        assert loaded.resume.generation_started is True
        assert len(loaded.resume.completed_tasks) == 2
        assert loaded.resume.total_tasks == 10

    def test_fresh_start_has_empty_resume(self):
        config = AppConfig()
        assert config.resume.last_screen == ""
        assert config.resume.completed_tasks == []
        assert config.resume.generation_started is False
        assert config.resume.generation_finished is False


# ── Skeleton Suggestions Parsing ─────────────────────────────────────


class TestSkeletonSuggestionsParsing:
    """Test LLM suggestion output parsing."""

    def test_parse_valid_suggestions(self):
        from src.ui.tui_screens.skeleton_suggestions_screen import _parse_suggestions
        output = """getting-started/docker.md|Docker-Setup|Anleitung zur Nutzung mit Docker
architecture/security.md|Sicherheitskonzept|Sicherheitsarchitektur und Maßnahmen
manual/troubleshooting.md|Fehlerbehebung|Häufige Probleme und Lösungen"""
        suggestions = _parse_suggestions(output)
        assert len(suggestions) == 3
        assert suggestions[0].path == "getting-started/docker.md"
        assert suggestions[0].title == "Docker-Setup"
        assert suggestions[0].accepted is True

    def test_parse_with_noise(self):
        from src.ui.tui_screens.skeleton_suggestions_screen import _parse_suggestions
        output = """# Vorschläge
Hier sind meine Vorschläge:

getting-started/docker.md|Docker|Docker setup
# Kommentar
invalid line without pipe

manual/ops.md|Operations|Ops guide"""
        suggestions = _parse_suggestions(output)
        assert len(suggestions) == 2

    def test_parse_empty(self):
        from src.ui.tui_screens.skeleton_suggestions_screen import _parse_suggestions
        assert _parse_suggestions("") == []
        assert _parse_suggestions("no pipes here") == []

    def test_default_suggestions(self):
        from src.ui.tui_screens.skeleton_suggestions_screen import _default_suggestions
        suggestions = _default_suggestions()
        assert len(suggestions) > 0
        assert all(s.path for s in suggestions)
        assert all(s.title for s in suggestions)


# ── Engine Task ID and Disabled Models ───────────────────────────────


class TestEngineExtensions:
    """Test engine extensions for resume and failure handling."""

    def test_task_id_generation(self):
        from src.orchestrator.engine import OrchestrationEngine, GenerationTask
        from src.analyzer.file_classifier import ClassifiedFile, FileCategory

        cf = ClassifiedFile(
            path=Path("/tmp/test.py"),
            relative_path=Path("test.py"),
            language="python",
            category=FileCategory.MODULE,
            classes=[],
            functions=[],
        )
        task = GenerationTask(file=cf, stakeholder="developer", doc_type="modules")
        tid = OrchestrationEngine.task_id(task)
        assert tid == "developer:modules:test.py:0"

    def test_disabled_models_filter(self):
        from src.orchestrator.engine import OrchestrationEngine
        from src.discovery.role_assigner import RoleAssignment
        from src.analyzer.scanner import ScanResult

        engine = OrchestrationEngine(
            config=AppConfig(),
            assignment=RoleAssignment(),
            scan_result=ScanResult(total_files=0, files=[], by_language={}),
            classified_files=[],
            disabled_models={"bad-model"},
        )

        active = engine._get_active_analyst_ids(["good-model", "bad-model", "ok-model"])
        assert "bad-model" not in active
        assert "good-model" in active
        assert "ok-model" in active

    def test_disable_model(self):
        from src.orchestrator.engine import OrchestrationEngine
        from src.discovery.role_assigner import RoleAssignment
        from src.analyzer.scanner import ScanResult

        engine = OrchestrationEngine(
            config=AppConfig(),
            assignment=RoleAssignment(),
            scan_result=ScanResult(total_files=0, files=[], by_language={}),
            classified_files=[],
        )
        engine.disable_model("fail-model")
        assert "fail-model" in engine._disabled_models


# ── Diff Review & File Change Parsing ────────────────────────────────


class TestDiffReview:
    """Test file change parsing and diff generation."""

    def test_parse_file_changes_format1(self):
        from src.ui.tui_screens.diff_review_screen import parse_file_changes
        output = """Some preamble text.

<<<FILE src/main.py
DESCRIPTION: Add hello function
>>>
def hello():
    print("Hello")
<<<END>>>

<<<FILE src/utils.py
DESCRIPTION: Add utility
>>>
def util():
    return 42
<<<END>>>

Some trailing text."""
        changes = parse_file_changes(output)
        assert len(changes) == 2
        assert changes[0].file_path == "src/main.py"
        assert changes[0].description == "Add hello function"
        assert "def hello():" in changes[0].new_content
        assert changes[1].file_path == "src/utils.py"

    def test_parse_file_changes_format2(self):
        from src.ui.tui_screens.diff_review_screen import parse_file_changes
        output = """Here is the implementation:

```file:src/hello.py
def hello():
    print("world")
```

```file:src/bye.py
def bye():
    pass
```"""
        changes = parse_file_changes(output)
        assert len(changes) == 2
        assert changes[0].file_path == "src/hello.py"
        assert "def hello():" in changes[0].new_content
        assert changes[1].file_path == "src/bye.py"

    def test_parse_with_base_dir(self):
        from src.ui.tui_screens.diff_review_screen import parse_file_changes
        output = """<<<FILE main.py
>>>
print("hi")
<<<END>>>"""
        changes = parse_file_changes(output, base_dir="/project")
        assert changes[0].file_path == "/project/main.py"

    def test_parse_absolute_path_not_prefixed(self):
        from src.ui.tui_screens.diff_review_screen import parse_file_changes
        output = """<<<FILE /absolute/path.py
>>>
content
<<<END>>>"""
        changes = parse_file_changes(output, base_dir="/project")
        assert changes[0].file_path == "/absolute/path.py"

    def test_parse_empty_output(self):
        from src.ui.tui_screens.diff_review_screen import parse_file_changes
        assert parse_file_changes("") == []
        assert parse_file_changes("no structured content here") == []

    def test_file_change_new_file(self, tmp_path: Path):
        from src.ui.tui_screens.diff_review_screen import FileChange
        fc = FileChange(str(tmp_path / "new.py"), "print('new')\n")
        assert fc.is_new_file is True

    def test_file_change_existing_file(self, tmp_path: Path):
        from src.ui.tui_screens.diff_review_screen import FileChange
        existing = tmp_path / "existing.py"
        existing.write_text("old content\n", encoding="utf-8")
        fc = FileChange(str(existing), "new content\n")
        assert fc.is_new_file is False

    def test_file_change_diff(self, tmp_path: Path):
        from src.ui.tui_screens.diff_review_screen import FileChange
        existing = tmp_path / "test.py"
        existing.write_text("line1\nline2\n", encoding="utf-8")
        fc = FileChange(str(existing), "line1\nline2\nline3\n")
        diff = fc.get_diff()
        assert "+line3" in diff

    def test_file_change_apply(self, tmp_path: Path):
        from src.ui.tui_screens.diff_review_screen import FileChange
        target = tmp_path / "subdir" / "newfile.py"
        fc = FileChange(str(target), "hello = 42\n")
        assert fc.apply() is True
        assert target.exists()
        assert target.read_text(encoding="utf-8") == "hello = 42\n"

    def test_file_change_apply_overwrite(self, tmp_path: Path):
        from src.ui.tui_screens.diff_review_screen import FileChange
        existing = tmp_path / "overwrite.py"
        existing.write_text("old\n", encoding="utf-8")
        fc = FileChange(str(existing), "new\n")
        assert fc.apply() is True
        assert existing.read_text(encoding="utf-8") == "new\n"

    def test_escape_markup(self):
        from src.ui.tui_screens.diff_review_screen import _escape_markup
        assert _escape_markup("no markup") == "no markup"
        assert _escape_markup("[bold]text[/bold]") == "\\[bold\\]text\\[/bold\\]"
