"""Extract Doxygen-style comments from source code."""
from __future__ import annotations
import logging
import re
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class DoxygenComment:
    """A parsed Doxygen comment block."""
    brief: str = ""
    description: str = ""
    params: list[tuple[str, str]] = field(default_factory=list)  # (name, desc)
    returns: str = ""
    notes: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    see_also: list[str] = field(default_factory=list)
    deprecated: str = ""
    raw: str = ""
    line_number: int = 0
    associated_symbol: str = ""


# Block comment: /** ... */
_BLOCK_COMMENT = re.compile(r"/\*\*(.*?)\*/", re.DOTALL)
# Line comments: /// or //!
_LINE_COMMENT = re.compile(r"^[ \t]*(?:///|//!)[ \t]?(.*?)$", re.MULTILINE)

# Doxygen tags
_TAG_BRIEF = re.compile(r"@brief\s+(.*?)(?=@\w|\Z)", re.DOTALL)
_TAG_PARAM = re.compile(r"@param(?:\[(?:in|out|in,out)\])?\s+(\w+)\s+(.*?)(?=@\w|\Z)", re.DOTALL)
_TAG_RETURN = re.compile(r"@returns?\s+(.*?)(?=@\w|\Z)", re.DOTALL)
_TAG_NOTE = re.compile(r"@note\s+(.*?)(?=@\w|\Z)", re.DOTALL)
_TAG_WARNING = re.compile(r"@warning\s+(.*?)(?=@\w|\Z)", re.DOTALL)
_TAG_SEE = re.compile(r"@see\s+(.*?)(?=@\w|\Z)", re.DOTALL)
_TAG_DEPRECATED = re.compile(r"@deprecated\s+(.*?)(?=@\w|\Z)", re.DOTALL)

# Symbol following a comment
_SYMBOL_AFTER = re.compile(
    r"(?:class|struct|enum|void|int|float|double|bool|auto|[\w:*&<>]+)\s+(\w+)",
)


def _clean_comment_text(text: str) -> str:
    """Remove leading asterisks and excessive whitespace from comment text."""
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        line = re.sub(r"^\s*\*\s?", "", line)
        cleaned.append(line)
    return "\n".join(cleaned).strip()


def _parse_comment_block(raw: str) -> DoxygenComment:
    """Parse a single Doxygen comment block."""
    text = _clean_comment_text(raw)
    comment = DoxygenComment(raw=raw)

    # Brief
    brief_match = _TAG_BRIEF.search(text)
    if brief_match:
        comment.brief = brief_match.group(1).strip()
    else:
        # First sentence/line is implicit brief
        first_line = text.split("\n")[0].strip()
        if first_line and not first_line.startswith("@"):
            comment.brief = first_line

    # Parameters
    for match in _TAG_PARAM.finditer(text):
        comment.params.append((match.group(1), match.group(2).strip()))

    # Return
    ret_match = _TAG_RETURN.search(text)
    if ret_match:
        comment.returns = ret_match.group(1).strip()

    # Notes
    for match in _TAG_NOTE.finditer(text):
        comment.notes.append(match.group(1).strip())

    # Warnings
    for match in _TAG_WARNING.finditer(text):
        comment.warnings.append(match.group(1).strip())

    # See also
    for match in _TAG_SEE.finditer(text):
        comment.see_also.append(match.group(1).strip())

    # Deprecated
    dep_match = _TAG_DEPRECATED.search(text)
    if dep_match:
        comment.deprecated = dep_match.group(1).strip()

    # Description: everything not covered by tags
    desc_text = text
    for tag_pattern in [_TAG_BRIEF, _TAG_PARAM, _TAG_RETURN, _TAG_NOTE,
                        _TAG_WARNING, _TAG_SEE, _TAG_DEPRECATED]:
        desc_text = tag_pattern.sub("", desc_text)
    desc_text = desc_text.strip()
    if desc_text and desc_text != comment.brief:
        comment.description = desc_text

    return comment


def extract_doxygen_comments(source_code: str) -> list[DoxygenComment]:
    """Extract all Doxygen comments from source code."""
    comments: list[DoxygenComment] = []

    # Block comments
    for match in _BLOCK_COMMENT.finditer(source_code):
        comment = _parse_comment_block(match.group(1))
        comment.line_number = source_code[:match.start()].count("\n") + 1

        # Try to find the associated symbol
        after = source_code[match.end():match.end() + 200]
        sym_match = _SYMBOL_AFTER.search(after.lstrip())
        if sym_match:
            comment.associated_symbol = sym_match.group(1)
        comments.append(comment)

    # Consecutive line comments (/// or //!)
    lines = source_code.split("\n")
    i = 0
    while i < len(lines):
        line_match = re.match(r"^[ \t]*(?:///|//!)[ \t]?(.*?)$", lines[i])
        if line_match:
            block_lines = [line_match.group(1)]
            start_line = i + 1
            j = i + 1
            while j < len(lines):
                next_match = re.match(r"^[ \t]*(?:///|//!)[ \t]?(.*?)$", lines[j])
                if next_match:
                    block_lines.append(next_match.group(1))
                    j += 1
                else:
                    break
            comment = _parse_comment_block("\n".join(block_lines))
            comment.line_number = start_line
            if j < len(lines):
                sym_match = _SYMBOL_AFTER.search(lines[j])
                if sym_match:
                    comment.associated_symbol = sym_match.group(1)
            comments.append(comment)
            i = j
        else:
            i += 1

    return comments


def format_doxygen_as_context(comments: list[DoxygenComment]) -> str:
    """Format extracted Doxygen comments as context for prompts."""
    if not comments:
        return ""

    sections = ["## Existing Doxygen Documentation\n"]
    for c in comments:
        if c.associated_symbol:
            sections.append(f"### {c.associated_symbol}")
        if c.brief:
            sections.append(f"**Brief**: {c.brief}")
        if c.description:
            sections.append(c.description)
        if c.params:
            sections.append("**Parameters**:")
            for name, desc in c.params:
                sections.append(f"- `{name}`: {desc}")
        if c.returns:
            sections.append(f"**Returns**: {c.returns}")
        if c.notes:
            for note in c.notes:
                sections.append(f"> **Note:** {note}")
        if c.warnings:
            for warn in c.warnings:
                sections.append(f"> **Warning:** {warn}")
        if c.deprecated:
            sections.append(f"> **Deprecated:** {c.deprecated}")
        sections.append("")

    return "\n".join(sections)
