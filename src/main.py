"""mkdocsOnSteroids - CLI entrypoint using Click."""
from __future__ import annotations

import asyncio
import logging
import os
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
@click.option("--auto", "-a", is_flag=True, help="Automationsmodus (keine Rückfragen)")
@click.pass_context
def cli(ctx: click.Context, config: str, verbose: bool, auto: bool) -> None:
    """mkdocsOnSteroids - Automated documentation generator."""
    ctx.ensure_object(dict)
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    ctx.obj["config_path"] = Path(config)
    ctx.obj["auto"] = auto or os.environ.get("AUTOMATION_MODE", "").lower() in ("1", "true", "yes")


@cli.command()
@click.option("--server-url", default=None, help="Override server URL")
@click.option("--interactive", is_flag=True, help="Run interactive setup wizard")
@click.pass_context
def setup(ctx: click.Context, server_url: str | None, interactive: bool) -> None:
    """Set up mkdocsOnSteroids (discover models, generate config)."""
    config_path = ctx.obj["config_path"]
    config = load_config(config_path)
    auto = ctx.obj["auto"]

    if server_url:
        config.server.url = server_url

    if interactive and not auto:
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
                role = "Master" if assignment.judge and m.id == assignment.judge.id else "Slave"
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
            ctx_info = f", ctx:{m.context_length}" if m.context_length > 0 else ""
            click.echo(f"  - {m.id} (owned_by: {m.owned_by}{ctx_info})")

        if auto_assign:
            model_ids = [m.id for m in discovered]
            detected_ctx = {m.id: m.context_length for m in discovered if m.context_length > 0}

            # Probe capabilities (instruct, tool_use)
            from .discovery.server_probe import probe_all_capabilities
            click.echo("\nProbing capabilities (instruct, tool_use)...")
            detected_caps = await probe_all_capabilities(
                config.server.url, discovered, config.server.api_key, timeout=15,
            )

            classified = classify_models(model_ids, detected_ctx, detected_caps)
            assignment = assign_roles(classified)

            click.echo(f"\nClassification:")
            for m in classified:
                caps = ", ".join(c.value for c in m.capabilities)
                click.echo(f"  {m.id}: {m.size_class}, ctx={m.estimated_context:,}, [{caps}]")

            click.echo("\nRole assignments:")
            if assignment.judge:
                click.echo(f"  Master: {assignment.judge.id}")
            for a in assignment.analysts:
                click.echo(f"  Slave: {a.id}")

            # Persist discovered data
            from .config.schema import ModelHealthEntry
            for m in classified:
                caps_list = list(detected_caps.get(m.id, set()))
                entry_found = False
                for e in config.model_health.entries:
                    if e.model_id == m.id:
                        e.context_length = detected_ctx.get(m.id, 0)
                        if caps_list:
                            e.detected_capabilities = caps_list
                        entry_found = True
                        break
                if not entry_found:
                    config.model_health.entries.append(ModelHealthEntry(
                        model_id=m.id,
                        context_length=detected_ctx.get(m.id, 0),
                        detected_capabilities=caps_list,
                    ))
            save_config(config, ctx.obj["config_path"])
            click.echo(f"\nModel data saved to {ctx.obj['config_path']}")

    asyncio.run(_discover())


@cli.command()
@click.option("--stakeholder", "-s", type=click.Choice(["developer", "api", "user", "all"]),
              default="all", help="Stakeholder to generate for")
@click.option("--tui", is_flag=True, help="Use TUI mode")
@click.pass_context
def generate(ctx: click.Context, stakeholder: str, tui: bool) -> None:
    """Generate documentation from source code."""
    config = load_config(ctx.obj["config_path"])
    auto = ctx.obj["auto"]

    # Apply stakeholder filter
    if stakeholder != "all":
        for sh_name in ("developer", "api", "user"):
            sh_cfg = getattr(config.stakeholders, sh_name)
            if sh_name != stakeholder:
                sh_cfg.enabled = False

    if tui:
        from .ui.tui_app import run_tui
        run_tui(config, auto=auto)
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


@cli.command(name="init")
@click.option("--force", is_flag=True, help="Bestehende Skeleton-Dateien überschreiben")
@click.pass_context
def init_skeleton(ctx: click.Context, force: bool) -> None:
    """Initialize the documentation skeleton with rich content guidelines.

    Creates the directory structure and placeholder pages. Can be run
    independently before 'generate' or 'run'.
    Safe to run multiple times — existing files are not overwritten (unless --force).
    """
    config_path = ctx.obj["config_path"]
    config = load_config(config_path)
    output_dir = config.project.output_dir

    if force:
        # Remove existing docs to rebuild
        docs_dir = output_dir / "docs"
        if docs_dir.exists():
            import shutil
            shutil.rmtree(docs_dir)
            click.echo(f"Bestehendes docs/ entfernt: {docs_dir}")

    from .generator.skeleton_builder import create_skeleton, create_suggestion_files

    created = create_skeleton(output_dir, config.project.name)
    click.echo(f"Skeleton: {len(created)} Dateien erstellt in {output_dir / 'docs'}")

    # Also create suggestion files if any are stored
    if config.preferences.skeleton_suggestions:
        sugg_created = create_suggestion_files(output_dir, config.preferences.skeleton_suggestions)
        if sugg_created:
            click.echo(f"LLM-Vorschläge: {len(sugg_created)} zusätzliche Dateien erstellt")

    # Generate mkdocs.yml
    from .generator.mkdocs_builder import write_mkdocs_config
    write_mkdocs_config(config, output_dir)
    click.echo(f"mkdocs.yml generiert: {output_dir / 'mkdocs.yml'}")

    click.echo("\nFertig. Starte mit 'serve' um die Struktur im Browser zu sehen,")
    click.echo("oder mit 'run' für den vollen Workflow.")


@cli.command(name="restructure")
@click.pass_context
def restructure_cmd(ctx: click.Context) -> None:
    """Analyze documentation structure and suggest improvements.

    Checks for empty files, overly large files, unnecessary nesting,
    duplicate titles and other structural issues.
    """
    config = load_config(ctx.obj["config_path"])
    auto = ctx.obj["auto"]
    _run_restructure(config, config.project.output_dir, auto)


@cli.command()
@click.pass_context
def run(ctx: click.Context) -> None:
    """Start the full TUI workflow (discovery → generation → chat)."""
    config_path = ctx.obj["config_path"]
    config = load_config(config_path)
    auto = ctx.obj["auto"]

    from .ui.tui_app import run_tui
    run_tui(config, config_path=config_path, auto=auto)


@cli.command()
@click.option("--plugins", is_flag=True, help="MkDocs-Plugins hinzufügen")
@click.option("--extensions", is_flag=True, help="Markdown-Extensions hinzufügen")
@click.option("--skeleton", is_flag=True, help="Skeleton-Beschreibungen erweitern/erstellen")
@click.option("--restructure", is_flag=True, help="Restrukturierung & Konsolidierung vorschlagen")
@click.option("--llm", is_flag=True, help="KI-Analyse: alle Modelle bewerten mkdocs.yml und schlagen Verbesserungen vor")
@click.option("--all", "do_all", is_flag=True, help="Alles erweitern")
@click.pass_context
def enhance(ctx: click.Context, plugins: bool, extensions: bool, skeleton: bool, restructure: bool, llm: bool, do_all: bool) -> None:
    """Enhance mkdocs.yml, plugins, extensions and skeleton content.

    Can be run iteratively — only adds what is not yet present.
    """
    config_path = ctx.obj["config_path"]
    config = load_config(config_path)
    auto = ctx.obj["auto"]
    output_dir = config.project.output_dir
    mkdocs_path = output_dir / "mkdocs.yml"

    if do_all:
        plugins = extensions = skeleton = restructure = llm = True

    # If nothing specified, default to interactive selection
    if not plugins and not extensions and not skeleton and not restructure and not llm:
        if auto:
            plugins = extensions = skeleton = True
        else:
            click.echo("Was soll erweitert werden?\n")
            click.echo("  1. MkDocs-Plugins hinzufügen")
            click.echo("  2. Markdown-Extensions hinzufügen")
            click.echo("  3. Skeleton-Beschreibungen erweitern")
            click.echo("  4. Restrukturierung & Konsolidierung")
            click.echo("  5. KI-Analyse (alle Modelle bewerten Dokumentation)")
            click.echo("  6. Alles")
            click.echo()
            choice = click.prompt("Auswahl (Komma-getrennt, z.B. 1,3)", default="6")
            choices = {c.strip() for c in choice.split(",")}
            if "6" in choices:
                plugins = extensions = skeleton = restructure = llm = True
            else:
                plugins = "1" in choices
                extensions = "2" in choices
                skeleton = "3" in choices
                restructure = "4" in choices
                llm = "5" in choices

    from .generator.mkdocs_enhancer import (
        enhance_mkdocs_config,
        get_available_plugins,
        get_available_extensions,
        get_pip_requirements,
    )

    # ── Plugins & Extensions ──────────────────────────────────────
    if (plugins or extensions) and mkdocs_path.exists():
        import yaml
        with open(mkdocs_path, "r", encoding="utf-8") as f:
            current = yaml.safe_load(f) or {}

        selected_plugins = None
        selected_extensions = None

        if plugins and not auto:
            avail = get_available_plugins(current)
            if avail:
                click.echo("\nVerfügbare Plugins:")
                for i, p in enumerate(avail, 1):
                    click.echo(f"  {i}. {p['name']} — {p['description']}")
                sel = click.prompt("Welche hinzufügen? (Nummern komma-getrennt, 'a'=alle)", default="a")
                if sel.strip().lower() == "a":
                    selected_plugins = [p["name"] for p in avail]
                else:
                    indices = {int(s.strip()) for s in sel.split(",") if s.strip().isdigit()}
                    selected_plugins = [avail[i - 1]["name"] for i in indices if 1 <= i <= len(avail)]
            else:
                click.echo("Alle verfügbaren Plugins sind bereits aktiv.")

        if extensions and not auto:
            avail = get_available_extensions(current)
            if avail:
                click.echo("\nVerfügbare Extensions:")
                for i, e in enumerate(avail, 1):
                    click.echo(f"  {i}. {e['name']} — {e['description']}")
                sel = click.prompt("Welche hinzufügen? (Nummern komma-getrennt, 'a'=alle)", default="a")
                if sel.strip().lower() == "a":
                    selected_extensions = [e["name"] for e in avail]
                else:
                    indices = {int(s.strip()) for s in sel.split(",") if s.strip().isdigit()}
                    selected_extensions = [avail[i - 1]["name"] for i in indices if 1 <= i <= len(avail)]
            else:
                click.echo("Alle verfügbaren Extensions sind bereits aktiv.")

        result = enhance_mkdocs_config(
            mkdocs_path,
            plugins=plugins,
            extensions=extensions,
            plugin_names=selected_plugins,
            extension_names=selected_extensions,
        )

        if result["plugins"]:
            click.echo(f"\nHinzugefügte Plugins: {', '.join(result['plugins'])}")
            pip_pkgs = get_pip_requirements(result["plugins"])
            if pip_pkgs:
                click.echo(f"Benötigte pip-Pakete: {' '.join(pip_pkgs)}")
                if auto or click.confirm("Jetzt installieren?", default=True):
                    import subprocess
                    subprocess.run([sys.executable, "-m", "pip", "install"] + pip_pkgs)
        if result["extensions"]:
            click.echo(f"Hinzugefügte Extensions: {', '.join(result['extensions'])}")

        if not result["plugins"] and not result["extensions"]:
            click.echo("Keine neuen Plugins/Extensions hinzugefügt (alles bereits aktiv).")
    elif (plugins or extensions) and not mkdocs_path.exists():
        click.echo(f"mkdocs.yml nicht gefunden unter {mkdocs_path}. Zuerst 'generate' oder 'run' ausführen.")

    # ── Skeleton ──────────────────────────────────────────────────
    if skeleton:
        from .generator.skeleton_builder import create_skeleton, create_suggestion_files

        created = create_skeleton(output_dir, config.project.name)
        if created:
            click.echo(f"\nSkeleton: {len(created)} neue Dateien erstellt")
        else:
            click.echo("\nSkeleton: Alle Dateien existieren bereits")

        # Also create suggestion files if any are stored
        if config.preferences.skeleton_suggestions:
            sugg_created = create_suggestion_files(output_dir, config.preferences.skeleton_suggestions)
            if sugg_created:
                click.echo(f"Vorschläge: {len(sugg_created)} zusätzliche Dateien erstellt")

        # Regenerate mkdocs.yml nav to include new files
        if mkdocs_path.exists():
            from .generator.mkdocs_builder import write_mkdocs_config
            write_mkdocs_config(config, output_dir)
            click.echo("mkdocs.yml Navigation aktualisiert")

    # ── Restructure ───────────────────────────────────────────────
    if restructure:
        _run_restructure(config, output_dir, auto)

    # ── LLM Enhancement ──────────────────────────────────────────
    if llm:
        _run_llm_enhance_cli(config, output_dir, auto)

    click.echo("\nFertig.")


def _run_llm_enhance_cli(config, output_dir: Path, auto: bool) -> None:
    """Run KI-gesteuerte Verbesserung via CLI."""
    mkdocs_path = output_dir / "mkdocs.yml"
    if not mkdocs_path.exists():
        click.echo(f"mkdocs.yml nicht gefunden unter {mkdocs_path}. Zuerst 'init' ausführen.")
        return

    slaves = config.preferences.selected_analysts
    master = config.preferences.selected_judge
    if not slaves:
        click.echo("Keine Modelle konfiguriert. Zuerst 'discover' ausführen.")
        return

    click.echo(f"\n--- KI-gesteuerte Verbesserung ---")
    click.echo(f"Modelle: {', '.join(slaves)}")
    if master:
        click.echo(f"Master: {master}")

    from .generator.llm_enhancer import run_llm_enhancement
    from .orchestrator.opencode_runner import configure_http_fallback
    from .orchestrator.semaphore import WorkerPool

    def print_progress(completed: int, total: int, model_id: str, status: str) -> None:
        click.echo(f"  [{completed}/{total}] {status}" + (f" ({model_id})" if model_id else ""))

    pool = WorkerPool(max_workers=3)
    changes = asyncio.run(run_llm_enhancement(
        config=config,
        slaves=slaves,
        master=master,
        pool=pool,
        progress_cb=print_progress,
    ))

    if not changes:
        click.echo("Keine Verbesserungsvorschläge erhalten.")
        return

    click.echo(f"\n{len(changes)} Änderungsvorschläge:")
    for i, change in enumerate(changes, 1):
        action = "NEU" if change.is_new_file else "GEÄNDERT"
        click.echo(f"  {i}. [{action}] {change.file_path}")
        if change.description:
            click.echo(f"     {change.description}")

    if auto:
        click.echo("\nAuto-Modus: Alle Änderungen werden angewendet...")
        applied = 0
        for change in changes:
            if change.apply():
                applied += 1
                click.echo(f"  ✓ {change.file_path}")
            else:
                click.echo(f"  ✗ {change.file_path}")
        click.echo(f"\n{applied}/{len(changes)} Änderungen angewendet.")
    else:
        if click.confirm("\nAlle Änderungen anwenden?", default=True):
            applied = 0
            for change in changes:
                if change.apply():
                    applied += 1
                    click.echo(f"  ✓ {change.file_path}")
                else:
                    click.echo(f"  ✗ {change.file_path}")
            click.echo(f"\n{applied}/{len(changes)} Änderungen angewendet.")
        else:
            click.echo("Keine Änderungen angewendet.")


def _run_restructure(config, output_dir: Path, auto: bool) -> None:
    """Analyze existing docs and suggest restructuring/consolidation."""
    docs_dir = output_dir / "docs"
    if not docs_dir.exists():
        click.echo("Kein docs/-Verzeichnis gefunden. Zuerst Skeleton erstellen.")
        return

    # Collect all markdown files with their sizes
    md_files: list[tuple[Path, int]] = []
    for md in sorted(docs_dir.rglob("*.md")):
        size = md.stat().st_size
        md_files.append((md, size))

    if not md_files:
        click.echo("Keine Markdown-Dateien gefunden.")
        return

    click.echo(f"\n--- Restrukturierung & Konsolidierung ---")
    click.echo(f"Analysiere {len(md_files)} Markdown-Dateien...\n")

    # Detect issues
    suggestions: list[str] = []

    # 1. Empty or near-empty files
    empty_files = [(p, s) for p, s in md_files if s < 100]
    if empty_files:
        suggestions.append(
            f"  • {len(empty_files)} fast leere Dateien (<100 Bytes) gefunden — "
            f"könnten konsolidiert oder entfernt werden:\n" +
            "\n".join(f"    - {p.relative_to(docs_dir)} ({s}B)" for p, s in empty_files[:10])
        )

    # 2. Very large files that could be split
    large_files = [(p, s) for p, s in md_files if s > 50000]
    if large_files:
        suggestions.append(
            f"  • {len(large_files)} sehr große Dateien (>50KB) — "
            f"könnten in Unterseiten aufgeteilt werden:\n" +
            "\n".join(f"    - {p.relative_to(docs_dir)} ({s // 1024}KB)" for p, s in large_files)
        )

    # 3. Directories with only one file (could be flattened)
    dirs_with_files: dict[Path, list[Path]] = {}
    for p, _ in md_files:
        parent = p.parent
        if parent != docs_dir:
            dirs_with_files.setdefault(parent, []).append(p)
    single_file_dirs = [d for d, files in dirs_with_files.items() if len(files) == 1]
    if single_file_dirs:
        suggestions.append(
            f"  • {len(single_file_dirs)} Verzeichnisse mit nur einer Datei — "
            f"könnten nach oben verschoben werden:\n" +
            "\n".join(f"    - {d.relative_to(docs_dir)}/" for d in single_file_dirs[:10])
        )

    # 4. Duplicate-looking titles
    from collections import Counter
    titles: list[str] = []
    for p, _ in md_files:
        try:
            first_line = p.read_text(encoding="utf-8").split("\n", 1)[0]
            if first_line.startswith("# "):
                titles.append(first_line[2:].strip())
        except Exception:
            pass
    title_counts = Counter(titles)
    duplicates = {t: c for t, c in title_counts.items() if c > 1}
    if duplicates:
        suggestions.append(
            f"  • {len(duplicates)} doppelte Titel gefunden — eventuell zusammenführen:\n" +
            "\n".join(f"    - \"{t}\" ({c}x)" for t, c in duplicates.items())
        )

    # 5. Deep nesting (>3 levels)
    deep_files = [(p, len(p.relative_to(docs_dir).parts)) for p, _ in md_files
                  if len(p.relative_to(docs_dir).parts) > 4]
    if deep_files:
        suggestions.append(
            f"  • {len(deep_files)} tief verschachtelte Dateien (>4 Ebenen) — "
            f"flachere Struktur empfohlen:\n" +
            "\n".join(f"    - {p.relative_to(docs_dir)} ({d} Ebenen)" for p, d in deep_files[:10])
        )

    if suggestions:
        click.echo("Vorschläge zur Restrukturierung:\n")
        for s in suggestions:
            click.echo(s)
            click.echo()

        if not auto:
            click.echo("Diese Analyse dient als Empfehlung. Änderungen müssen manuell oder")
            click.echo("über den Chat-Modus (TUI) umgesetzt werden.")
    else:
        click.echo("Keine Restrukturierung nötig — die Dokumentation sieht gut strukturiert aus.")


def main() -> None:
    """Main entry point."""
    cli(obj={})


if __name__ == "__main__":
    main()
