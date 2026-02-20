"""Tests for configuration loading and validation."""
import tempfile
from pathlib import Path

import pytest
import yaml

from src.config.loader import load_config, save_config
from src.config.schema import AppConfig, ProjectConfig, ServerConfig


def test_default_config():
    """Test that default config is valid."""
    config = AppConfig()
    assert config.project.name == "MyProject Documentation"
    assert config.system.parallel_workers == 3
    assert config.output.mkdocs_theme == "material"


def test_load_missing_config():
    """Test loading a non-existent config returns defaults."""
    config = load_config(Path("/nonexistent/config.yaml"))
    assert isinstance(config, AppConfig)
    assert config.project.name == "MyProject Documentation"


def test_load_valid_config():
    """Test loading a valid YAML config."""
    data = {
        "project": {"name": "TestProject", "languages": ["python"]},
        "system": {"mock_mode": True, "parallel_workers": 5},
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(data, f)
        f.flush()
        config = load_config(Path(f.name))

    assert config.project.name == "TestProject"
    assert config.project.languages == ["python"]
    assert config.system.mock_mode is True
    assert config.system.parallel_workers == 5
    # Defaults still apply
    assert config.output.latex_enabled is True
    Path(f.name).unlink()


def test_save_and_load_config():
    """Test save then load roundtrip."""
    config = AppConfig()
    config.project.name = "RoundTrip Test"
    config.system.mock_mode = True

    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "test_config.yaml"
        save_config(config, path)
        assert path.exists()

        loaded = load_config(path)
        assert loaded.project.name == "RoundTrip Test"
        assert loaded.system.mock_mode is True


def test_env_var_resolution():
    """Test that ${ENV_VAR} syntax is resolved."""
    import os
    os.environ["TEST_API_KEY_12345"] = "secret123"
    config = AppConfig(server=ServerConfig(api_key="${TEST_API_KEY_12345}"))
    assert config.server.api_key == "secret123"
    del os.environ["TEST_API_KEY_12345"]


def test_stakeholder_defaults():
    """Test stakeholder default configuration."""
    config = AppConfig()
    assert config.stakeholders.developer.enabled is True
    assert "classes" in config.stakeholders.developer.doc_types
    assert config.stakeholders.api.enabled is True
    assert config.stakeholders.user.enabled is True
