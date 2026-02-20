"""Generate mkdocs.yml from template and configuration."""
from __future__ import annotations
import logging
import re
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
    _unquote_python_name_tags(mkdocs_path)

    # Write mathjax.js helper if LaTeX enabled
    if config.output.latex_enabled:
        _write_mathjax_js(output_dir)

    logger.info("Written mkdocs.yml to %s", mkdocs_path)
    return mkdocs_path


def _unquote_python_name_tags(mkdocs_path: Path) -> None:
    """Remove quotes around !!python/name: tags so MkDocs can resolve them.

    yaml.dump wraps these as '!!python/name:...' or "!!python/name:..."
    but MkDocs needs them unquoted.
    """
    content = mkdocs_path.read_text(encoding="utf-8")
    content = re.sub(
        r"""['"](!!python/name:[a-zA-Z0-9_.]+)['"]""",
        r"\1",
        content,
    )
    mkdocs_path.write_text(content, encoding="utf-8")


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
    """Return a full default MkDocs Material 9.x configuration."""
    return {
        "site_name": "Documentation",
        "site_description": "Auto-generated documentation by mkdocsOnSteroids",
        "theme": {
            "name": "material",
            "language": "de",
            "features": [
                "navigation.tabs",
                "navigation.tabs.sticky",
                "navigation.sections",
                "navigation.expand",
                "navigation.top",
                "navigation.indexes",
                "navigation.instant",
                "navigation.instant.progress",
                "navigation.tracking",
                "navigation.path",
                "navigation.footer",
                "search.suggest",
                "search.highlight",
                "search.share",
                "content.tabs.link",
                "content.code.copy",
                "content.code.annotate",
                "content.code.select",
                "content.tooltips",
                "content.action.edit",
                "content.action.view",
                "toc.follow",
                "header.autohide",
                "announce.dismiss",
            ],
            "palette": [
                {
                    "media": "(prefers-color-scheme: light)",
                    "scheme": "default",
                    "primary": "indigo",
                    "accent": "indigo",
                    "toggle": {"icon": "material/brightness-7", "name": "Dark Mode aktivieren"},
                },
                {
                    "media": "(prefers-color-scheme: dark)",
                    "scheme": "slate",
                    "primary": "indigo",
                    "accent": "indigo",
                    "toggle": {"icon": "material/brightness-4", "name": "Light Mode aktivieren"},
                },
            ],
            "font": {"text": "Roboto", "code": "Roboto Mono"},
            "icon": {"repo": "fontawesome/brands/github"},
        },
        "markdown_extensions": [
            "abbr",
            "admonition",
            "attr_list",
            "def_list",
            "footnotes",
            "md_in_html",
            "tables",
            {"toc": {"permalink": True, "toc_depth": 3}},
            {"pymdownx.arithmatex": {"generic": True}},
            {"pymdownx.betterem": {"smart_enable": "all"}},
            "pymdownx.caret",
            "pymdownx.critic",
            "pymdownx.details",
            {"pymdownx.emoji": {
                "emoji_index": "!!python/name:material.extensions.emoji.twemoji",
                "emoji_generator": "!!python/name:material.extensions.emoji.to_svg",
            }},
            {"pymdownx.highlight": {
                "anchor_linenums": True,
                "line_spans": "__span",
                "pygments_lang_class": True,
                "auto_title": True,
            }},
            "pymdownx.inlinehilite",
            "pymdownx.keys",
            "pymdownx.mark",
            "pymdownx.smartsymbols",
            {"pymdownx.snippets": {
                "auto_append": ["includes/abbreviations.md"],
                "check_paths": False,
            }},
            {"pymdownx.superfences": {
                "custom_fences": [{
                    "name": "mermaid",
                    "class": "mermaid",
                    "format": "!!python/name:pymdownx.superfences.fence_code_format",
                }],
            }},
            {"pymdownx.tabbed": {
                "alternate_style": True,
                "combine_header_slug": True,
                "slugify": "!!python/name:pymdownx.slugs.slugify",
            }},
            {"pymdownx.tasklist": {"custom_checkbox": True}},
            "pymdownx.tilde",
        ],
        "extra_javascript": [
            "javascripts/mathjax.js",
            "https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js",
        ],
        "extra_css": ["stylesheets/extra.css"],
        "plugins": [
            {"search": {"lang": "de", "separator": r"[\s\-\.]+"}},
            {"tags": {"tags_file": "reference/tags.md"}},
            "offline",
        ],
    }
