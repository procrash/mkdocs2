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


def build_enhancement_prompt(mkdocs_path: Path, docs_dir: Path) -> str:
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
    if docs_dir.exists():
        for md_file in sorted(docs_dir.rglob("*.md")):
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

    # Use registered template
    ensure_loaded()
    ctx = PromptContext(
        code_content=mkdocs_content,
        file_listing=file_listing,
    )
    prompt = build_prompt("enhance", "analysis", ctx)
    if prompt:
        return prompt

    # Fallback: build directly if template not found
    logger.warning("enhance/analysis template not found, using inline fallback")
    return f"""Du bist ein erfahrener MkDocs-Experte und Technical Writer.

Analysiere die folgende Dokumentationsstruktur und mkdocs.yml-Konfiguration.
Schlage konkrete Verbesserungen vor als geänderte Dateien.

## Aktuelle mkdocs.yml:
```yaml
{mkdocs_content}
```

## Vorhandene Dokumentations-Dateien:
{file_listing}

## Deine Aufgabe:
1. Analysiere die Struktur auf Schwächen (fehlende Seiten, schlechte Navigation, etc.)
2. Prüfe die mkdocs.yml auf Optimierungspotenzial (Theme-Einstellungen, Features, etc.)
3. Schlage neue oder verbesserte Markdown-Seiten vor
4. Schlage mkdocs.yml-Änderungen vor falls sinnvoll

## Ausgabeformat (STRIKT einhalten):

Für jede geänderte/neue Datei:
<<<FILE pfad/zur/datei.md
DESCRIPTION: Kurze Beschreibung der Änderung
>>>
Kompletter neuer Dateiinhalt hier
<<<END>>>

Nur Dateien ausgeben die sich tatsächlich ändern oder neu sind.
Bestehende Inhalte verbessern, nicht löschen.
Alle Texte auf Deutsch."""


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

    prompt = build_enhancement_prompt(mkdocs_path, docs_dir)
    logger.info("Enhancement prompt: %d chars", len(prompt))

    if progress_cb:
        progress_cb(0, len(slaves), "", "Prompt erstellt")

    # Query ensemble
    ensemble_result = await query_ensemble(
        prompt=prompt,
        model_ids=slaves,
        pool=pool,
        timeout=180,
        max_retries=2,
        retry_delay=3,
        mock_mode=mock_mode,
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
        return []

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

    # Parse into FileChange list
    base_dir = str(output_dir)
    changes = parse_file_changes(merged, base_dir=base_dir)

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

    prompt = build_enhancement_prompt(mkdocs_path, docs_dir)

    if progress_cb:
        progress_cb(0, 1, model_id, f"Modell {model_id} analysiert...")

    async with pool.acquire(f"enhance:{model_id}"):
        result = await run_opencode(
            prompt=prompt,
            model_id=model_id,
            timeout=180,
            max_retries=2,
            retry_delay=3,
            mock_mode=mock_mode,
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
