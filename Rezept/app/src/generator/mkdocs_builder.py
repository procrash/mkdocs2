"""Generate mkdocs.yml from template and configuration."""
from __future__ import annotations
import logging
from pathlib import Path

import yaml

from ..config.schema import AppConfig
from .nav_builder import build_nav

logger = logging.getLogger(__name__)

TEMPLATE_PATH = Path(__file__).parent.parent.parent / "templates" / "mkdocs_base.yml"


def build_mkdocs_config(config: AppConfig, output_dir: Path) -> dict:
    """Build a complete mkdocs.yml configuration."""
    # Load template
    if TEMPLATE_PATH.exists():
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            mkdocs_config = yaml.safe_load(f) or {}
    else:
        mkdocs_config = _default_mkdocs_config()

    # Apply project settings
    mkdocs_config["site_name"] = config.project.name
    if config.project.repo_url:
        mkdocs_config["repo_url"] = config.project.repo_url

    # Build navigation from actual files
    nav = build_nav(output_dir)
    if nav:
        mkdocs_config["nav"] = nav

    # Apply output settings
    if "theme" not in mkdocs_config:
        mkdocs_config["theme"] = {}
    mkdocs_config["theme"]["name"] = config.output.mkdocs_theme

    # LaTeX support
    if config.output.latex_enabled:
        _ensure_latex_extensions(mkdocs_config)

    # Mermaid support
    if config.output.mermaid_enabled:
        _ensure_mermaid_extensions(mkdocs_config)

    return mkdocs_config


def write_mkdocs_config(config: AppConfig, output_dir: Path) -> Path:
    """Generate and write mkdocs.yml."""
    mkdocs_config = build_mkdocs_config(config, output_dir)

    mkdocs_path = output_dir / "mkdocs.yml"
    with open(mkdocs_path, "w", encoding="utf-8") as f:
        yaml.dump(
            mkdocs_config, f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )

    # Post-process: restore !!python/name: tags that yaml.dump quoted
    content = mkdocs_path.read_text(encoding="utf-8")
    content = content.replace(
        "'!!python/name:pymdownx.superfences.fence_code_format'",
        "!!python/name:pymdownx.superfences.fence_code_format",
    )
    mkdocs_path.write_text(content, encoding="utf-8")

    # Write mathjax.js helper if LaTeX enabled
    if config.output.latex_enabled:
        _write_mathjax_js(output_dir)

    logger.info("Written mkdocs.yml to %s", mkdocs_path)
    return mkdocs_path


def _ensure_latex_extensions(config: dict) -> None:
    """Ensure LaTeX/MathJax extensions are configured."""
    extensions = config.setdefault("markdown_extensions", [])
    arithmatex = {"pymdownx.arithmatex": {"generic": True}}
    if not any("pymdownx.arithmatex" in (e if isinstance(e, dict) else {e: None}) for e in extensions):
        extensions.append(arithmatex)

    extra_js = config.setdefault("extra_javascript", [])
    mathjax_files = [
        "javascripts/mathjax.js",
        "https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js",
    ]
    for js in mathjax_files:
        if js not in extra_js:
            extra_js.append(js)


def _ensure_mermaid_extensions(config: dict) -> None:
    """Ensure Mermaid diagram support is configured."""
    extensions = config.setdefault("markdown_extensions", [])
    superfences_config = {
        "pymdownx.superfences": {
            "custom_fences": [{
                "name": "mermaid",
                "class": "mermaid",
                "format": "!!python/name:pymdownx.superfences.fence_code_format",  # Post-processed on write
            }]
        }
    }
    # Replace existing superfences config or add new
    for i, ext in enumerate(extensions):
        if isinstance(ext, dict) and "pymdownx.superfences" in ext:
            extensions[i] = superfences_config
            return
    extensions.append(superfences_config)


def _write_mathjax_js(output_dir: Path) -> None:
    """Write the MathJax configuration JavaScript file."""
    js_dir = output_dir / "docs" / "javascripts"
    js_dir.mkdir(parents=True, exist_ok=True)
    js_file = js_dir / "mathjax.js"
    js_file.write_text(
        'window.MathJax = {\n'
        '  tex: {\n'
        '    inlineMath: [["$", "$"], ["\\\\(", "\\\\)"]],\n'
        '    displayMath: [["$$", "$$"], ["\\\\[", "\\\\]"]],\n'
        '    processEscapes: true,\n'
        '    processEnvironments: true\n'
        '  },\n'
        '  options: {\n'
        '    ignoreHtmlClass: ".*|",\n'
        '    processHtmlClass: "arithmatex"\n'
        '  }\n'
        '};\n',
        encoding="utf-8",
    )


def _default_mkdocs_config() -> dict:
    """Return a minimal default MkDocs configuration."""
    return {
        "site_name": "Documentation",
        "theme": {
            "name": "material",
            "features": [
                "navigation.tabs",
                "navigation.sections",
                "navigation.expand",
                "navigation.top",
                "search.suggest",
                "search.highlight",
                "content.code.copy",
            ],
            "palette": [
                {
                    "scheme": "default",
                    "primary": "indigo",
                    "accent": "indigo",
                    "toggle": {"icon": "material/brightness-7", "name": "Dark Mode"},
                },
                {
                    "scheme": "slate",
                    "primary": "indigo",
                    "accent": "indigo",
                    "toggle": {"icon": "material/brightness-4", "name": "Light Mode"},
                },
            ],
        },
        "markdown_extensions": [
            "admonition",
            "attr_list",
            "md_in_html",
            "tables",
            {"toc": {"permalink": True}},
            {"pymdownx.highlight": {"anchor_linenums": True}},
            "pymdownx.inlinehilite",
            {"pymdownx.tabbed": {"alternate_style": True}},
            "pymdownx.details",
            {"pymdownx.tasklist": {"custom_checkbox": True}},
        ],
        "plugins": ["search"],
    }
