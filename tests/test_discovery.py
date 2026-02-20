"""Tests for server discovery and model classification."""
import pytest

from src.discovery.model_classifier import (
    ClassifiedModel,
    ModelCapability,
    classify_model,
    classify_models,
)
from src.discovery.role_assigner import assign_roles, RoleAssignment
from src.discovery.opencode_configurator import generate_opencode_config


class TestModelClassifier:
    def test_classify_code_model(self):
        result = classify_model("deepseek-coder-33b")
        assert ModelCapability.CODE_FOCUSED in result.capabilities

    def test_classify_large_model(self):
        result = classify_model("llama3-70b")
        assert result.size_class == "large"
        assert ModelCapability.CODE_FOCUSED in result.capabilities

    def test_classify_tool_use_model(self):
        result = classify_model("qwen2.5-72b")
        assert ModelCapability.TOOL_USE in result.capabilities
        assert ModelCapability.LONG_CONTEXT in result.capabilities

    def test_classify_vision_model(self):
        result = classify_model("llava-13b")
        assert ModelCapability.VISION in result.capabilities

    def test_classify_unknown_model(self):
        result = classify_model("some-tiny-model-1b")
        assert ModelCapability.BASIC in result.capabilities
        assert result.size_class == "small"

    def test_classify_multiple(self):
        results = classify_models(["llama3-70b", "mixtral-8x7b", "phi-2"])
        assert len(results) == 3


    def test_classify_with_detected_context(self):
        """Server-detected context length should override heuristic."""
        result = classify_model("some-tiny-model-1b", detected_context=131072)
        assert result.estimated_context == 131072
        assert ModelCapability.LONG_CONTEXT in result.capabilities

    def test_classify_detected_context_zero_uses_heuristic(self):
        """detected_context=0 should fall back to heuristic."""
        result = classify_model("qwen2.5-72b", detected_context=0)
        assert result.estimated_context == 65536  # heuristic for long_context pattern

    def test_classify_models_with_detected_map(self):
        """classify_models should pass detected contexts through."""
        ctx_map = {"model-a": 8192, "model-b": 65536}
        results = classify_models(["model-a", "model-b", "model-c"], ctx_map)
        assert results[0].estimated_context == 8192
        assert results[1].estimated_context == 65536
        assert results[2].estimated_context == 4096  # default heuristic for unknown


class TestRoleAssigner:
    def test_single_model(self):
        models = [ClassifiedModel(id="test-model")]
        assignment = assign_roles(models)
        assert len(assignment.analysts) == 1
        assert assignment.judge is None

    def test_two_models(self):
        models = [
            ClassifiedModel(id="large-70b", size_class="large",
                          capabilities=[ModelCapability.CODE_FOCUSED, ModelCapability.TOOL_USE]),
            ClassifiedModel(id="small-7b", size_class="small",
                          capabilities=[ModelCapability.BASIC]),
        ]
        assignment = assign_roles(models)
        assert assignment.judge is not None
        assert assignment.judge.id == "large-70b"
        assert len(assignment.analysts) == 1

    def test_three_models(self):
        models = [
            ClassifiedModel(id="model-a", size_class="large",
                          capabilities=[ModelCapability.TOOL_USE]),
            ClassifiedModel(id="model-b", size_class="medium",
                          capabilities=[ModelCapability.CODE_FOCUSED]),
            ClassifiedModel(id="model-c", size_class="small",
                          capabilities=[ModelCapability.BASIC]),
        ]
        assignment = assign_roles(models)
        assert assignment.judge is not None
        assert len(assignment.analysts) == 2

    def test_no_models(self):
        assignment = assign_roles([])
        assert len(assignment.analysts) == 0
        assert assignment.judge is None


class TestOpenCodeConfigurator:
    def test_generate_config(self):
        assignment = RoleAssignment(
            analysts=[
                ClassifiedModel(id="model-a", capabilities=[ModelCapability.CODE_FOCUSED]),
            ],
            judge=ClassifiedModel(id="model-b", capabilities=[ModelCapability.TOOL_USE]),
        )
        config = generate_opencode_config(assignment, "http://localhost:11434")
        assert "provider" in config
        assert "local-server" in config["provider"]
        assert "models" in config["provider"]["local-server"]
