"""Generate pipeline execution reports."""
from __future__ import annotations
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class FileReport:
    """Report for a single file's documentation generation."""
    file_path: str
    stakeholder: str
    doc_type: str
    success: bool
    model_used: str = ""
    duration_seconds: float = 0.0
    retries: int = 0
    error: str = ""
    output_path: str = ""


@dataclass
class PipelineReport:
    """Complete report for a pipeline run."""
    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime | None = None
    total_files_scanned: int = 0
    total_tasks: int = 0
    successful: int = 0
    failed: int = 0
    skipped: int = 0
    file_reports: list[FileReport] = field(default_factory=list)
    models_used: dict[str, int] = field(default_factory=dict)
    by_stakeholder: dict[str, dict[str, int]] = field(default_factory=dict)

    @property
    def duration_seconds(self) -> float:
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0

    @property
    def success_rate(self) -> float:
        if self.total_tasks == 0:
            return 0.0
        return self.successful / self.total_tasks * 100

    def add_file_report(self, report: FileReport) -> None:
        """Add a file report and update aggregates."""
        self.file_reports.append(report)
        if report.success:
            self.successful += 1
        else:
            self.failed += 1

        if report.model_used:
            self.models_used[report.model_used] = (
                self.models_used.get(report.model_used, 0) + 1
            )

        stakeholder_stats = self.by_stakeholder.setdefault(
            report.stakeholder, {"success": 0, "failed": 0}
        )
        if report.success:
            stakeholder_stats["success"] += 1
        else:
            stakeholder_stats["failed"] += 1

    def finalize(self) -> None:
        """Mark the report as complete."""
        self.end_time = datetime.now()

    def to_markdown(self) -> str:
        """Generate a markdown report."""
        lines = [
            "# Documentation Generation Report\n",
            f"**Generated**: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n",
            f"**Duration**: {self.duration_seconds:.1f}s\n",
            "",
            "## Summary\n",
            f"| Metric | Value |",
            f"|---|---|",
            f"| Files Scanned | {self.total_files_scanned} |",
            f"| Total Tasks | {self.total_tasks} |",
            f"| Successful | {self.successful} |",
            f"| Failed | {self.failed} |",
            f"| Success Rate | {self.success_rate:.1f}% |",
            "",
        ]

        if self.models_used:
            lines.append("## Models Used\n")
            lines.append("| Model | Tasks |")
            lines.append("|---|---|")
            for model, count in sorted(self.models_used.items()):
                lines.append(f"| {model} | {count} |")
            lines.append("")

        if self.by_stakeholder:
            lines.append("## By Stakeholder\n")
            lines.append("| Stakeholder | Success | Failed |")
            lines.append("|---|---|---|")
            for sh, stats in sorted(self.by_stakeholder.items()):
                lines.append(f"| {sh} | {stats['success']} | {stats['failed']} |")
            lines.append("")

        # Failed tasks
        failed = [r for r in self.file_reports if not r.success]
        if failed:
            lines.append("## Failed Tasks\n")
            for r in failed:
                lines.append(f"- **{r.file_path}** ({r.stakeholder}/{r.doc_type}): {r.error}")
            lines.append("")

        return "\n".join(lines)

    def save(self, output_dir: Path) -> Path:
        """Save the report to a file."""
        report_path = output_dir / "generation_report.md"
        report_path.write_text(self.to_markdown(), encoding="utf-8")
        logger.info("Report saved to %s", report_path)
        return report_path
