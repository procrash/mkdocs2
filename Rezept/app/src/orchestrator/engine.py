"""Main orchestrator engine - coordinates the entire documentation pipeline."""
from __future__ import annotations
import asyncio
import logging
from dataclasses import dataclass, field
from pathlib import Path

from ..analyzer.code_chunker import chunk_code
from ..analyzer.doxygen_extractor import extract_doxygen_comments, format_doxygen_as_context
from ..analyzer.file_classifier import ClassifiedFile, FileCategory
from ..analyzer.scanner import ScanResult
from ..config.schema import AppConfig
from ..discovery.opencode_configurator import get_model_provider_id
from ..discovery.role_assigner import RoleAssignment
from ..prompts.builder import PromptContext, build_prompt
from .ensemble import query_ensemble, EnsembleResult
from .judge import judge_drafts
from .opencode_runner import configure_http_fallback
from .semaphore import WorkerPool

logger = logging.getLogger(__name__)


@dataclass
class GenerationTask:
    """A single documentation generation task."""
    file: ClassifiedFile
    stakeholder: str
    doc_type: str
    chunk_index: int = 0
    total_chunks: int = 1


@dataclass
class GenerationResult:
    """Result of a single generation task."""
    task: GenerationTask
    content: str = ""
    success: bool = False
    error: str = ""
    duration_seconds: float = 0.0


@dataclass
class PipelineResult:
    """Result of the entire pipeline run."""
    results: list[GenerationResult] = field(default_factory=list)
    total_tasks: int = 0
    successful: int = 0
    failed: int = 0


# Map file categories to stakeholder doc_types
CATEGORY_DOC_TYPES: dict[FileCategory, dict[str, list[str]]] = {
    FileCategory.CLASS_DEF: {
        "developer": ["classes"],
        "api": [],
        "user": ["features"],
    },
    FileCategory.MODULE: {
        "developer": ["modules"],
        "api": [],
        "user": ["features"],
    },
    FileCategory.HEADER: {
        "developer": ["classes", "functions"],
        "api": ["schemas"],
        "user": [],
    },
    FileCategory.API_ENDPOINT: {
        "developer": ["functions"],
        "api": ["endpoints"],
        "user": ["features"],
    },
    FileCategory.UTILITY: {
        "developer": ["functions"],
        "api": [],
        "user": [],
    },
    FileCategory.MAIN: {
        "developer": ["modules"],
        "api": [],
        "user": ["features"],
    },
}


class OrchestrationEngine:
    """Main engine that orchestrates the documentation pipeline."""

    def __init__(
        self,
        config: AppConfig,
        assignment: RoleAssignment,
        scan_result: ScanResult,
        classified_files: list[ClassifiedFile],
        progress_callback=None,
    ):
        self.config = config
        self.assignment = assignment
        self.scan_result = scan_result
        self.classified_files = classified_files
        self.progress_callback = progress_callback
        self.pool = WorkerPool(config.system.parallel_workers)

    def _build_tasks(self) -> list[GenerationTask]:
        """Build the list of generation tasks from classified files."""
        tasks: list[GenerationTask] = []
        stakeholders_cfg = self.config.stakeholders

        for cf in self.classified_files:
            if cf.category in (FileCategory.TEST, FileCategory.CONFIG, FileCategory.UNKNOWN):
                continue

            doc_types_map = CATEGORY_DOC_TYPES.get(cf.category, {})

            for stakeholder_name in ("developer", "api", "user"):
                stakeholder_cfg = getattr(stakeholders_cfg, stakeholder_name, None)
                if not stakeholder_cfg or not stakeholder_cfg.enabled:
                    continue

                applicable_types = doc_types_map.get(stakeholder_name, [])
                enabled_types = stakeholder_cfg.doc_types

                for dt in applicable_types:
                    if dt in enabled_types:
                        tasks.append(GenerationTask(
                            file=cf,
                            stakeholder=stakeholder_name,
                            doc_type=dt,
                        ))

        logger.info("Built %d generation tasks", len(tasks))
        return tasks

    async def run(self) -> PipelineResult:
        """Run the full documentation generation pipeline."""
        # Configure HTTP fallback for direct API access
        configure_http_fallback(
            server_url=self.config.server.url,
            api_key=self.config.server.api_key,
            timeout_read=self.config.server.timeout_read,
        )

        tasks = self._build_tasks()
        pipeline_result = PipelineResult(total_tasks=len(tasks))

        if not tasks:
            logger.warning("No generation tasks to run")
            return pipeline_result

        analyst_ids = [
            get_model_provider_id(m) for m in self.assignment.analysts
        ]
        judge_id = (
            get_model_provider_id(self.assignment.judge)
            if self.assignment.judge else None
        )

        semaphore = asyncio.Semaphore(self.config.system.parallel_workers)

        async def process_task(task: GenerationTask) -> GenerationResult:
            async with semaphore:
                return await self._process_single_task(
                    task, analyst_ids, judge_id,
                )

        coroutines = [process_task(t) for t in tasks]
        results = await asyncio.gather(*coroutines, return_exceptions=True)

        for task, result in zip(tasks, results):
            if isinstance(result, Exception):
                gr = GenerationResult(
                    task=task, success=False, error=str(result),
                )
            else:
                gr = result

            pipeline_result.results.append(gr)
            if gr.success:
                pipeline_result.successful += 1
            else:
                pipeline_result.failed += 1

            if self.progress_callback:
                self.progress_callback(gr, pipeline_result)

        return pipeline_result

    async def _process_single_task(
        self,
        task: GenerationTask,
        analyst_ids: list[str],
        judge_id: str | None,
    ) -> GenerationResult:
        """Process a single generation task through the ensemble pipeline."""
        import time
        start = time.monotonic()

        try:
            content = task.file.path.read_text(encoding="utf-8", errors="replace")
        except Exception as exc:
            return GenerationResult(
                task=task, success=False, error=f"Cannot read file: {exc}",
            )

        # Extract doxygen if present
        doxygen_ctx = ""
        if task.file.has_doxygen:
            comments = extract_doxygen_comments(content)
            doxygen_ctx = format_doxygen_as_context(comments)

        # Chunk if needed
        chunks = chunk_code(
            content, str(task.file.relative_path), task.file.language,
            max_tokens=8000,
        )

        all_content_parts: list[str] = []

        for chunk in chunks:
            ctx = PromptContext(
                code_content=chunk.content,
                file_path=str(task.file.relative_path),
                language=task.file.language,
                classes=task.file.classes,
                functions=task.file.functions,
                doxygen_section=doxygen_ctx,
            )

            prompt = build_prompt(task.stakeholder, task.doc_type, ctx)
            if not prompt:
                continue

            # Query ensemble
            ensemble_result = await query_ensemble(
                prompt=prompt,
                model_ids=analyst_ids,
                pool=self.pool,
                timeout=self.config.system.global_timeout_seconds,
                max_retries=self.config.system.max_retries,
                retry_delay=self.config.system.retry_base_delay,
                mock_mode=self.config.system.mock_mode,
            )

            if not ensemble_result.successful_drafts:
                logger.warning(
                    "No successful drafts for %s/%s/%s",
                    task.stakeholder, task.doc_type, task.file.relative_path,
                )
                continue

            # Judge/merge
            if judge_id and len(ensemble_result.successful_drafts) > 1:
                merged = await judge_drafts(
                    drafts=ensemble_result.successful_drafts,
                    context_description=f"{task.file.relative_path} ({task.doc_type})",
                    stakeholder=task.stakeholder,
                    judge_model_id=judge_id,
                    pool=self.pool,
                    timeout=self.config.system.global_timeout_seconds,
                    mock_mode=self.config.system.mock_mode,
                )
            else:
                # Single model or no judge: take best draft
                best = max(
                    ensemble_result.successful_drafts,
                    key=lambda d: len(d.output),
                )
                merged = best.output

            all_content_parts.append(merged)

        duration = time.monotonic() - start
        if all_content_parts:
            return GenerationResult(
                task=task,
                content="\n\n".join(all_content_parts),
                success=True,
                duration_seconds=duration,
            )
        else:
            return GenerationResult(
                task=task,
                success=False,
                error="No content generated",
                duration_seconds=duration,
            )
