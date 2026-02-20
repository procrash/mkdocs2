"""mkdocsOnSteroids - CLI entrypoint using Click."""
from __future__ import annotations

import asyncio
import logging
import sys
from pathlib import Path

import click

from .config.loader import load_config, save_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("mkdocs-steroids")


@click.group()
@click.option("--config", "-c", default="config.yaml", help="Path to config.yaml")
@click.option("--verbose", "-v", is_flag=True, help="Enable debug logging")
@click.pass_context
def cli(ctx: click.Context, config: str, verbose: bool) -> None:
    """mkdocsOnSteroids - Automated documentation generator."""
    ctx.ensure_object(dict)
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    ctx.obj["config_path"] = Path(config)


@cli.command()
@click.option("--server-url", default=None, help="Override server URL")
@click.option("--interactive", is_flag=True, help="Run interactive setup wizard")
@click.pass_context
def setup(ctx: click.Context, server_url: str | None, interactive: bool) -> None:
    """Set up mkdocsOnSteroids (discover models, generate config)."""
    config_path = ctx.obj["config_path"]
    config = load_config(config_path)

    if server_url:
        config.server.url = server_url

    if interactive:
        from .ui.setup_wizard import run_setup_wizard
        asyncio.run(run_setup_wizard(config))
    else:
        # Non-interactive: just discover and save
        from .discovery.server_probe import probe_server
        from .discovery.model_classifier import classify_models
        from .discovery.role_assigner import assign_roles
        from .discovery.opencode_configurator import generate_opencode_config

        async def _setup():
            discovered = await probe_server(config.server.url, config.server.api_key)
            if not discovered:
                click.echo(f"No models found at {config.server.url}")
                return
            model_ids = [m.id for m in discovered]
            classified = classify_models(model_ids)
            assignment = assign_roles(classified)

            for m in classified:
                role = "Judge" if assignment.judge and m.id == assignment.judge.id else "Analyst"
                click.echo(f"  {m.id}: {role}")

            generate_opencode_config(
                assignment, config.server.url, config.server.api_key,
                output_path=Path("opencode.json"),
            )
            click.echo("opencode.json generated")
            save_config(config, config_path)
            click.echo(f"Config saved to {config_path}")

        asyncio.run(_setup())


@cli.command()
@click.option("--server-url", default=None, help="Override server URL")
@click.option("--auto-assign", is_flag=True, default=True, help="Auto-assign roles")
@click.pass_context
def discover(ctx: click.Context, server_url: str | None, auto_assign: bool) -> None:
    """Discover available models from OpenAI-compatible server."""
    config = load_config(ctx.obj["config_path"])
    if server_url:
        config.server.url = server_url

    from .discovery.server_probe import probe_server
    from .discovery.model_classifier import classify_models
    from .discovery.role_assigner import assign_roles

    async def _discover():
        discovered = await probe_server(config.server.url, config.server.api_key)
        if not discovered:
            click.echo(f"No models found at {config.server.url}")
            sys.exit(1)

        click.echo(f"Found {len(discovered)} models:")
        for m in discovered:
            click.echo(f"  - {m.id} (owned_by: {m.owned_by})")

        if auto_assign:
            model_ids = [m.id for m in discovered]
            classified = classify_models(model_ids)
            assignment = assign_roles(classified)

            click.echo("\nRole assignments:")
            if assignment.judge:
                click.echo(f"  Judge: {assignment.judge.id}")
            for a in assignment.analysts:
                click.echo(f"  Analyst: {a.id}")

    asyncio.run(_discover())


@cli.command()
@click.option("--stakeholder", "-s", type=click.Choice(["developer", "api", "user", "all"]),
              default="all", help="Stakeholder to generate for")
@click.option("--tui", is_flag=True, help="Use TUI mode")
@click.pass_context
def generate(ctx: click.Context, stakeholder: str, tui: bool) -> None:
    """Generate documentation from source code."""
    config = load_config(ctx.obj["config_path"])

    # Apply stakeholder filter
    if stakeholder != "all":
        for sh_name in ("developer", "api", "user"):
            sh_cfg = getattr(config.stakeholders, sh_name)
            if sh_name != stakeholder:
                sh_cfg.enabled = False

    if tui:
        from .ui.tui_app import run_tui
        run_tui(config)
    else:
        from .ui.cli_runner import run_cli_pipeline
        report = asyncio.run(run_cli_pipeline(config))
        sys.exit(0 if report.failed == 0 else 1)


@cli.command()
@click.option("--port", "-p", default=8000, help="Port to serve on")
@click.pass_context
def serve(ctx: click.Context, port: int) -> None:
    """Serve the generated documentation with MkDocs."""
    import subprocess
    config = load_config(ctx.obj["config_path"])
    mkdocs_dir = config.project.output_dir
    mkdocs_yml = mkdocs_dir / "mkdocs.yml"

    if not mkdocs_yml.exists():
        click.echo(f"mkdocs.yml not found at {mkdocs_yml}. Run 'generate' first.")
        sys.exit(1)

    click.echo(f"Serving documentation at http://localhost:{port}")
    subprocess.run(
        ["mkdocs", "serve", "--dev-addr", f"0.0.0.0:{port}"],
        cwd=str(mkdocs_dir),
    )


@cli.command()
@click.pass_context
def report(ctx: click.Context) -> None:
    """Show the last generation report."""
    config = load_config(ctx.obj["config_path"])
    report_path = config.project.output_dir / "generation_report.md"

    if not report_path.exists():
        click.echo("No report found. Run 'generate' first.")
        sys.exit(1)

    click.echo(report_path.read_text(encoding="utf-8"))


def main() -> None:
    """Main entry point."""
    cli(obj={})


if __name__ == "__main__":
    main()
