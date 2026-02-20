"""Enhance mkdocs.yml with additional plugins, extensions, and skeleton content.

Designed to be run **iteratively** — only adds what is not yet present.
"""
from __future__ import annotations
import logging
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

# ── Available Plugins ────────────────────────────────────────────────

AVAILABLE_PLUGINS: dict[str, dict[str, Any]] = {
    "git-revision-date-localized": {
        "pip": "mkdocs-git-revision-date-localized-plugin",
        "config": {"git-revision-date-localized": {"enable_creation_date": True}},
        "description": "Zeigt Erstellungs- und Änderungsdatum pro Seite",
    },
    "minify": {
        "pip": "mkdocs-minify-plugin",
        "config": {"minify": {"minify_html": True}},
        "description": "HTML/CSS/JS minifizieren für schnellere Ladezeiten",
    },
    "print-site": {
        "pip": "mkdocs-print-site-plugin",
        "config": {"print-site": {}},
        "description": "Druckbare Gesamtseite aller Dokumente",
    },
    "glightbox": {
        "pip": "mkdocs-glightbox",
        "config": {"glightbox": {}},
        "description": "Bild-Lightbox — Bilder per Klick vergrößern",
    },
}

# ── Available Markdown Extensions ────────────────────────────────────

AVAILABLE_EXTENSIONS: dict[str, dict[str, Any]] = {
    "pymdownx.emoji": {
        "config": {
            "pymdownx.emoji": {
                "emoji_index": "!!python/name:material.extensions.emoji.twemoji",
                "emoji_generator": "!!python/name:material.extensions.emoji.to_svg",
            }
        },
        "description": "Emoji-Support (:smile:, :rocket:, etc.)",
    },
    "footnotes": {
        "config": "footnotes",
        "description": "Fußnoten-Syntax ([^1])",
    },
    "abbr": {
        "config": "abbr",
        "description": "Abkürzungen mit Tooltip (*[API]: Application Programming Interface)",
    },
    "pymdownx.keys": {
        "config": "pymdownx.keys",
        "description": "Tastenkürzel-Darstellung (++ctrl+c++)",
    },
    "pymdownx.mark": {
        "config": "pymdownx.mark",
        "description": "Markierter/hervorgehobener Text (==markiert==)",
    },
    "pymdownx.smartsymbols": {
        "config": "pymdownx.smartsymbols",
        "description": "Smarte Symbole (→, ←, ©, ™, etc.)",
    },
}


# ── Helpers ──────────────────────────────────────────────────────────


def _get_active_plugin_names(mkdocs_config: dict) -> set[str]:
    """Return set of currently active plugin names."""
    plugins = mkdocs_config.get("plugins", [])
    names: set[str] = set()
    for p in plugins:
        if isinstance(p, str):
            names.add(p)
        elif isinstance(p, dict):
            names.update(p.keys())
    return names


def _get_active_extension_names(mkdocs_config: dict) -> set[str]:
    """Return set of currently active extension names."""
    extensions = mkdocs_config.get("markdown_extensions", [])
    names: set[str] = set()
    for e in extensions:
        if isinstance(e, str):
            names.add(e)
        elif isinstance(e, dict):
            names.update(e.keys())
    return names


# ── Public API ───────────────────────────────────────────────────────


def get_available_plugins(mkdocs_config: dict) -> list[dict[str, str]]:
    """Return plugins that can be added (not yet active)."""
    active = _get_active_plugin_names(mkdocs_config)
    result = []
    for name, info in AVAILABLE_PLUGINS.items():
        if name not in active:
            result.append({"name": name, "description": info["description"], "pip": info["pip"]})
    return result


def get_available_extensions(mkdocs_config: dict) -> list[dict[str, str]]:
    """Return extensions that can be added (not yet active)."""
    active = _get_active_extension_names(mkdocs_config)
    result = []
    for name, info in AVAILABLE_EXTENSIONS.items():
        if name not in active:
            result.append({"name": name, "description": info["description"]})
    return result


def apply_plugins(mkdocs_config: dict, plugin_names: list[str] | None = None) -> list[str]:
    """Add plugins to mkdocs config. Returns list of actually added plugin names.

    If *plugin_names* is None, adds all available plugins.
    """
    active = _get_active_plugin_names(mkdocs_config)
    plugins_list = mkdocs_config.setdefault("plugins", [])
    added: list[str] = []

    targets = plugin_names if plugin_names is not None else list(AVAILABLE_PLUGINS.keys())
    for name in targets:
        if name in active or name not in AVAILABLE_PLUGINS:
            continue
        cfg = AVAILABLE_PLUGINS[name]["config"]
        if isinstance(cfg, dict):
            plugins_list.append(cfg)
        else:
            plugins_list.append(name)
        added.append(name)
        logger.info("Added plugin: %s", name)

    return added


def apply_extensions(mkdocs_config: dict, extension_names: list[str] | None = None) -> list[str]:
    """Add markdown extensions to mkdocs config. Returns list of actually added names.

    If *extension_names* is None, adds all available extensions.
    """
    active = _get_active_extension_names(mkdocs_config)
    ext_list = mkdocs_config.setdefault("markdown_extensions", [])
    added: list[str] = []

    targets = extension_names if extension_names is not None else list(AVAILABLE_EXTENSIONS.keys())
    for name in targets:
        if name in active or name not in AVAILABLE_EXTENSIONS:
            continue
        cfg = AVAILABLE_EXTENSIONS[name]["config"]
        if isinstance(cfg, dict):
            ext_list.append(cfg)
        else:
            ext_list.append(name)
        added.append(name)
        logger.info("Added extension: %s", name)

    return added


def enhance_mkdocs_config(
    mkdocs_path: Path,
    plugins: bool = True,
    extensions: bool = True,
    plugin_names: list[str] | None = None,
    extension_names: list[str] | None = None,
) -> dict[str, list[str]]:
    """Read mkdocs.yml, add plugins/extensions, write back. Returns what was added.

    Idempotent — safe to call multiple times.
    """
    if not mkdocs_path.exists():
        logger.error("mkdocs.yml not found at %s", mkdocs_path)
        return {"plugins": [], "extensions": []}

    # Quote !!python/name: tags before safe_load (they crash yaml.safe_load)
    raw = mkdocs_path.read_text(encoding="utf-8")
    raw = raw.replace("!!python/name:", "'!!python/name:")
    # Close the quotes at end of value (before newline)
    import re as _re
    raw = _re.sub(r"('!!python/name:[^\n']+)", r"\1'", raw)
    config = yaml.safe_load(raw) or {}

    added_plugins: list[str] = []
    added_extensions: list[str] = []

    if plugins:
        added_plugins = apply_plugins(config, plugin_names)
    if extensions:
        added_extensions = apply_extensions(config, extension_names)

    if added_plugins or added_extensions:
        with open(mkdocs_path, "w", encoding="utf-8") as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        # Post-process !!python/name: tags
        content = mkdocs_path.read_text(encoding="utf-8")
        content = content.replace(
            "'!!python/name:pymdownx.superfences.fence_code_format'",
            "!!python/name:pymdownx.superfences.fence_code_format",
        )
        content = content.replace(
            "'!!python/name:material.extensions.emoji.twemoji'",
            "!!python/name:material.extensions.emoji.twemoji",
        )
        content = content.replace(
            "'!!python/name:material.extensions.emoji.to_svg'",
            "!!python/name:material.extensions.emoji.to_svg",
        )
        mkdocs_path.write_text(content, encoding="utf-8")

        logger.info("Enhanced mkdocs.yml: +%d plugins, +%d extensions",
                     len(added_plugins), len(added_extensions))

    return {"plugins": added_plugins, "extensions": added_extensions}


def get_pip_requirements(plugin_names: list[str]) -> list[str]:
    """Return pip package names for the given plugins."""
    return [
        AVAILABLE_PLUGINS[name]["pip"]
        for name in plugin_names
        if name in AVAILABLE_PLUGINS and "pip" in AVAILABLE_PLUGINS[name]
    ]
