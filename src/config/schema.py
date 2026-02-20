"""Pydantic v2 models for mkdocsOnSteroids configuration."""
from __future__ import annotations
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class ProjectConfig(BaseModel):
    name: str = "MyProject Documentation"
    source_dir: Path = Path("/src")
    output_dir: Path = Path("/docs")
    repo_url: str = ""
    languages: list[str] = Field(default_factory=lambda: ["cpp", "python"])
    ignore_patterns: list[str] = Field(default_factory=lambda: [
        "*/test/*", "*/build/*", "*/__pycache__/*", "*.generated.*"
    ])


class ServerConfig(BaseModel):
    url: str = "http://host.docker.internal:11434"
    api_key: str = ""
    timeout_connect: int = 10
    timeout_read: int = 60

    @field_validator("api_key", mode="before")
    @classmethod
    def resolve_env_var(cls, v: str) -> str:
        import os
        if isinstance(v, str) and v.startswith("${") and v.endswith("}"):
            env_name = v[2:-1]
            return os.environ.get(env_name, "")
        return v


class SystemConfig(BaseModel):
    global_timeout_seconds: int = 120
    max_retries: int = 3
    retry_base_delay: int = 2
    parallel_workers: int = 3
    mock_mode: bool = False


class ModelConfig(BaseModel):
    id: str
    capabilities: list[str] = Field(default_factory=list)
    max_context: int = 32768


class ModelsConfig(BaseModel):
    analysts: list[ModelConfig] = Field(default_factory=list)
    judge: Optional[ModelConfig] = None


class StakeholderConfig(BaseModel):
    enabled: bool = True
    models: str = "analysts"
    doc_types: list[str] = Field(default_factory=list)


class StakeholdersConfig(BaseModel):
    developer: StakeholderConfig = Field(default_factory=lambda: StakeholderConfig(
        doc_types=["classes", "modules", "functions", "architecture", "diagrams"]
    ))
    api: StakeholderConfig = Field(default_factory=lambda: StakeholderConfig(
        doc_types=["endpoints", "schemas", "examples"]
    ))
    user: StakeholderConfig = Field(default_factory=lambda: StakeholderConfig(
        doc_types=["features", "tutorials", "getting_started"]
    ))


class OutputConfig(BaseModel):
    mkdocs_theme: str = "material"
    latex_enabled: bool = True
    mermaid_enabled: bool = True
    code_copy_enabled: bool = True
    serve_port: int = 8000


class AutomationConfig(BaseModel):
    """Automation mode settings."""
    enabled: bool = False
    auto_start_mkdocs: bool = True
    auto_assign_roles: bool = True


class ModelHealthEntry(BaseModel):
    """Health tracking for a single model."""
    model_id: str
    enabled: bool = True
    replacement_model_id: str = ""
    failure_count: int = 0
    context_length: int = 0            # 0 = unknown, >0 = diagnosed/detected
    detected_capabilities: list[str] = Field(default_factory=list)  # e.g. ["tool_use", "instruct"]


class ModelHealthConfig(BaseModel):
    """Persistent model health data."""
    entries: list[ModelHealthEntry] = Field(default_factory=list)


class SkeletonConfig(BaseModel):
    """Skeleton generation settings."""
    create_before_generation: bool = True


class SkeletonSuggestionEntry(BaseModel):
    """A single LLM-suggested skeleton section."""
    path: str                          # e.g. "docs/getting-started/deployment.md"
    title: str                         # e.g. "Deployment Guide"
    description: str = ""              # Short description of the section
    accepted: bool = False             # User accepted this suggestion


class UserPreferencesConfig(BaseModel):
    """Persistent user preferences - set once, reused across sessions."""
    selected_analysts: list[str] = Field(default_factory=list)
    selected_judge: str = ""
    preferred_port: int = 8000
    start_mkdocs_early: bool = True
    language: str = "de"
    last_server_url: str = ""
    last_source_dir: str = ""
    enhance_mkdocs: bool = True
    skeleton_suggestions: list[SkeletonSuggestionEntry] = Field(default_factory=list)


class ResumeStateConfig(BaseModel):
    """Tracks progress for session resume after interruption."""
    last_screen: str = ""              # Screen name where user left off
    completed_tasks: list[str] = Field(default_factory=list)  # Task IDs already done
    total_tasks: int = 0
    generation_started: bool = False
    generation_finished: bool = False
    skeleton_created: bool = False
    mkdocs_server_started: bool = False
    suggestions_fetched: bool = False


class AppConfig(BaseModel):
    project: ProjectConfig = Field(default_factory=ProjectConfig)
    server: ServerConfig = Field(default_factory=ServerConfig)
    system: SystemConfig = Field(default_factory=SystemConfig)
    models: ModelsConfig = Field(default_factory=ModelsConfig)
    stakeholders: StakeholdersConfig = Field(default_factory=StakeholdersConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)
    automation: AutomationConfig = Field(default_factory=AutomationConfig)
    model_health: ModelHealthConfig = Field(default_factory=ModelHealthConfig)
    skeleton: SkeletonConfig = Field(default_factory=SkeletonConfig)
    preferences: UserPreferencesConfig = Field(default_factory=UserPreferencesConfig)
    resume: ResumeStateConfig = Field(default_factory=ResumeStateConfig)
