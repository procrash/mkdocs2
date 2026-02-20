"""Interactive setup wizard for first-time configuration."""
from __future__ import annotations
import asyncio
import logging

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

from ..config.loader import save_config
from ..config.schema import (
    AppConfig,
    ModelConfig,
    ModelsConfig,
    ServerConfig,
    StakeholderConfig,
)
from ..discovery.model_classifier import classify_models
from ..discovery.opencode_configurator import generate_opencode_config
from ..discovery.role_assigner import assign_roles
from ..discovery.server_probe import probe_server

logger = logging.getLogger(__name__)
console = Console()


async def run_setup_wizard(config: AppConfig | None = None) -> AppConfig:
    """Run the interactive setup wizard."""
    console.print(Panel.fit(
        "[bold blue]mkdocsOnSteroids Setup Wizard[/bold blue]\n"
        "This wizard will help you configure the documentation generator.",
    ))

    if config is None:
        config = AppConfig()

    # Step 1: Project settings
    console.print("\n[bold]Step 1: Project Settings[/bold]")
    config.project.name = Prompt.ask(
        "Project name", default=config.project.name,
    )
    source_dir = Prompt.ask(
        "Source code directory", default=str(config.project.source_dir),
    )
    config.project.source_dir = __import__("pathlib").Path(source_dir)
    output_dir = Prompt.ask(
        "Output directory", default=str(config.project.output_dir),
    )
    config.project.output_dir = __import__("pathlib").Path(output_dir)

    langs = Prompt.ask(
        "Languages (comma-separated)", default=",".join(config.project.languages),
    )
    config.project.languages = [l.strip() for l in langs.split(",")]

    # Step 2: Server configuration
    console.print("\n[bold]Step 2: Server Configuration[/bold]")
    config.server.url = Prompt.ask(
        "OpenAI-compatible server URL", default=config.server.url,
    )
    config.server.api_key = Prompt.ask(
        "API key (leave empty for no auth)", default=config.server.api_key,
    )

    # Step 3: Discover models
    console.print("\n[bold]Step 3: Model Discovery[/bold]")
    with console.status("Probing server..."):
        discovered = await probe_server(
            config.server.url, config.server.api_key,
        )

    if discovered:
        model_ids = [m.id for m in discovered]
        classified = classify_models(model_ids)
        assignment = assign_roles(classified)

        table = Table(title="Discovered Models")
        table.add_column("Model", style="cyan")
        table.add_column("Assigned Role", style="green")
        table.add_column("Capabilities")

        for m in classified:
            role = "Judge" if assignment.judge and m.id == assignment.judge.id else "Analyst"
            caps = ", ".join(c.value for c in m.capabilities)
            table.add_row(m.id, role, caps)
        console.print(table)

        if Confirm.ask("Accept automatic role assignment?", default=True):
            # Convert to config
            config.models = ModelsConfig(
                analysts=[
                    ModelConfig(
                        id=m.id,
                        capabilities=[c.value for c in m.capabilities],
                        max_context=m.estimated_context,
                    )
                    for m in assignment.analysts
                ],
                judge=ModelConfig(
                    id=assignment.judge.id,
                    capabilities=[c.value for c in assignment.judge.capabilities],
                    max_context=assignment.judge.estimated_context,
                ) if assignment.judge else None,
            )
            # Generate opencode.json
            from pathlib import Path
            generate_opencode_config(
                assignment, config.server.url, config.server.api_key,
                output_path=Path("opencode.json"),
            )
            console.print("[green]opencode.json generated[/green]")
    else:
        console.print("[yellow]No models discovered. Configure manually in config.yaml[/yellow]")

    # Step 4: Stakeholders
    console.print("\n[bold]Step 4: Stakeholder Configuration[/bold]")
    config.stakeholders.developer.enabled = Confirm.ask(
        "Enable Developer documentation?", default=True,
    )
    config.stakeholders.api.enabled = Confirm.ask(
        "Enable API documentation?", default=True,
    )
    config.stakeholders.user.enabled = Confirm.ask(
        "Enable User documentation?", default=True,
    )

    # Step 5: System settings
    console.print("\n[bold]Step 5: System Settings[/bold]")
    workers = Prompt.ask(
        "Parallel workers", default=str(config.system.parallel_workers),
    )
    config.system.parallel_workers = int(workers)
    config.system.mock_mode = Confirm.ask(
        "Enable mock mode (no real LLM calls)?", default=False,
    )

    # Save config
    console.print("\n[bold]Saving configuration...[/bold]")
    from pathlib import Path
    save_config(config, Path("config.yaml"))
    console.print("[green]config.yaml saved successfully![/green]")

    console.print(Panel.fit(
        "[bold green]Setup complete![/bold green]\n"
        "Run [cyan]mkdocs-steroids generate --cli[/cyan] to start generating documentation.",
    ))

    return config
