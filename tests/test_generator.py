"""Tests for documentation generator."""
import tempfile
from pathlib import Path

import pytest

from src.generator.markdown_writer import write_markdown, sanitize_filename, _clean_markdown
from src.generator.nav_builder import build_nav, _title_from_filename
from src.generator.index_generator import generate_index_pages


class TestMarkdownWriter:
    def test_sanitize_filename(self):
        assert sanitize_filename("MyClass") == "myclass"
        assert sanitize_filename("my_util_func") == "my-util-func"
        assert sanitize_filename("path/to/File!") == "pathtofile"

    def test_clean_markdown(self):
        content = "```markdown\n# Hello\nWorld\n```"
        cleaned = _clean_markdown(content)
        assert cleaned.startswith("# Hello")
        assert cleaned.endswith("\n")

    def test_write_markdown(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = write_markdown(
                content="# Test\n\nContent here.",
                output_dir=Path(tmpdir),
                stakeholder="developer",
                doc_type="classes",
                name="MyClass",
            )
            assert path.exists()
            assert "myclass.md" in str(path)
            assert path.read_text().startswith("# Test")


class TestNavBuilder:
    def test_title_from_filename(self):
        assert _title_from_filename("my-class") == "My Class"
        assert _title_from_filename("getting_started") == "Getting Started"

    def test_build_nav_empty(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            nav = build_nav(Path(tmpdir))
            assert isinstance(nav, list)

    def test_build_nav_with_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            docs = Path(tmpdir) / "docs"
            docs.mkdir()
            (docs / "index.md").write_text("# Home")
            gen = docs / "generated" / "developer"
            gen.mkdir(parents=True)
            (gen / "architecture.md").write_text("# Arch")

            nav = build_nav(Path(tmpdir))
            assert len(nav) >= 1


class TestIndexGenerator:
    def test_generate_index_pages(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir)
            docs = output / "docs"
            gen = docs / "generated" / "developer" / "classes"
            gen.mkdir(parents=True)
            (gen / "myclass.md").write_text("# MyClass")

            pages = generate_index_pages(output, "TestProject")
            assert len(pages) >= 1
            assert (docs / "index.md").exists()
