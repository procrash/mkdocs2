"""Probe OpenAI-compatible servers for available models."""
from __future__ import annotations
import logging
from dataclasses import dataclass, field

import httpx

logger = logging.getLogger(__name__)


@dataclass
class DiscoveredModel:
    """A model discovered from an OpenAI-compatible API."""
    id: str
    owned_by: str = ""
    object_type: str = "model"
    raw: dict = field(default_factory=dict)


async def probe_server(base_url: str, api_key: str = "", timeout: int = 10) -> list[DiscoveredModel]:
    """Query /v1/models endpoint and return discovered models."""
    url = base_url.rstrip("/")
    if not url.endswith("/v1"):
        url += "/v1"
    models_url = f"{url}/models"

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.get(models_url, headers=headers)
            resp.raise_for_status()
            data = resp.json()
    except httpx.ConnectError:
        logger.error("Cannot connect to %s", models_url)
        return []
    except httpx.HTTPStatusError as exc:
        logger.error("HTTP error from %s: %s", models_url, exc.response.status_code)
        return []
    except Exception as exc:
        logger.error("Error probing %s: %s", models_url, exc)
        return []

    models_list = data.get("data", [])
    result = []
    for m in models_list:
        result.append(DiscoveredModel(
            id=m.get("id", ""),
            owned_by=m.get("owned_by", ""),
            object_type=m.get("object", "model"),
            raw=m,
        ))
    logger.info("Discovered %d models at %s", len(result), models_url)
    return result


async def check_server_health(base_url: str, api_key: str = "", timeout: int = 5) -> bool:
    """Quick health check - can we reach the server?"""
    try:
        models = await probe_server(base_url, api_key, timeout)
        return len(models) > 0
    except Exception:
        return False
