"""Tests for the KI-gesteuerte Verbesserung (LLM enhancement) module."""
import asyncio
from pathlib import Path
from unittest.mock import patch

import pytest

from src.generator.llm_enhancer import (
    build_enhancement_prompt,
    run_llm_enhancement,
    run_llm_enhancement_single,
    _select_best_draft,
    _compute_max_tokens,
)
from src.orchestrator.opencode_runner import OpenCodeResult
from src.orchestrator.semaphore import WorkerPool
from src.ui.tui_screens.diff_review_screen import FileChange, parse_file_changes


class _MockHealthEntry:
    """Minimal mock for ModelHealthEntry."""
    def __init__(self, model_id, context_length=0):
        self.model_id = model_id
        self.context_length = context_length


class _MockModelHealth:
    """Minimal mock for model_health config."""
    def __init__(self, entries=None):
        self.entries = entries or []


def _make_mock_config(tmp_path, analysts=None, judge="", health_entries=None):
    """Create a MockConfig with all required fields for llm_enhancer."""
    class MockConfig:
        class server:
            url = "http://localhost:11434"
            api_key = ""
            timeout_read = 60
        class project:
            output_dir = tmp_path
            name = "TestProject"
        class preferences:
            selected_analysts = analysts or ["model-a", "model-b"]
            selected_judge = judge
        model_health = _MockModelHealth(health_entries or [])
    return MockConfig


class TestBuildEnhancementPrompt:
    def test_builds_prompt_with_mkdocs(self, tmp_path):
        mkdocs_path = tmp_path / "mkdocs.yml"
        mkdocs_path.write_text("site_name: Test\n", encoding="utf-8")
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        (docs_dir / "index.md").write_text("# Welcome\nHello world", encoding="utf-8")

        prompt = build_enhancement_prompt(mkdocs_path, docs_dir)
        assert "site_name: Test" in prompt
        assert "index.md" in prompt
        assert "Welcome" in prompt

    def test_handles_missing_mkdocs(self, tmp_path):
        mkdocs_path = tmp_path / "mkdocs.yml"
        docs_dir = tmp_path / "docs"
        prompt = build_enhancement_prompt(mkdocs_path, docs_dir)
        assert "MkDocs" in prompt  # Template content still present
        assert "keine Dateien" in prompt or "Dokumentations-Dateien" in prompt

    def test_truncates_large_files(self, tmp_path):
        mkdocs_path = tmp_path / "mkdocs.yml"
        mkdocs_path.write_text("site_name: Test\n", encoding="utf-8")
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        # Create a file with >30 lines
        lines = [f"Line {i}" for i in range(50)]
        (docs_dir / "big.md").write_text("\n".join(lines), encoding="utf-8")

        prompt = build_enhancement_prompt(mkdocs_path, docs_dir)
        assert "50 Zeilen gesamt" in prompt
        assert "Line 29" in prompt
        assert "Line 40" not in prompt


class TestComputeMaxTokens:
    def test_uses_detected_context(self):
        entries = [_MockHealthEntry("model-a", 32768)]
        config = type("C", (), {"model_health": _MockModelHealth(entries)})
        result = _compute_max_tokens(config, ["model-a"], 1000)
        assert result >= 4096
        assert result <= 32768

    def test_uses_minimum_across_models(self):
        entries = [
            _MockHealthEntry("model-a", 32768),
            _MockHealthEntry("model-b", 8192),
        ]
        config = type("C", (), {"model_health": _MockModelHealth(entries)})
        result = _compute_max_tokens(config, ["model-a", "model-b"], 1000)
        assert result <= 8192

    def test_fallback_when_no_context_info(self):
        config = type("C", (), {"model_health": _MockModelHealth([])})
        result = _compute_max_tokens(config, ["model-a"], 1000)
        assert result == 16384  # default

    def test_minimum_4096(self):
        entries = [_MockHealthEntry("model-a", 5000)]
        config = type("C", (), {"model_health": _MockModelHealth(entries)})
        result = _compute_max_tokens(config, ["model-a"], 4000)
        assert result >= 4096


class TestSelectBestDraft:
    def test_prefers_structured_output(self):
        drafts = [
            OpenCodeResult(success=True, output="Short answer.", model_id="a"),
            OpenCodeResult(
                success=True,
                output=(
                    "<<<FILE docs/index.md\nDESCRIPTION: Verbesserte Startseite\n>>>\n"
                    "# Startseite\nInhalt\n<<<END>>>\n"
                    "<<<FILE docs/guide.md\nDESCRIPTION: Neue Anleitung\n>>>\n"
                    "# Anleitung\nDetails\n<<<END>>>"
                ),
                model_id="b",
            ),
        ]
        best = _select_best_draft(drafts)
        assert "<<<FILE" in best
        assert "Startseite" in best

    def test_handles_single_draft(self):
        drafts = [
            OpenCodeResult(success=True, output="Only one.", model_id="a"),
        ]
        best = _select_best_draft(drafts)
        assert best == "Only one."


class TestParseFileChanges:
    def test_parses_file_format(self):
        output = (
            "<<<FILE docs/index.md\n"
            "DESCRIPTION: Verbesserte Startseite\n"
            ">>>\n"
            "# Willkommen\nNeuer Inhalt\n"
            "<<<END>>>"
        )
        changes = parse_file_changes(output)
        assert len(changes) == 1
        assert changes[0].file_path == "docs/index.md"
        assert changes[0].description == "Verbesserte Startseite"
        assert "Willkommen" in changes[0].new_content

    def test_parses_multiple_files(self):
        output = (
            "<<<FILE docs/a.md\nDESCRIPTION: File A\n>>>\nContent A\n<<<END>>>\n"
            "<<<FILE docs/b.md\nDESCRIPTION: File B\n>>>\nContent B\n<<<END>>>"
        )
        changes = parse_file_changes(output)
        assert len(changes) == 2

    def test_applies_base_dir(self):
        output = "<<<FILE docs/test.md\n>>>\nContent\n<<<END>>>"
        changes = parse_file_changes(output, base_dir="/project")
        assert changes[0].file_path == "/project/docs/test.md"

    def test_empty_output(self):
        changes = parse_file_changes("")
        assert changes == []


class TestRunLlmEnhancement:
    def test_mock_mode_ensemble(self, tmp_path):
        """Test that ensemble works with mock mode (no real LLM)."""
        config = _make_mock_config(tmp_path, ["model-a", "model-b"], "model-judge")

        mkdocs_path = tmp_path / "mkdocs.yml"
        mkdocs_path.write_text("site_name: TestProject\n", encoding="utf-8")
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        (docs_dir / "index.md").write_text("# Test\nHello", encoding="utf-8")

        async def _test():
            pool = WorkerPool(max_workers=3)
            changes = await run_llm_enhancement(
                config=config,
                slaves=["model-a", "model-b"],
                master="model-judge",
                pool=pool,
                mock_mode=True,
            )
            assert isinstance(changes, list)

        asyncio.run(_test())

    def test_single_model_mock(self, tmp_path):
        """Test single model enhancement with mock mode."""
        config = _make_mock_config(tmp_path)

        mkdocs_path = tmp_path / "mkdocs.yml"
        mkdocs_path.write_text("site_name: TestProject\n", encoding="utf-8")
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        (docs_dir / "index.md").write_text("# Test", encoding="utf-8")

        async def _test():
            pool = WorkerPool(max_workers=1)
            changes = await run_llm_enhancement_single(
                config=config,
                model_id="test-model",
                pool=pool,
                mock_mode=True,
            )
            assert isinstance(changes, list)

        asyncio.run(_test())

    def test_progress_callback_called(self, tmp_path):
        """Test that progress callback is invoked."""
        config = _make_mock_config(tmp_path)

        mkdocs_path = tmp_path / "mkdocs.yml"
        mkdocs_path.write_text("site_name: Test\n", encoding="utf-8")
        (tmp_path / "docs").mkdir()

        progress_calls = []

        def on_progress(completed, total, model_id, status):
            progress_calls.append((completed, total, model_id, status))

        async def _test():
            pool = WorkerPool(max_workers=3)
            await run_llm_enhancement(
                config=config,
                slaves=["model-a"],
                master="",
                pool=pool,
                progress_cb=on_progress,
                mock_mode=True,
            )

        asyncio.run(_test())
        assert len(progress_calls) >= 2  # At least start + finish

    def test_no_master_uses_best_draft(self, tmp_path):
        """Without master, selects best draft heuristically."""
        config = _make_mock_config(tmp_path)

        mkdocs_path = tmp_path / "mkdocs.yml"
        mkdocs_path.write_text("site_name: Test\n", encoding="utf-8")
        (tmp_path / "docs").mkdir()

        async def _test():
            pool = WorkerPool(max_workers=3)
            changes = await run_llm_enhancement(
                config=config,
                slaves=["model-a", "model-b"],
                master="",
                pool=pool,
                mock_mode=True,
            )
            assert isinstance(changes, list)

        asyncio.run(_test())

    def test_uses_detected_context_for_max_tokens(self, tmp_path):
        """When models have detected context lengths, uses them."""
        entries = [
            _MockHealthEntry("model-a", 32768),
            _MockHealthEntry("model-b", 16384),
        ]
        config = _make_mock_config(tmp_path, health_entries=entries)

        mkdocs_path = tmp_path / "mkdocs.yml"
        mkdocs_path.write_text("site_name: Test\n", encoding="utf-8")
        (tmp_path / "docs").mkdir()

        async def _test():
            pool = WorkerPool(max_workers=3)
            changes = await run_llm_enhancement(
                config=config,
                slaves=["model-a", "model-b"],
                master="",
                pool=pool,
                mock_mode=True,
            )
            assert isinstance(changes, list)

        asyncio.run(_test())


class TestFileChange:
    def test_new_file_detection(self):
        change = FileChange("/nonexistent/path/test.md", "content")
        assert change.is_new_file is True

    def test_apply_creates_file(self, tmp_path):
        file_path = tmp_path / "new_file.md"
        change = FileChange(str(file_path), "# New Content\nHello")
        assert change.apply() is True
        assert file_path.read_text(encoding="utf-8") == "# New Content\nHello"

    def test_apply_creates_directories(self, tmp_path):
        file_path = tmp_path / "sub" / "dir" / "file.md"
        change = FileChange(str(file_path), "Content")
        assert change.apply() is True
        assert file_path.exists()
