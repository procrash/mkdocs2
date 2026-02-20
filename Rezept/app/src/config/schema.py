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


class AppConfig(BaseModel):
    project: ProjectConfig = Field(default_factory=ProjectConfig)
    server: ServerConfig = Field(default_factory=ServerConfig)
    system: SystemConfig = Field(default_factory=SystemConfig)
    models: ModelsConfig = Field(default_factory=ModelsConfig)
    stakeholders: StakeholdersConfig = Field(default_factory=StakeholdersConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)
