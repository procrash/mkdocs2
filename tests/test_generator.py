"""Tests for documentation generator."""
import tempfile
from pathlib import Path

import pytest

from src.generator.markdown_writer import (
    write_markdown, sanitize_filename, _clean_markdown,
    write_new_page, parse_new_pages, extract_content_without_new_pages,
)
from src.generator.nav_builder import build_nav, _title_from_filename
from src.generator.index_generator import generate_index_pages
from src.generator.skeleton_reader import (
    _extract_guideline, load_all_guidelines, find_matching_page,
    build_skeleton_context,
)
from src.generator.skeleton_builder import DEFAULT_SKELETON


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


class TestWriteNewPage:
    def test_write_new_page(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = write_new_page(
                content="Some new content here.",
                output_dir=Path(tmpdir),
                page_path="tutorials/advanced-caching.md",
                title="Erweitertes Caching",
            )
            assert path.exists()
            text = path.read_text()
            assert text.startswith("# Erweitertes Caching")
            assert "Some new content here." in text

    def test_parse_new_pages(self):
        llm_output = '''Here is existing content.

<<<NEW_PAGE path="tutorials/caching.md" title="Caching Guide">>>
## Einführung
Caching beschleunigt...
<<<END>>>

More text.

<<<NEW_PAGE path="api/websocket.md" title="WebSocket API">>>
## WebSocket-Endpunkte
Verbindungsaufbau...
<<<END>>>
'''
        pages = parse_new_pages(llm_output)
        assert len(pages) == 2
        assert pages[0]["path"] == "tutorials/caching.md"
        assert pages[0]["title"] == "Caching Guide"
        assert "Caching beschleunigt" in pages[0]["content"]
        assert pages[1]["path"] == "api/websocket.md"

    def test_parse_no_new_pages(self):
        pages = parse_new_pages("Regular content without new pages.")
        assert pages == []

    def test_extract_content_without_new_pages(self):
        llm_output = '''Intro text.

<<<NEW_PAGE path="test.md" title="Test">>>
Content
<<<END>>>

Outro text.'''
        cleaned = extract_content_without_new_pages(llm_output)
        assert "Intro text." in cleaned
        assert "Outro text." in cleaned
        assert "<<<NEW_PAGE" not in cleaned


class TestSkeletonReader:
    def test_extract_guideline_basic(self):
        md = '''# Title

!!! tip "Inhaltsrichtlinie"
    **Zielgruppe:** Entwickler

    **Pflicht-Abschnitte:**

    - Abschnitt 1
    - Abschnitt 2

## Nächster Abschnitt
'''
        result = _extract_guideline(md)
        assert "**Zielgruppe:** Entwickler" in result
        assert "Abschnitt 1" in result

    def test_extract_guideline_missing(self):
        md = "# Title\n\nNo guideline here.\n"
        result = _extract_guideline(md)
        assert result == ""

    def test_load_all_guidelines(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            docs = Path(tmpdir) / "docs"
            docs.mkdir()
            (docs / "test.md").write_text(
                '# Test\n\n!!! tip "Inhaltsrichtlinie"\n    **Zielgruppe:** Tester\n\n## Content\n'
            )
            (docs / "no-guide.md").write_text("# No guide\n\nJust content.\n")

            guidelines = load_all_guidelines(docs)
            assert "test.md" in guidelines
            assert "**Zielgruppe:** Tester" in guidelines["test.md"]
            assert "no-guide.md" not in guidelines

    def test_find_matching_page(self):
        guidelines = {
            "getting-started/installation.md": "Installation Anleitung Paketmanager Docker",
            "api/endpoints.md": "REST API Endpunkte HTTP Methoden",
            "user-guide/configuration.md": "Konfiguration YAML Einstellungen",
        }
        result = find_matching_page("installation docker setup", guidelines)
        assert result == "getting-started/installation.md"

    def test_find_matching_page_no_match(self):
        guidelines = {"api/endpoints.md": "REST API"}
        result = find_matching_page("xyz", guidelines)
        assert result is None

    def test_build_skeleton_context(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            docs = Path(tmpdir) / "docs"
            docs.mkdir()
            (docs / "test.md").write_text(
                '# Test\n\n!!! tip "Inhaltsrichtlinie"\n    **Zielgruppe:** Tester\n\n'
            )
            ctx = build_skeleton_context(docs)
            assert "## Seite: test.md" in ctx
            assert "Tester" in ctx


class TestSkeletonBuilderExpanded:
    """Verify the expanded guidelines in DEFAULT_SKELETON."""

    def test_skeleton_has_many_entries(self):
        assert len(DEFAULT_SKELETON) >= 190

    def test_most_entries_have_expanded_guidelines(self):
        expanded = sum(1 for _, _, body in DEFAULT_SKELETON if "**Zielgruppe:**" in body)
        # At least 200 entries should have expanded guidelines
        assert expanded >= 200, f"Only {expanded} entries have expanded guidelines"

    def test_guideline_structure_complete(self):
        """Check that expanded guidelines have all required sections."""
        required_sections = ["**Zielgruppe:**", "**Pflicht-Abschnitte:**", "**Abgrenzung:**"]
        missing = []
        for path, _, body in DEFAULT_SKELETON:
            if "**Zielgruppe:**" not in body:
                continue  # Skip entries without expansion (index.md, abbreviations)
            for section in required_sections:
                if section not in body:
                    missing.append(f"{path} missing {section}")
        assert missing == [], f"Missing sections: {missing[:5]}"

    def test_sample_guideline_quality(self):
        """Spot-check a specific guideline for quality."""
        for path, _, body in DEFAULT_SKELETON:
            if path == "getting-started/installation.md":
                assert "**Zielgruppe:**" in body
                assert "**Pflicht-Abschnitte:**" in body
                assert "**Abgrenzung:**" in body
                break
        else:
            pytest.fail("getting-started/installation.md not found")


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
