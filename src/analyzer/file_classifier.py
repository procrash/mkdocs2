"""Classify source files into documentation-relevant categories."""
from __future__ import annotations
import logging
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class FileCategory(str, Enum):
    CLASS_DEF = "class_definition"
    MODULE = "module"
    HEADER = "header"
    API_ENDPOINT = "api_endpoint"
    CONFIG = "config"
    TEST = "test"
    UTILITY = "utility"
    MAIN = "main_entry"
    UNKNOWN = "unknown"


@dataclass
class ClassifiedFile:
    """A source file with its classified category."""
    path: Path
    relative_path: Path
    language: str
    category: FileCategory
    classes: list[str]
    functions: list[str]
    has_doxygen: bool = False

    @property
    def doc_name(self) -> str:
        """Generate a documentation-friendly name."""
        return self.relative_path.stem.replace("_", "-")


# Regex patterns for classification
_CLASS_PATTERN_CPP = re.compile(r"^\s*class\s+(\w+)", re.MULTILINE)
_CLASS_PATTERN_PY = re.compile(r"^class\s+(\w+)", re.MULTILINE)
_FUNC_PATTERN_CPP = re.compile(
    r"^\s*(?:[\w:*&<>]+\s+)+(\w+)\s*\([^)]*\)\s*(?:const)?\s*(?:\{|;)", re.MULTILINE
)
_FUNC_PATTERN_PY = re.compile(r"^def\s+(\w+)\s*\(", re.MULTILINE)
_API_PATTERNS = re.compile(
    r"(@app\.(get|post|put|delete|patch|route)|@router\.|@api_view|"
    r"CROW_ROUTE|ROUTE_|app\.Get|app\.Post|HandleFunc)",
    re.IGNORECASE,
)
_DOXYGEN_PATTERN = re.compile(r"/\*\*|///|//!")
_MAIN_PATTERN = re.compile(r"(int\s+main\s*\(|if\s+__name__\s*==\s*['\"]__main__['\"])")
_TEST_PATTERN = re.compile(r"(TEST_CASE|TEST_F|BOOST_AUTO_TEST|def\s+test_|class\s+Test\w+|@pytest)")


def classify_file(path: Path, relative_path: Path, language: str) -> ClassifiedFile:
    """Classify a single source file."""
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        logger.warning("Cannot read %s for classification: %s", path, exc)
        return ClassifiedFile(
            path=path, relative_path=relative_path, language=language,
            category=FileCategory.UNKNOWN, classes=[], functions=[],
        )

    # Extract classes and functions
    if language in ("cpp", "c"):
        classes = _CLASS_PATTERN_CPP.findall(content)
        functions = [f for f in _FUNC_PATTERN_CPP.findall(content)
                     if f not in ("if", "for", "while", "switch", "return", "main")]
    else:
        classes = _CLASS_PATTERN_PY.findall(content)
        functions = [f for f in _FUNC_PATTERN_PY.findall(content)
                     if not f.startswith("_")]

    has_doxygen = bool(_DOXYGEN_PATTERN.search(content))

    # Determine category
    category = FileCategory.UNKNOWN

    if _TEST_PATTERN.search(content):
        category = FileCategory.TEST
    elif _MAIN_PATTERN.search(content):
        category = FileCategory.MAIN
    elif _API_PATTERNS.search(content):
        category = FileCategory.API_ENDPOINT
    elif path.suffix.lower() in (".h", ".hpp", ".hxx", ".hh"):
        category = FileCategory.HEADER
    elif classes:
        category = FileCategory.CLASS_DEF
    elif functions:
        if len(functions) > 3:
            category = FileCategory.MODULE
        else:
            category = FileCategory.UTILITY
    elif path.name in ("config.py", "settings.py", "conf.py"):
        category = FileCategory.CONFIG

    return ClassifiedFile(
        path=path,
        relative_path=relative_path,
        language=language,
        category=category,
        classes=classes,
        functions=functions,
        has_doxygen=has_doxygen,
    )
