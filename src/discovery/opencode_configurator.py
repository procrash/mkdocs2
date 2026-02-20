"""Generate opencode.json configuration file for discovered models."""
from __future__ import annotations
import json
import logging
from pathlib import Path

from .model_classifier import ClassifiedModel, ModelCapability
from .role_assigner import RoleAssignment

logger = logging.getLogger(__name__)


def generate_opencode_config(
    assignment: RoleAssignment,
    server_url: str,
    api_key: str = "",
    output_path: Path | None = None,
) -> dict:
    """Generate opencode.json configuration."""
    all_models = list(assignment.analysts)
    if assignment.judge and assignment.judge not in assignment.analysts:
        all_models.append(assignment.judge)

    models_section = {}
    for model in all_models:
        model_config: dict = {}
        if ModelCapability.TOOL_USE not in model.capabilities:
            model_config["tools"] = False
        models_section[model.id] = model_config

    provider_config: dict = {
        "npm": "@ai-sdk/openai-compatible",
        "options": {
            "baseURL": server_url.rstrip("/") + "/v1" if not server_url.rstrip("/").endswith("/v1") else server_url,
        },
        "models": models_section,
    }
    if api_key:
        provider_config["options"]["apiKey"] = api_key

    config = {
        "provider": {
            "local-server": provider_config,
        }
    }

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        logger.info("opencode.json written to %s", output_path)

    return config


def get_model_provider_id(model: ClassifiedModel) -> str:
    """Get the provider-prefixed model ID for opencode CLI."""
    return f"local-server/{model.id}"
