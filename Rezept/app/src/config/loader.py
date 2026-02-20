"""Load and validate configuration from YAML files."""
from __future__ import annotations
import logging
from pathlib import Path
from typing import Optional

import yaml

from .schema import AppConfig

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = Path("config.yaml")


def load_config(config_path: Optional[Path] = None) -> AppConfig:
    """Load configuration from YAML file with validation and defaults."""
    path = config_path or DEFAULT_CONFIG_PATH
    if not path.exists():
        logger.warning("Config file %s not found, using defaults", path)
        return AppConfig()

    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    config = AppConfig.model_validate(raw)
    logger.info("Configuration loaded from %s", path)
    return config


def save_config(config: AppConfig, config_path: Optional[Path] = None) -> None:
    """Save configuration to YAML file."""
    path = config_path or DEFAULT_CONFIG_PATH
    data = config.model_dump(mode="json")
    # Convert Path objects to strings for YAML serialization
    _convert_paths(data)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    logger.info("Configuration saved to %s", path)


def _convert_paths(data: dict) -> None:
    """Recursively convert Path-like values to strings."""
    for key, value in data.items():
        if isinstance(value, dict):
            _convert_paths(value)
        elif isinstance(value, Path):
            data[key] = str(value)
