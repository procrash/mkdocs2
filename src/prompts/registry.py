"""Central registry for all prompt templates."""
from __future__ import annotations
import logging
from typing import Callable

logger = logging.getLogger(__name__)

# Registry: maps (stakeholder, doc_type) -> template render function
_REGISTRY: dict[tuple[str, str], Callable] = {}


def register(stakeholder: str, doc_type: str):
    """Decorator to register a prompt template."""
    def decorator(func: Callable):
        _REGISTRY[(stakeholder, doc_type)] = func
        logger.debug("Registered prompt: %s/%s", stakeholder, doc_type)
        return func
    return decorator


def get_template(stakeholder: str, doc_type: str) -> Callable | None:
    """Get a registered template function."""
    return _REGISTRY.get((stakeholder, doc_type))


def list_templates() -> list[tuple[str, str]]:
    """List all registered (stakeholder, doc_type) pairs."""
    return list(_REGISTRY.keys())


def ensure_loaded():
    """Import all template modules to trigger registration."""
    from .templates import (  # noqa: F401
        developer_class,
        developer_module,
        developer_function,
        api_endpoint,
        api_schema,
        user_feature,
        user_tutorial,
        architecture,
        doxygen_convert,
        mermaid_diagram,
        judge_merge,
        index_page,
    )
