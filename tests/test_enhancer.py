"""Tests for mkdocs enhancer module."""
import pytest
import yaml
from pathlib import Path

from src.generator.mkdocs_enhancer import (
    AVAILABLE_PLUGINS,
    AVAILABLE_EXTENSIONS,
    get_available_plugins,
    get_available_extensions,
    apply_plugins,
    apply_extensions,
    enhance_mkdocs_config,
    get_pip_requirements,
)


class TestAvailablePlugins:
    def test_get_available_with_empty_config(self):
        config = {"plugins": []}
        avail = get_available_plugins(config)
        assert len(avail) == len(AVAILABLE_PLUGINS)

    def test_get_available_with_existing_plugin(self):
        config = {"plugins": [{"minify": {"minify_html": True}}]}
        avail = get_available_plugins(config)
        names = [p["name"] for p in avail]
        assert "minify" not in names
        assert "glightbox" in names

    def test_get_available_with_string_plugin(self):
        config = {"plugins": ["search", "tags"]}
        avail = get_available_plugins(config)
        # search and tags are not in AVAILABLE_PLUGINS, so all should be available
        assert len(avail) == len(AVAILABLE_PLUGINS)


class TestAvailableExtensions:
    def test_get_available_with_empty_config(self):
        config = {"markdown_extensions": []}
        avail = get_available_extensions(config)
        assert len(avail) == len(AVAILABLE_EXTENSIONS)

    def test_get_available_with_existing_extension(self):
        config = {"markdown_extensions": ["footnotes", "abbr"]}
        avail = get_available_extensions(config)
        names = [e["name"] for e in avail]
        assert "footnotes" not in names
        assert "abbr" not in names
        assert "pymdownx.emoji" in names

    def test_get_available_with_dict_extension(self):
        config = {"markdown_extensions": [{"pymdownx.emoji": {"emoji_index": "test"}}]}
        avail = get_available_extensions(config)
        names = [e["name"] for e in avail]
        assert "pymdownx.emoji" not in names


class TestApplyPlugins:
    def test_apply_all(self):
        config = {"plugins": ["search"]}
        added = apply_plugins(config)
        assert len(added) == len(AVAILABLE_PLUGINS)
        assert len(config["plugins"]) == 1 + len(AVAILABLE_PLUGINS)

    def test_apply_specific(self):
        config = {"plugins": ["search"]}
        added = apply_plugins(config, ["minify", "glightbox"])
        assert added == ["minify", "glightbox"]

    def test_apply_idempotent(self):
        config = {"plugins": ["search"]}
        apply_plugins(config)
        count_after_first = len(config["plugins"])
        apply_plugins(config)
        assert len(config["plugins"]) == count_after_first

    def test_apply_unknown_plugin(self):
        config = {"plugins": []}
        added = apply_plugins(config, ["nonexistent-plugin"])
        assert added == []


class TestApplyExtensions:
    def test_apply_all(self):
        config = {"markdown_extensions": []}
        added = apply_extensions(config)
        assert len(added) == len(AVAILABLE_EXTENSIONS)

    def test_apply_specific(self):
        config = {"markdown_extensions": []}
        added = apply_extensions(config, ["footnotes", "abbr"])
        assert added == ["footnotes", "abbr"]

    def test_apply_idempotent(self):
        config = {"markdown_extensions": []}
        apply_extensions(config)
        count_after_first = len(config["markdown_extensions"])
        apply_extensions(config)
        assert len(config["markdown_extensions"]) == count_after_first


class TestEnhanceMkdocsConfig:
    def test_enhance_nonexistent_file(self, tmp_path):
        result = enhance_mkdocs_config(tmp_path / "missing.yml")
        assert result == {"plugins": [], "extensions": []}

    def test_enhance_adds_plugins_and_extensions(self, tmp_path):
        mkdocs_path = tmp_path / "mkdocs.yml"
        mkdocs_path.write_text(yaml.dump({
            "site_name": "Test",
            "plugins": ["search"],
            "markdown_extensions": ["admonition"],
        }), encoding="utf-8")

        result = enhance_mkdocs_config(mkdocs_path)
        assert len(result["plugins"]) > 0
        assert len(result["extensions"]) > 0

        # Verify the file was updated (read as text, safe_load can't handle !!python/name: tags)
        content = mkdocs_path.read_text(encoding="utf-8")
        assert "minify" in content or "glightbox" in content
        assert "footnotes" in content or "pymdownx.emoji" in content

    def test_enhance_idempotent(self, tmp_path):
        mkdocs_path = tmp_path / "mkdocs.yml"
        mkdocs_path.write_text(yaml.dump({
            "site_name": "Test",
            "plugins": ["search"],
            "markdown_extensions": [],
        }), encoding="utf-8")

        result1 = enhance_mkdocs_config(mkdocs_path)
        result2 = enhance_mkdocs_config(mkdocs_path)
        assert result2 == {"plugins": [], "extensions": []}

    def test_enhance_plugins_only(self, tmp_path):
        mkdocs_path = tmp_path / "mkdocs.yml"
        mkdocs_path.write_text(yaml.dump({
            "site_name": "Test",
            "plugins": [],
            "markdown_extensions": [],
        }), encoding="utf-8")

        result = enhance_mkdocs_config(mkdocs_path, plugins=True, extensions=False)
        assert len(result["plugins"]) > 0
        assert result["extensions"] == []


class TestGetPipRequirements:
    def test_known_plugins(self):
        reqs = get_pip_requirements(["minify", "glightbox"])
        assert "mkdocs-minify-plugin" in reqs
        assert "mkdocs-glightbox" in reqs

    def test_unknown_plugin(self):
        reqs = get_pip_requirements(["nonexistent"])
        assert reqs == []
