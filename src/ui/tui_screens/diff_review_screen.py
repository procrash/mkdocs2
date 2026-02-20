"""Diff review screen - preview and approve/reject file changes from LLM implementation."""
from __future__ import annotations
import difflib
import logging
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import (
    Button,
    Checkbox,
    Footer,
    Label,
    Static,
)

logger = logging.getLogger(__name__)


class FileChange:
    """Represents a single file change proposed by the LLM."""

    def __init__(self, file_path: str, new_content: str, description: str = ""):
        self.file_path = file_path
        self.new_content = new_content
        self.description = description
        self.accepted = True  # Default: accepted

    @property
    def is_new_file(self) -> bool:
        return not Path(self.file_path).exists()

    def get_diff(self) -> str:
        """Generate unified diff between current and proposed content."""
        path = Path(self.file_path)
        if path.exists():
            try:
                old_lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
            except Exception:
                old_lines = []
        else:
            old_lines = []

        new_lines = self.new_content.splitlines(keepends=True)

        diff = difflib.unified_diff(
            old_lines, new_lines,
            fromfile=f"a/{path.name}",
            tofile=f"b/{path.name}",
            lineterm="",
        )
        return "\n".join(diff)

    def apply(self) -> bool:
        """Write the new content to disk. Returns True on success."""
        try:
            path = Path(self.file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(self.new_content, encoding="utf-8")
            logger.info("Applied change to %s", self.file_path)
            return True
        except Exception as exc:
            logger.error("Failed to apply change to %s: %s", self.file_path, exc)
            return False


class DiffReviewScreen(ModalScreen):
    """Modal screen to review and approve file changes before applying."""

    CSS = """
    DiffReviewScreen {
        align: center middle;
    }
    #review-box {
        width: 95%;
        height: 90%;
        border: solid $primary;
        padding: 1 2;
        background: $surface;
    }
    #review-header {
        height: 3;
        margin-bottom: 1;
    }
    #changes-scroll {
        height: 1fr;
        border: solid $accent;
    }
    .change-block {
        margin-bottom: 1;
        padding: 1;
        border: dashed $primary;
    }
    .change-header {
        height: 2;
    }
    .diff-view {
        padding: 0 1;
    }
    .diff-add {
        color: $success;
    }
    .diff-del {
        color: $error;
    }
    #btn-row {
        height: 3;
        margin-top: 1;
        align: center middle;
    }
    #summary-label {
        margin-top: 1;
    }
    """

    BINDINGS = [
        ("escape", "cancel", "Abbrechen"),
        ("a", "select_all", "Alle auswählen"),
        ("n", "select_none", "Keine auswählen"),
    ]

    def __init__(self, changes: list[FileChange]):
        super().__init__()
        self.changes = changes

    def compose(self) -> ComposeResult:
        with Vertical(id="review-box"):
            yield Label(
                f"[bold]Änderungsvorschau[/bold] - {len(self.changes)} Dateien betroffen\n"
                f"Wähle aus welche Änderungen angewendet werden sollen.",
                id="review-header",
            )
            with VerticalScroll(id="changes-scroll"):
                for i, change in enumerate(self.changes):
                    with Vertical(classes="change-block"):
                        action = "[green]NEU[/green]" if change.is_new_file else "[yellow]GEÄNDERT[/yellow]"
                        yield Checkbox(
                            f"{action} {change.file_path}",
                            value=change.accepted,
                            id=f"change-{i}",
                            classes="change-header",
                        )
                        if change.description:
                            yield Label(f"  [dim]{change.description}[/dim]")
                        diff_text = self._format_diff(change)
                        yield Static(diff_text, classes="diff-view")

            yield Label("", id="summary-label")
            with Center(id="btn-row"):
                yield Button("Ausgewählte anwenden", variant="primary", id="btn-apply")
                yield Button("Alle ablehnen", variant="error", id="btn-cancel")
        yield Footer()

    def _format_diff(self, change: FileChange) -> str:
        """Format diff with color markup for display."""
        diff = change.get_diff()
        if not diff:
            # New file: show first 30 lines
            lines = change.new_content.splitlines()[:30]
            preview = "\n".join(f"  [green]+{line}[/green]" for line in lines)
            if len(change.new_content.splitlines()) > 30:
                preview += f"\n  [dim]... +{len(change.new_content.splitlines()) - 30} weitere Zeilen[/dim]"
            return preview

        formatted_lines: list[str] = []
        for line in diff.splitlines()[:60]:
            if line.startswith("+") and not line.startswith("+++"):
                formatted_lines.append(f"  [green]{_escape_markup(line)}[/green]")
            elif line.startswith("-") and not line.startswith("---"):
                formatted_lines.append(f"  [red]{_escape_markup(line)}[/red]")
            elif line.startswith("@@"):
                formatted_lines.append(f"  [cyan]{_escape_markup(line)}[/cyan]")
            else:
                formatted_lines.append(f"  {_escape_markup(line)}")

        if len(diff.splitlines()) > 60:
            formatted_lines.append(f"  [dim]... +{len(diff.splitlines()) - 60} weitere Zeilen[/dim]")

        return "\n".join(formatted_lines)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-apply":
            # Collect selections
            for i, change in enumerate(self.changes):
                try:
                    cb = self.query_one(f"#change-{i}", Checkbox)
                    change.accepted = cb.value
                except Exception:
                    pass

            accepted = [c for c in self.changes if c.accepted]
            applied = 0
            failed = 0
            for c in accepted:
                if c.apply():
                    applied += 1
                else:
                    failed += 1

            self.dismiss({
                "applied": applied,
                "failed": failed,
                "total": len(accepted),
                "changes": self.changes,
            })

        elif event.button.id == "btn-cancel":
            self.dismiss({"applied": 0, "failed": 0, "total": 0, "changes": []})

    def action_cancel(self) -> None:
        self.dismiss({"applied": 0, "failed": 0, "total": 0, "changes": []})

    def action_select_all(self) -> None:
        for i in range(len(self.changes)):
            try:
                self.query_one(f"#change-{i}", Checkbox).value = True
            except Exception:
                pass

    def action_select_none(self) -> None:
        for i in range(len(self.changes)):
            try:
                self.query_one(f"#change-{i}", Checkbox).value = False
            except Exception:
                pass


def _escape_markup(text: str) -> str:
    """Escape Rich markup characters in text."""
    return text.replace("[", "\\[").replace("]", "\\]")


def parse_file_changes(llm_output: str, base_dir: str = "") -> list[FileChange]:
    """Parse structured file changes from LLM output.

    Expected format:
    <<<FILE path/to/file.py
    DESCRIPTION: What this change does
    >>>
    file content here
    <<<END>>>

    Also supports:
    ```file:path/to/file.py
    content
    ```
    """
    changes: list[FileChange] = []

    # Format 1: <<<FILE ... <<<END>>>
    import re
    pattern1 = re.compile(
        r'<<<FILE\s+(.+?)\s*\n'
        r'(?:DESCRIPTION:\s*(.+?)\n)?'
        r'>>>\s*\n'
        r'(.*?)\n<<<END>>>',
        re.DOTALL,
    )
    for match in pattern1.finditer(llm_output):
        file_path = match.group(1).strip()
        description = (match.group(2) or "").strip()
        content = match.group(3)
        if base_dir and not file_path.startswith("/"):
            file_path = str(Path(base_dir) / file_path)
        changes.append(FileChange(file_path, content, description))

    if changes:
        return changes

    # Format 2: ```file:path/to/file.py ... ```
    pattern2 = re.compile(
        r'```(?:file:)(.+?)\s*\n(.*?)```',
        re.DOTALL,
    )
    for match in pattern2.finditer(llm_output):
        file_path = match.group(1).strip()
        content = match.group(2)
        if base_dir and not file_path.startswith("/"):
            file_path = str(Path(base_dir) / file_path)
        changes.append(FileChange(file_path, content))

    return changes
