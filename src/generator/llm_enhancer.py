"""KI-gesteuerte Verbesserung: Ensemble-Analyse der Dokumentation.

All slave models analyze the current mkdocs.yml + skeleton files and propose
improvements. The master model synthesizes the best proposals into concrete
changes that the user can accept/reject via DiffReviewScreen.
"""
from __future__ import annotations

import logging
from collections.abc import Callable
from pathlib import Path
from typing import Optional

from ..orchestrator.ensemble import query_ensemble
from ..orchestrator.judge import judge_drafts
from ..orchestrator.opencode_runner import OpenCodeResult, configure_http_fallback, run_opencode
from ..orchestrator.semaphore import WorkerPool
from ..prompts.builder import PromptContext, build_prompt
from ..prompts.registry import ensure_loaded
from ..ui.tui_screens.diff_review_screen import FileChange, parse_file_changes

logger = logging.getLogger(__name__)

# Type for progress callback: (completed: int, total: int, model_id: str, status: str) -> None
ProgressCallback = Optional[Callable[[int, int, str, str], None]]

# Fallback max_tokens when no context length info available
_DEFAULT_MAX_TOKENS = 16384


def _compute_max_tokens(config, model_ids: list[str], prompt_chars: int) -> int:
    """Compute max_tokens from detected context window sizes.

    Uses the minimum detected context length across all models, reserves
    space for the prompt, and uses up to 50% of remaining context for output.
    Falls back to _DEFAULT_MAX_TOKENS if no context info is available.
    """
    detected = []
    for entry in config.model_health.entries:
        if entry.model_id in model_ids and entry.context_length > 0:
            detected.append(entry.context_length)

    if not detected:
        logger.info("No detected context lengths, using default max_tokens=%d", _DEFAULT_MAX_TOKENS)
        return _DEFAULT_MAX_TOKENS

    min_context = min(detected)
    # Rough estimate: 1 token ≈ 3.5 chars
    prompt_tokens = int(prompt_chars / 3.5)
    available = max(min_context - prompt_tokens, min_context // 2)
    # Use up to 50% of available context for output, capped at reasonable range
    max_tokens = max(4096, min(available, min_context // 2))
    logger.info(
        "Context windows: %s, min=%d, prompt≈%d tokens → max_tokens=%d",
        {m: c for m, c in zip(model_ids, detected)},
        min_context, prompt_tokens, max_tokens,
    )
    return max_tokens


def build_enhancement_prompt(mkdocs_path: Path, docs_dir: Path, project_name: str = "") -> str:
    """Build the analysis prompt from mkdocs.yml and documentation files.

    Reads the full mkdocs.yml and collects all .md files with path + first 30 lines.
    Returns the complete prompt string.
    """
    # Read mkdocs.yml
    mkdocs_content = ""
    if mkdocs_path.exists():
        try:
            mkdocs_content = mkdocs_path.read_text(encoding="utf-8")
        except Exception as exc:
            logger.warning("Could not read mkdocs.yml: %s", exc)

    # Collect .md files with previews
    file_listing_parts: list[str] = []
    md_count = 0
    if docs_dir.exists():
        for md_file in sorted(docs_dir.rglob("*.md")):
            md_count += 1
            rel_path = md_file.relative_to(docs_dir.parent)
            try:
                lines = md_file.read_text(encoding="utf-8").splitlines()
                preview = "\n".join(lines[:30])
                if len(lines) > 30:
                    preview += f"\n... ({len(lines)} Zeilen gesamt)"
                file_listing_parts.append(f"### {rel_path}\n```markdown\n{preview}\n```")
            except Exception:
                file_listing_parts.append(f"### {rel_path}\n(nicht lesbar)")

    file_listing = "\n\n".join(file_listing_parts) if file_listing_parts else "(keine Dateien gefunden)"
    logger.info("Enhancement context: mkdocs.yml + %d .md files from docs/", md_count)

    # Use registered template
    ensure_loaded()
    ctx = PromptContext(
        code_content=mkdocs_content,
        file_listing=file_listing,
        section_name=project_name,
    )
    prompt = build_prompt("enhance", "analysis", ctx)
    if prompt:
        return prompt

    # Fallback: build directly if template not found
    logger.warning("enhance/analysis template not found, using inline fallback")
    pname = project_name or "das Projekt"
    return f"""Du bist ein erfahrener MkDocs-Experte und Technical Writer.

## Projekt: {pname}

## Aktuelle mkdocs.yml:
```yaml
{mkdocs_content}
```

## Vorhandene Dokumentations-Dateien:
{file_listing}

## Deine Aufgabe:
Analysiere den nav:-Abschnitt der mkdocs.yml.
Identifiziere fehlende Abschnitte die eine vollständige Dokumentation haben sollte.
Für jeden fehlenden Abschnitt:
1. Füge ihn in die nav:-Hierarchie der mkdocs.yml ein
2. Erstelle die Markdown-Datei mit Inhaltsbeschreibung

## Ausgabeformat (STRIKT einhalten):
<<<FILE mkdocs.yml
DESCRIPTION: Navigation ergänzt
>>>
komplette mkdocs.yml
<<<END>>>

<<<FILE docs/pfad/neue_seite.md
DESCRIPTION: Was diese Seite abdeckt
>>>
Markdown-Inhalt
<<<END>>>

Alle Texte auf Deutsch."""


def build_format_analysis_prompt(
    source_dir: Path,
    mkdocs_path: Path,
    project_name: str = "",
    max_source_chars: int = 80000,
) -> str:
    """Build a prompt for file format analysis from source code.

    Reads source code files (.py, .js, .ts, .java, .go, .rs, .c, .cpp, .rb, etc.)
    and the mkdocs.yml, then uses the enhance/formats template.
    """
    # Collect source files
    source_extensions = {
        ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rs",
        ".c", ".cpp", ".h", ".hpp", ".rb", ".php", ".cs", ".swift",
        ".kt", ".scala", ".sh", ".bash", ".toml", ".ini", ".cfg",
    }
    source_parts: list[str] = []
    total_chars = 0

    if source_dir.exists():
        for src_file in sorted(source_dir.rglob("*")):
            if not src_file.is_file():
                continue
            if src_file.suffix.lower() not in source_extensions:
                continue
            # Skip test files, virtualenvs, node_modules
            rel = str(src_file.relative_to(source_dir))
            if any(skip in rel for skip in [
                "node_modules", ".venv", "__pycache__", ".git",
                "dist/", "build/", ".egg-info",
            ]):
                continue
            try:
                content = src_file.read_text(encoding="utf-8", errors="replace")
                # Truncate very large files
                if len(content) > 5000:
                    content = content[:5000] + f"\n... (gekürzt, {len(content)} Zeichen gesamt)"
                entry = f"### {rel}\n```{src_file.suffix.lstrip('.')}\n{content}\n```"
                if total_chars + len(entry) > max_source_chars:
                    source_parts.append(f"\n... (weitere Dateien weggelassen, Limit erreicht)")
                    break
                source_parts.append(entry)
                total_chars += len(entry)
            except Exception:
                continue

    code_content = "\n\n".join(source_parts) if source_parts else "(kein Quellcode gefunden)"
    logger.info("Format analysis context: %d source files, %d chars", len(source_parts), total_chars)

    # Read mkdocs.yml for context
    mkdocs_content = ""
    if mkdocs_path.exists():
        try:
            mkdocs_content = mkdocs_path.read_text(encoding="utf-8")
        except Exception:
            pass

    ensure_loaded()
    ctx = PromptContext(
        code_content=code_content,
        file_listing=mkdocs_content,
        section_name=project_name,
    )
    prompt = build_prompt("enhance", "formats", ctx)
    if prompt:
        return prompt

    logger.warning("enhance/formats template not found")
    return ""


async def run_format_analysis(
    config,
    slaves: list[str],
    master: str,
    pool: WorkerPool,
    source_dir: Path | None = None,
    progress_cb: ProgressCallback = None,
    mock_mode: bool = False,
) -> list[FileChange]:
    """Run format analysis on source code to generate format documentation.

    Similar to run_llm_enhancement but uses a different prompt focused on
    analyzing file formats in the source code.
    """
    configure_http_fallback(
        server_url=config.server.url,
        api_key=config.server.api_key,
        timeout_read=config.server.timeout_read,
    )

    output_dir = config.project.output_dir
    mkdocs_path = output_dir / "mkdocs.yml"

    # Use project source dir or fall back to src/ in project root
    if source_dir is None:
        source_dir = config.project.source_dir

    prompt = build_format_analysis_prompt(
        source_dir=source_dir,
        mkdocs_path=mkdocs_path,
        project_name=config.project.name,
    )
    if not prompt:
        logger.error("Could not build format analysis prompt")
        return []

    logger.info("Format analysis prompt: %d chars", len(prompt))
    max_tokens = _compute_max_tokens(config, slaves, len(prompt))

    if progress_cb:
        progress_cb(0, len(slaves), "", f"Formatanalyse-Prompt erstellt ({max_tokens} max tokens)")

    # Query ensemble
    ensemble_result = await query_ensemble(
        prompt=prompt,
        model_ids=slaves,
        pool=pool,
        timeout=180,
        max_retries=2,
        retry_delay=3,
        mock_mode=mock_mode,
        max_tokens=max_tokens,
    )

    if progress_cb:
        progress_cb(
            len(ensemble_result.successful_drafts),
            len(slaves),
            "",
            f"{len(ensemble_result.successful_drafts)}/{len(slaves)} Modelle erfolgreich",
        )

    if not ensemble_result.successful_drafts:
        logger.error("No successful drafts from format analysis ensemble")
        return []

    # Debug output
    debug_dir = output_dir / "_enhance_debug"
    debug_dir.mkdir(exist_ok=True)
    try:
        (debug_dir / "00_format_prompt.txt").write_text(prompt, encoding="utf-8")
    except Exception:
        pass
    for i, draft in enumerate(ensemble_result.successful_drafts):
        safe_name = draft.model_id.replace("/", "_").replace(":", "_")
        try:
            (debug_dir / f"01_format_draft_{i}_{safe_name}.txt").write_text(
                draft.output, encoding="utf-8"
            )
        except Exception:
            pass

    # Merge or select
    if master and len(ensemble_result.successful_drafts) > 1:
        if progress_cb:
            progress_cb(
                len(ensemble_result.successful_drafts), len(slaves),
                master, f"Master-Modell {master} synthetisiert...",
            )
        merged = await judge_drafts(
            drafts=ensemble_result.successful_drafts,
            context_description="dateiformat-analyse",
            stakeholder="developer",
            judge_model_id=master,
            pool=pool,
            timeout=240,
            mock_mode=mock_mode,
        )
    else:
        if len(ensemble_result.successful_drafts) == 1:
            merged = ensemble_result.successful_drafts[0].output
        else:
            merged = _select_best_draft(ensemble_result.successful_drafts)

    # Debug merged
    try:
        (debug_dir / "02_format_merged.txt").write_text(merged, encoding="utf-8")
    except Exception:
        pass

    base_dir = str(output_dir)
    changes = parse_file_changes(merged, base_dir=base_dir)
    logger.info("Format analysis: parsed %d file changes", len(changes))
    return changes


def _select_best_draft(drafts: list[OpenCodeResult]) -> str:
    """Select the best draft using heuristics (for when no master is available).

    Prefers: more <<<FILE blocks, longer output, more structure elements.
    """
    def score(draft: OpenCodeResult) -> float:
        text = draft.output
        s = len(text) * 0.001
        s += text.count("<<<FILE") * 20
        s += text.count("<<<END>>>") * 20
        s += text.count("##") * 3
        s += text.count("```") * 2
        return s

    best = max(drafts, key=score)
    logger.info("Selected best draft from %s (score: %.1f)", best.model_id, score(best))
    return best.output


async def run_llm_enhancement(
    config,
    slaves: list[str],
    master: str,
    pool: WorkerPool,
    progress_cb: ProgressCallback = None,
    mock_mode: bool = False,
) -> list[FileChange]:
    """Run the full ensemble enhancement pipeline.

    1. Build the analysis prompt from current mkdocs.yml + docs
    2. Query all slave models in parallel
    3. If master is set and >1 successful drafts: judge_drafts to merge
    4. If no master: pick best draft heuristically
    5. Parse result into FileChange list

    Args:
        config: AppConfig instance
        slaves: List of slave model IDs
        master: Master/judge model ID (empty string if none)
        pool: WorkerPool for concurrency control
        progress_cb: Optional callback (completed, total, model_id, status)
        mock_mode: Use mock responses for testing

    Returns:
        List of FileChange objects ready for DiffReviewScreen
    """
    # Configure HTTP fallback
    configure_http_fallback(
        server_url=config.server.url,
        api_key=config.server.api_key,
        timeout_read=config.server.timeout_read,
    )

    # Build prompt
    output_dir = config.project.output_dir
    mkdocs_path = output_dir / "mkdocs.yml"
    docs_dir = output_dir / "docs"

    prompt = build_enhancement_prompt(mkdocs_path, docs_dir, project_name=config.project.name)
    logger.info("Enhancement prompt: %d chars", len(prompt))

    # Compute max_tokens from detected context window sizes
    max_tokens = _compute_max_tokens(config, slaves, len(prompt))

    if progress_cb:
        progress_cb(0, len(slaves), "", f"Prompt erstellt ({max_tokens} max tokens)")

    # Query ensemble
    ensemble_result = await query_ensemble(
        prompt=prompt,
        model_ids=slaves,
        pool=pool,
        timeout=180,
        max_retries=2,
        retry_delay=3,
        mock_mode=mock_mode,
        max_tokens=max_tokens,
    )

    if progress_cb:
        progress_cb(
            len(ensemble_result.successful_drafts),
            len(slaves),
            "",
            f"{len(ensemble_result.successful_drafts)}/{len(slaves)} Modelle erfolgreich",
        )

    if not ensemble_result.successful_drafts:
        logger.error("No successful drafts from ensemble")
        if ensemble_result.failed_models:
            logger.error("Failed models: %s", ensemble_result.failed_models)
        return []

    # ── Debug: write all drafts + prompt to files ──────────────────
    debug_dir = output_dir / "_enhance_debug"
    debug_dir.mkdir(exist_ok=True)
    try:
        (debug_dir / "00_prompt.txt").write_text(prompt, encoding="utf-8")
        logger.info("Debug: prompt written to %s", debug_dir / "00_prompt.txt")
    except Exception as exc:
        logger.warning("Could not write debug prompt: %s", exc)

    for i, draft in enumerate(ensemble_result.successful_drafts):
        has_markers = "<<<FILE" in draft.output and "<<<END>>>" in draft.output
        safe_name = draft.model_id.replace("/", "_").replace(":", "_")
        debug_file = debug_dir / f"01_draft_{i}_{safe_name}.txt"
        try:
            header = (
                f"# Model: {draft.model_id}\n"
                f"# Length: {len(draft.output)} chars\n"
                f"# Has <<<FILE markers: {has_markers}\n"
                f"# Duration: {draft.duration_seconds:.1f}s\n"
                f"# Retries: {draft.retries}\n"
                f"{'=' * 60}\n\n"
            )
            debug_file.write_text(header + draft.output, encoding="utf-8")
            logger.info("Debug: draft from %s → %s (%d chars, markers=%s)",
                        draft.model_id, debug_file.name, len(draft.output), has_markers)
        except Exception as exc:
            logger.warning("Could not write debug draft: %s", exc)

    for i, model_id in enumerate(ensemble_result.failed_models):
        logger.info("Debug: failed model %s", model_id)
        try:
            (debug_dir / f"01_FAILED_{model_id.replace('/', '_').replace(':', '_')}.txt").write_text(
                f"Model {model_id} failed.\n", encoding="utf-8"
            )
        except Exception:
            pass
    # ── End debug ────────────────────────────────────────────────

    # Merge or select
    if master and len(ensemble_result.successful_drafts) > 1:
        if progress_cb:
            progress_cb(
                len(ensemble_result.successful_drafts),
                len(slaves),
                master,
                f"Master-Modell {master} synthetisiert...",
            )
        merged = await judge_drafts(
            drafts=ensemble_result.successful_drafts,
            context_description="mkdocs-verbesserung",
            stakeholder="developer",
            judge_model_id=master,
            pool=pool,
            timeout=240,
            mock_mode=mock_mode,
        )
    else:
        if len(ensemble_result.successful_drafts) == 1:
            merged = ensemble_result.successful_drafts[0].output
        else:
            merged = _select_best_draft(ensemble_result.successful_drafts)

    if progress_cb:
        progress_cb(len(slaves), len(slaves), "", "Änderungen werden geparst...")

    # ── Debug: write merged result ───────────────────────────────
    try:
        (debug_dir / "02_merged_result.txt").write_text(merged, encoding="utf-8")
        logger.info("Debug: merged result written (%d chars)", len(merged))
    except Exception as exc:
        logger.warning("Could not write debug merged: %s", exc)
    # ── End debug ────────────────────────────────────────────────

    # Parse into FileChange list
    base_dir = str(output_dir)
    changes = parse_file_changes(merged, base_dir=base_dir)

    if not changes:
        logger.warning(
            "No <<<FILE...<<<END>>> blocks found in merged output (%d chars). "
            "Check %s for full output.",
            len(merged), debug_dir / "02_merged_result.txt",
        )

    logger.info("Parsed %d file changes from LLM output", len(changes))
    return changes


async def run_llm_enhancement_single(
    config,
    model_id: str,
    pool: WorkerPool,
    progress_cb: ProgressCallback = None,
    mock_mode: bool = False,
) -> list[FileChange]:
    """Run enhancement with a single model (no ensemble).

    Useful when only one model is available.
    """
    configure_http_fallback(
        server_url=config.server.url,
        api_key=config.server.api_key,
        timeout_read=config.server.timeout_read,
    )

    output_dir = config.project.output_dir
    mkdocs_path = output_dir / "mkdocs.yml"
    docs_dir = output_dir / "docs"

    prompt = build_enhancement_prompt(mkdocs_path, docs_dir, project_name=config.project.name)

    if progress_cb:
        progress_cb(0, 1, model_id, f"Modell {model_id} analysiert...")

    max_tokens = _compute_max_tokens(config, [model_id], len(prompt))

    async with pool.acquire(f"enhance:{model_id}"):
        result = await run_opencode(
            prompt=prompt,
            model_id=model_id,
            timeout=180,
            max_retries=2,
            retry_delay=3,
            mock_mode=mock_mode,
            max_tokens=max_tokens,
        )

    if progress_cb:
        progress_cb(1, 1, model_id, "Fertig")

    if not result.success or not result.output.strip():
        logger.error("Single model enhancement failed: %s", result.error)
        return []

    base_dir = str(output_dir)
    changes = parse_file_changes(result.output, base_dir=base_dir)
    logger.info("Parsed %d file changes from single model", len(changes))
    return changes
