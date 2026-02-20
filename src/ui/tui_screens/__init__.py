"""TUI screen package for mkdocsOnSteroids multi-screen workflow."""
from .welcome_screen import WelcomeScreen
from .discovery_screen import DiscoveryScreen
from .model_selection_screen import ModelSelectionScreen
from .skeleton_screen import SkeletonScreen
from .skeleton_suggestions_screen import SkeletonSuggestionsScreen
from .generation_screen import GenerationScreen
from .failure_screen import FailureScreen
from .chat_screen import ChatScreen

__all__ = [
    "WelcomeScreen",
    "DiscoveryScreen",
    "ModelSelectionScreen",
    "SkeletonScreen",
    "SkeletonSuggestionsScreen",
    "GenerationScreen",
    "FailureScreen",
    "ChatScreen",
]
