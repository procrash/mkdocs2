"""CLI runner with Rich progress bars and status display."""
from __future__ import annotations
import asyncio
import logging
import sys

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table
from rich.text import Text

from ..analyzer.file_classifier import classify_file
from ..analyzer.scanner import scan_directory
from ..config.schema import AppConfig
from ..discovery.model_classifier import classify_models
from ..discovery.opencode_configurator import generate_opencode_config
from ..discovery.role_assigner import assign_roles, RoleAssignment
from ..discovery.server_probe import probe_server
from ..generator.index_generator import generate_index_pages
from ..generator.markdown_writer import write_markdown, write_manual_placeholder
from ..generator.mkdocs_builder import write_mkdocs_config
from ..orchestrator.engine import OrchestrationEngine, GenerationResult, PipelineResult
from ..reporting.report import PipelineReport, FileReport

logger = logging.getLogger(__name__)


console = Console()


async def run_cli_pipeline(config: AppConfig) -> PipelineReport:
    """Run the full documentation pipeline with CLI progress display."""
    report = PipelineReport()

    console.print(Panel.fit(
        "[bold blue]mkdocsOnSteroids[/bold blue] - Documentation Generator",
        subtitle=f"Project: {config.project.name}",
    ))

    # Phase 1: Discovery
    console.print("\n[bold]Phase 1: Server Discovery[/bold]")
    assignment = await _discover_models(config)
    if not assignment.analysts:
        if not config.system.mock_mode:
            console.print("[red]No models available. Enable mock_mode or check server.[/red]")
            report.finalize()
            return report
        console.print("[yellow]Mock mode enabled, continuing without models.[/yellow]")
        # Create a dummy assignment for mock mode
        from ..discovery.model_classifier import ClassifiedModel
        assignment = RoleAssignment(
            analysts=[ClassifiedModel(id="mock-model", capabilities=[], estimated_context=32768)]
        )

    # Phase 2: Source Scanning
    console.print("\n[bold]Phase 2: Source Code Scanning[/bold]")
    scan_result, classified_files = _scan_sources(config)
    report.total_files_scanned = scan_result.total_files

    if not classified_files:
        console.print("[yellow]No source files found to document.[/yellow]")
        report.finalize()
        return report

    # Phase 3: Documentation Generation
    console.print("\n[bold]Phase 3: Documentation Generation[/bold]")
    engine = OrchestrationEngine(
        config=config,
        assignment=assignment,
        scan_result=scan_result,
        classified_files=classified_files,
    )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        gen_task = progress.add_task(
            "Generating documentation...",
            total=None,  # Unknown until engine builds tasks
        )

        pipeline_result = await engine.run()

        progress.update(gen_task, completed=pipeline_result.total_tasks, total=pipeline_result.total_tasks)

    # Write outputs
    console.print("\n[bold]Phase 4: Writing Output[/bold]")
    output_dir = config.project.output_dir
    written_count = 0

    for result in pipeline_result.results:
        if result.success and result.content:
            output_path = write_markdown(
                content=result.content,
                output_dir=output_dir,
                stakeholder=result.task.stakeholder,
                doc_type=result.task.doc_type,
                name=result.task.file.doc_name,
            )
            written_count += 1
            report.add_file_report(FileReport(
                file_path=str(result.task.file.relative_path),
                stakeholder=result.task.stakeholder,
                doc_type=result.task.doc_type,
                success=True,
                duration_seconds=result.duration_seconds,
                output_path=str(output_path),
            ))
        else:
            report.add_file_report(FileReport(
                file_path=str(result.task.file.relative_path),
                stakeholder=result.task.stakeholder,
                doc_type=result.task.doc_type,
                success=False,
                error=result.error,
            ))

    # Generate index pages and manual placeholders
    generate_index_pages(output_dir, config.project.name)
    write_manual_placeholder(output_dir, "index.md", "Manual")
    write_manual_placeholder(output_dir, "changelog.md", "Changelog")
    write_manual_placeholder(output_dir, "contributing.md", "Contributing")
    write_manual_placeholder(output_dir, "faq.md", "FAQ")

    # Generate mkdocs.yml
    write_mkdocs_config(config, output_dir)

    report.total_tasks = pipeline_result.total_tasks
    report.finalize()

    # Print summary
    _print_summary(report, written_count)

    # Save report
    report.save(output_dir)

    return report


async def _discover_models(config: AppConfig) -> RoleAssignment:
    """Discover and classify models from the configured server."""
    with console.status("Probing server..."):
        discovered = await probe_server(
            config.server.url,
            config.server.api_key,
            config.server.timeout_connect,
        )

    if not discovered:
        console.print(f"[yellow]No models found at {config.server.url}[/yellow]")

        # Check if models are pre-configured
        if config.models.analysts:
            console.print("[cyan]Using pre-configured models from config.yaml[/cyan]")
            from ..discovery.model_classifier import ClassifiedModel, ModelCapability
            classified = []
            for m in config.models.analysts:
                caps = [ModelCapability(c) for c in m.capabilities if c in ModelCapability.__members__.values()]
                classified.append(ClassifiedModel(
                    id=m.id, capabilities=caps, estimated_context=m.max_context,
                ))
            assignment = assign_roles(classified)
            if config.models.judge:
                judge_caps = [ModelCapability(c) for c in config.models.judge.capabilities if c in ModelCapability.__members__.values()]
                assignment.judge = ClassifiedModel(
                    id=config.models.judge.id,
                    capabilities=judge_caps,
                    estimated_context=config.models.judge.max_context,
                )
            return assignment
        return RoleAssignment()

    model_ids = [m.id for m in discovered]
    classified = classify_models(model_ids)
    assignment = assign_roles(classified)

    # Display results
    table = Table(title="Discovered Models")
    table.add_column("Model", style="cyan")
    table.add_column("Role", style="green")
    table.add_column("Capabilities")
    table.add_column("Context", justify="right")

    for m in classified:
        role = "Judge" if assignment.judge and m.id == assignment.judge.id else "Analyst"
        caps = ", ".join(c.value for c in m.capabilities)
        table.add_row(m.id, role, caps, str(m.estimated_context))

    console.print(table)

    # Generate opencode.json
    generate_opencode_config(
        assignment, config.server.url, config.server.api_key,
        output_path=None,  # Don't write to disk in CLI mode
    )

    return assignment


def _scan_sources(config: AppConfig):
    """Scan and classify source files."""
    scan_result = scan_directory(
        config.project.source_dir,
        config.project.languages,
        config.project.ignore_patterns,
    )

    classified_files = []
    for sf in scan_result.files:
        cf = classify_file(sf.path, sf.relative_path, sf.language)
        classified_files.append(cf)

    table = Table(title=f"Source Files ({scan_result.total_files} total)")
    table.add_column("Language", style="cyan")
    table.add_column("Count", justify="right")
    for lang, count in sorted(scan_result.by_language.items()):
        table.add_row(lang, str(count))
    console.print(table)

    return scan_result, classified_files


def _print_summary(report: PipelineReport, written: int) -> None:
    """Print the final summary."""
    status = "[green]SUCCESS[/green]" if report.failed == 0 else "[yellow]PARTIAL[/yellow]"
    console.print(f"\n[bold]Result: {status}[/bold]")
    console.print(f"  Files scanned: {report.total_files_scanned}")
    console.print(f"  Tasks: {report.total_tasks}")
    console.print(f"  Successful: [green]{report.successful}[/green]")
    console.print(f"  Failed: [red]{report.failed}[/red]")
    console.print(f"  Pages written: {written}")
    console.print(f"  Duration: {report.duration_seconds:.1f}s")
