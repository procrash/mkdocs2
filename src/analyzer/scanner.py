"""Recursively scan source directories for code files."""
from __future__ import annotations
import logging
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path

logger = logging.getLogger(__name__)

# Default file extensions per language
LANGUAGE_EXTENSIONS: dict[str, list[str]] = {
    "cpp": [".cpp", ".cxx", ".cc", ".c", ".h", ".hpp", ".hxx", ".hh"],
    "python": [".py", ".pyi"],
    "java": [".java"],
    "javascript": [".js", ".jsx", ".mjs"],
    "typescript": [".ts", ".tsx"],
    "rust": [".rs"],
    "go": [".go"],
    "csharp": [".cs"],
}


@dataclass
class SourceFile:
    """A discovered source file."""
    path: Path
    relative_path: Path
    language: str
    size_bytes: int
    line_count: int = 0


@dataclass
class ScanResult:
    """Result of a source code scan."""
    files: list[SourceFile] = field(default_factory=list)
    total_files: int = 0
    total_lines: int = 0
    by_language: dict[str, int] = field(default_factory=dict)
    skipped: list[str] = field(default_factory=list)


def scan_directory(
    source_dir: Path,
    languages: list[str],
    ignore_patterns: list[str] | None = None,
) -> ScanResult:
    """Recursively scan a directory for source files."""
    result = ScanResult()
    ignore = ignore_patterns or []

    # Build set of valid extensions
    valid_extensions: dict[str, str] = {}
    for lang in languages:
        for ext in LANGUAGE_EXTENSIONS.get(lang, []):
            valid_extensions[ext] = lang

    if not source_dir.exists():
        logger.error("Source directory does not exist: %s", source_dir)
        return result

    for file_path in sorted(source_dir.rglob("*")):
        if not file_path.is_file():
            continue

        rel_path = file_path.relative_to(source_dir)
        rel_str = str(rel_path)

        # Check ignore patterns
        if any(fnmatch(rel_str, pat) for pat in ignore):
            result.skipped.append(rel_str)
            continue

        ext = file_path.suffix.lower()
        if ext not in valid_extensions:
            continue

        lang = valid_extensions[ext]
        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")
            lines = content.count("\n") + (1 if content and not content.endswith("\n") else 0)
        except Exception as exc:
            logger.warning("Cannot read %s: %s", file_path, exc)
            result.skipped.append(rel_str)
            continue

        sf = SourceFile(
            path=file_path,
            relative_path=rel_path,
            language=lang,
            size_bytes=file_path.stat().st_size,
            line_count=lines,
        )
        result.files.append(sf)
        result.by_language[lang] = result.by_language.get(lang, 0) + 1

    result.total_files = len(result.files)
    result.total_lines = sum(f.line_count for f in result.files)
    logger.info(
        "Scanned %s: %d files, %d lines across %s",
        source_dir, result.total_files, result.total_lines,
        dict(result.by_language),
    )
    return result
