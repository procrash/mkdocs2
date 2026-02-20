"""Tests for source code analysis."""
import tempfile
from pathlib import Path

import pytest

from src.analyzer.scanner import scan_directory, LANGUAGE_EXTENSIONS
from src.analyzer.file_classifier import classify_file, FileCategory
from src.analyzer.doxygen_extractor import extract_doxygen_comments, format_doxygen_as_context
from src.analyzer.code_chunker import chunk_code, estimate_tokens


class TestScanner:
    def test_scan_empty_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = scan_directory(Path(tmpdir), ["python"])
            assert result.total_files == 0

    def test_scan_python_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            (Path(tmpdir) / "main.py").write_text("print('hello')")
            (Path(tmpdir) / "utils.py").write_text("def helper(): pass")
            (Path(tmpdir) / "readme.txt").write_text("not python")

            result = scan_directory(Path(tmpdir), ["python"])
            assert result.total_files == 2
            assert result.by_language.get("python") == 2

    def test_scan_with_ignore(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "src").mkdir()
            Path(tmpdir, "build").mkdir()
            (Path(tmpdir) / "src" / "main.py").write_text("code")
            (Path(tmpdir) / "build" / "output.py").write_text("generated")

            result = scan_directory(Path(tmpdir), ["python"], ["build/*"])
            assert result.total_files == 1

    def test_scan_nonexistent_dir(self):
        result = scan_directory(Path("/nonexistent"), ["python"])
        assert result.total_files == 0


class TestFileClassifier:
    def test_classify_class(self):
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write("class MyClass:\n    def method(self):\n        pass\n")
            f.flush()
            result = classify_file(Path(f.name), Path("myclass.py"), "python")
        assert result.category == FileCategory.CLASS_DEF
        assert "MyClass" in result.classes
        Path(f.name).unlink()

    def test_classify_api_endpoint(self):
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write("from flask import Flask\napp = Flask(__name__)\n@app.get('/api')\ndef handler(): pass\n")
            f.flush()
            result = classify_file(Path(f.name), Path("api.py"), "python")
        assert result.category == FileCategory.API_ENDPOINT
        Path(f.name).unlink()

    def test_classify_test(self):
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write("import pytest\ndef test_something():\n    assert True\n")
            f.flush()
            result = classify_file(Path(f.name), Path("test_main.py"), "python")
        assert result.category == FileCategory.TEST
        Path(f.name).unlink()

    def test_classify_header(self):
        with tempfile.NamedTemporaryFile(suffix=".h", mode="w", delete=False) as f:
            f.write("#pragma once\nclass Widget {};\n")
            f.flush()
            result = classify_file(Path(f.name), Path("widget.h"), "cpp")
        assert result.category == FileCategory.HEADER
        Path(f.name).unlink()


class TestDoxygenExtractor:
    def test_extract_block_comment(self):
        code = '''
/** @brief Calculate the sum.
 * @param a First number
 * @param b Second number
 * @return The sum
 */
int sum(int a, int b) { return a + b; }
'''
        comments = extract_doxygen_comments(code)
        assert len(comments) >= 1
        assert comments[0].brief == "Calculate the sum."
        assert len(comments[0].params) == 2
        assert comments[0].returns

    def test_extract_line_comments(self):
        code = '''
/// A simple function
/// @param x Input value
void doSomething(int x);
'''
        comments = extract_doxygen_comments(code)
        assert len(comments) >= 1

    def test_format_as_context(self):
        code = '/** @brief Test. */\nvoid test();'
        comments = extract_doxygen_comments(code)
        ctx = format_doxygen_as_context(comments)
        assert "Test." in ctx

    def test_empty_code(self):
        comments = extract_doxygen_comments("int x = 5;")
        assert len(comments) == 0


class TestCodeChunker:
    def test_small_file_no_chunking(self):
        content = "def hello():\n    print('world')\n"
        chunks = chunk_code(content, "hello.py", "python")
        assert len(chunks) == 1
        assert chunks[0].total_chunks == 1

    def test_large_file_chunking(self):
        # Create a large file
        content = "\n".join([f"def func_{i}():\n    pass\n" for i in range(500)])
        chunks = chunk_code(content, "big.py", "python", max_tokens=200)
        assert len(chunks) > 1
        for chunk in chunks:
            assert chunk.total_chunks == len(chunks)

    def test_token_estimation(self):
        text = "a" * 350
        tokens = estimate_tokens(text)
        assert tokens == 100
