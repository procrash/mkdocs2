"""Split large source files into manageable chunks for LLM processing."""
from __future__ import annotations
import logging
import re
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Approximate tokens per character ratio
CHARS_PER_TOKEN = 3.5


@dataclass
class CodeChunk:
    """A chunk of source code."""
    content: str
    start_line: int
    end_line: int
    chunk_index: int
    total_chunks: int
    context_header: str  # File info and chunk position
    symbol_name: str = ""  # Class or function name if applicable


def estimate_tokens(text: str) -> int:
    """Estimate token count for text."""
    return int(len(text) / CHARS_PER_TOKEN)


def chunk_code(
    content: str,
    file_path: str,
    language: str,
    max_tokens: int = 8000,
    overlap_lines: int = 5,
) -> list[CodeChunk]:
    """Split source code into chunks respecting logical boundaries.

    Strategy:
    1. If the file fits in max_tokens, return as single chunk.
    2. Otherwise, split at class/function boundaries.
    3. If a single class/function exceeds max_tokens, split at method boundaries.
    """
    if estimate_tokens(content) <= max_tokens:
        return [CodeChunk(
            content=content,
            start_line=1,
            end_line=content.count("\n") + 1,
            chunk_index=0,
            total_chunks=1,
            context_header=f"File: {file_path} (complete)",
        )]

    # Find logical split points
    split_points = _find_split_points(content, language)

    if not split_points:
        # Fallback: split by line count
        return _split_by_lines(content, file_path, max_tokens, overlap_lines)

    return _split_at_boundaries(content, file_path, split_points, max_tokens, overlap_lines)


def _find_split_points(content: str, language: str) -> list[tuple[int, str]]:
    """Find logical split points (class/function definitions) with their line numbers."""
    points: list[tuple[int, str]] = []
    lines = content.split("\n")

    if language in ("cpp", "c"):
        pattern = re.compile(r"^(?:class|struct|namespace|void|int|float|double|bool|auto|[\w:*&<>]+\s+)\s*(\w+)")
    else:
        pattern = re.compile(r"^(?:class|def|async\s+def)\s+(\w+)")

    for i, line in enumerate(lines):
        match = pattern.match(line.strip())
        if match:
            points.append((i, match.group(1)))

    return points


def _split_by_lines(
    content: str, file_path: str, max_tokens: int, overlap: int
) -> list[CodeChunk]:
    """Fallback: split by line count."""
    lines = content.split("\n")
    max_chars = int(max_tokens * CHARS_PER_TOKEN)
    chunks: list[CodeChunk] = []

    current_start = 0
    while current_start < len(lines):
        # Find how many lines fit
        current_chars = 0
        end = current_start
        while end < len(lines) and current_chars + len(lines[end]) < max_chars:
            current_chars += len(lines[end]) + 1
            end += 1
        if end == current_start:
            end = current_start + 1  # At least one line

        chunk_lines = lines[current_start:end]
        chunks.append(CodeChunk(
            content="\n".join(chunk_lines),
            start_line=current_start + 1,
            end_line=end,
            chunk_index=len(chunks),
            total_chunks=0,  # Updated later
            context_header=f"File: {file_path} (lines {current_start + 1}-{end})",
        ))
        current_start = max(current_start + 1, end - overlap)

    for c in chunks:
        c.total_chunks = len(chunks)
    return chunks


def _split_at_boundaries(
    content: str,
    file_path: str,
    split_points: list[tuple[int, str]],
    max_tokens: int,
    overlap: int,
) -> list[CodeChunk]:
    """Split at class/function boundaries."""
    lines = content.split("\n")
    chunks: list[CodeChunk] = []

    # Add end-of-file as final point
    boundaries = [p[0] for p in split_points] + [len(lines)]
    names = [p[1] for p in split_points] + [""]

    i = 0
    while i < len(boundaries) - 1:
        start = boundaries[i]
        symbol = names[i]

        # Accumulate sections until we hit max_tokens
        end = boundaries[i + 1]
        j = i + 1
        while j < len(boundaries) - 1:
            candidate_end = boundaries[j + 1]
            section = "\n".join(lines[start:candidate_end])
            if estimate_tokens(section) > max_tokens:
                break
            end = candidate_end
            j += 1

        chunk_content = "\n".join(lines[start:end])

        # If single section is too large, fall back to line splitting
        if estimate_tokens(chunk_content) > max_tokens and end - start > 10:
            sub_chunks = _split_by_lines(chunk_content, file_path, max_tokens, overlap)
            for sc in sub_chunks:
                sc.start_line += start
                sc.end_line += start
                sc.symbol_name = symbol
            chunks.extend(sub_chunks)
        else:
            chunks.append(CodeChunk(
                content=chunk_content,
                start_line=start + 1,
                end_line=end,
                chunk_index=len(chunks),
                total_chunks=0,
                context_header=f"File: {file_path} ({symbol or 'section'}, lines {start + 1}-{end})",
                symbol_name=symbol,
            ))

        i = j

    for idx, c in enumerate(chunks):
        c.chunk_index = idx
        c.total_chunks = len(chunks)

    return chunks
