"""Tests for prompt system."""
import pytest

from src.prompts.registry import ensure_loaded, get_template, list_templates
from src.prompts.builder import build_prompt, PromptContext


class TestRegistry:
    def test_templates_registered(self):
        ensure_loaded()
        templates = list_templates()
        assert len(templates) > 0
        assert ("developer", "classes") in templates
        assert ("api", "endpoints") in templates
        assert ("user", "features") in templates
        assert ("judge", "merge") in templates

    def test_get_template(self):
        ensure_loaded()
        fn = get_template("developer", "classes")
        assert fn is not None
        assert callable(fn)

    def test_get_nonexistent_template(self):
        ensure_loaded()
        fn = get_template("nonexistent", "nope")
        assert fn is None


class TestBuilder:
    def test_build_developer_class_prompt(self):
        ctx = PromptContext(
            code_content="class Foo:\n    pass",
            file_path="foo.py",
            language="python",
        )
        prompt = build_prompt("developer", "classes", ctx)
        assert prompt is not None
        assert "Foo" in prompt
        assert "python" in prompt

    def test_build_api_endpoint_prompt(self):
        ctx = PromptContext(
            code_content="@app.get('/api')\ndef handler(): pass",
            file_path="api.py",
            language="python",
        )
        prompt = build_prompt("api", "endpoints", ctx)
        assert prompt is not None
        assert "Endpunkt" in prompt or "API" in prompt

    def test_build_judge_prompt(self):
        ctx = PromptContext(
            n_drafts=2,
            drafts_section="Draft 1\n---\nDraft 2",
            context="test.py",
            stakeholder="developer",
        )
        prompt = build_prompt("judge", "merge", ctx)
        assert prompt is not None
        assert "2" in prompt

    def test_build_nonexistent(self):
        ctx = PromptContext()
        result = build_prompt("nonexistent", "nope", ctx)
        assert result is None

    def test_prompt_context_has_skeleton_fields(self):
        ctx = PromptContext()
        assert hasattr(ctx, "skeleton_guidelines")
        assert hasattr(ctx, "skeleton_page_map")
        assert hasattr(ctx, "target_page_path")
        assert ctx.skeleton_guidelines == ""
        assert ctx.skeleton_page_map == ""
        assert ctx.target_page_path == ""

    def test_guideline_injected_into_developer_class_prompt(self):
        ctx = PromptContext(
            code_content="class Bar:\n    pass",
            file_path="bar.py",
            language="python",
            skeleton_guidelines="**Zielgruppe:** Entwickler\n**Pflicht-Abschnitte:**\n- API-Doku",
            target_page_path="generated/developer/classes/bar.md",
        )
        prompt = build_prompt("developer", "classes", ctx)
        assert prompt is not None
        assert "Inhaltsrichtlinie" in prompt
        assert "**Zielgruppe:** Entwickler" in prompt
        assert "generated/developer/classes/bar.md" in prompt

    def test_guideline_injected_into_api_endpoint_prompt(self):
        ctx = PromptContext(
            code_content="@router.get('/users')\ndef get_users(): pass",
            file_path="routes.py",
            language="python",
            skeleton_guidelines="**Zielgruppe:** API-Entwickler",
            target_page_path="api/endpoints.md",
        )
        prompt = build_prompt("api", "endpoints", ctx)
        assert prompt is not None
        assert "**Zielgruppe:** API-Entwickler" in prompt

    def test_no_guideline_no_injection(self):
        ctx = PromptContext(
            code_content="class Baz:\n    pass",
            file_path="baz.py",
            language="python",
        )
        prompt = build_prompt("developer", "classes", ctx)
        assert prompt is not None
        assert "Inhaltsrichtlinie der Zielseite" not in prompt
