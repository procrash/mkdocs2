"""TUI screen package for mkdocsOnSteroids multi-screen workflow."""
import re


def sanitize_widget_id(raw_id: str) -> str:
    """Make a string safe for use as a Textual widget ID.

    Replaces any character that is not a letter, digit, underscore or hyphen
    with an underscore.  Ensures it doesn't start with a digit.
    """
    safe = re.sub(r"[^a-zA-Z0-9_-]", "_", raw_id)
    if safe and safe[0].isdigit():
        safe = f"m{safe}"
    return safe


from .welcome_screen import WelcomeScreen
from .discovery_screen import DiscoveryScreen
from .model_selection_screen import ModelSelectionScreen
from .skeleton_screen import SkeletonScreen
from .skeleton_suggestions_screen import SkeletonSuggestionsScreen
from .generation_screen import GenerationScreen
from .failure_screen import FailureScreen
from .chat_screen import ChatScreen
from .diff_review_screen import DiffReviewScreen

__all__ = [
    "WelcomeScreen",
    "DiscoveryScreen",
    "ModelSelectionScreen",
    "SkeletonScreen",
    "SkeletonSuggestionsScreen",
    "GenerationScreen",
    "FailureScreen",
    "ChatScreen",
    "DiffReviewScreen",
]
