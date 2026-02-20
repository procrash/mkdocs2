"""Skeleton screen - preview doc structure and optionally start MkDocs."""
from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import (
    Button,
    Checkbox,
    Footer,
    Header,
    Input,
    Label,
    Static,
    Tree,
)

from ...config.schema import AppConfig
from ...generator.mkdocs_server import find_available_port, is_port_available
from ...generator.skeleton_builder import create_skeleton, get_skeleton_tree


class SkeletonScreen(Screen):
    """Preview documentation skeleton and start MkDocs server."""

    CSS = """
    SkeletonScreen {
        align: center middle;
    }
    #skeleton-box {
        width: 90;
        height: auto;
        max-height: 85%;
        border: solid $primary;
        padding: 1 2;
    }
    #tree-container {
        height: 20;
        border: dashed $accent;
        overflow-y: auto;
    }
    #options-section {
        margin-top: 1;
        padding: 1;
    }
    .port-row {
        height: 3;
    }
    #btn-row {
        margin-top: 1;
        align: center middle;
        height: 5;
    }
    #btn-row Button {
        margin: 0 2;
    }
    """

    BINDINGS = [
        ("escape", "go_back", "Zurück"),
    ]

    def __init__(self, config: AppConfig):
        super().__init__()
        self.config = config

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        preferred_port = self.config.preferences.preferred_port
        if not is_port_available(preferred_port):
            preferred_port = find_available_port(preferred_port)

        with Center():
            with Vertical(id="skeleton-box"):
                yield Label("[bold]Dokumentations-Skelett[/bold]")
                yield Label("Folgende Verzeichnisstruktur wird erstellt:")

                yield Tree("docs/", id="skeleton-tree")

                with Vertical(id="options-section"):
                    yield Checkbox(
                        "MkDocs-Server jetzt starten (Live-Vorschau)",
                        value=self.config.preferences.start_mkdocs_early,
                        id="start-mkdocs-check",
                    )
                    with Horizontal(classes="port-row"):
                        yield Label("Port: ")
                        yield Input(
                            value=str(preferred_port),
                            placeholder="8000",
                            id="port-input",
                            max_length=5,
                        )

                with Horizontal(id="btn-row"):
                    yield Button("← Zurück", variant="default", id="btn-back")
                    yield Button("Skelett erstellen & Weiter →", variant="primary", id="btn-next")
        yield Footer()

    def on_mount(self) -> None:
        tree = self.query_one("#skeleton-tree", Tree)
        tree.root.expand()
        self._populate_tree(tree)

    def _populate_tree(self, tree_widget: Tree) -> None:
        """Populate tree with planned skeleton structure."""
        from ...generator.skeleton_builder import DEFAULT_SKELETON

        # Build nested tree from flat paths
        nodes: dict[str, object] = {}
        root = tree_widget.root

        for rel_path, title, _ in DEFAULT_SKELETON:
            parts = rel_path.split("/")
            current = root
            for i, part in enumerate(parts[:-1]):
                key = "/".join(parts[:i + 1])
                if key not in nodes:
                    nodes[key] = current.add(f"[bold]{part}/[/bold]", expand=True)
                current = nodes[key]
            # Add file leaf
            current.add_leaf(f"{parts[-1]}  [dim]({title})[/dim]")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-back":
            self.dismiss(None)
            return
        if event.button.id == "btn-next":
            start_mkdocs = self.query_one("#start-mkdocs-check", Checkbox).value
            port_input = self.query_one("#port-input", Input)
            try:
                port = int(port_input.value)
            except ValueError:
                port = self.config.preferences.preferred_port

            # Persist preferences
            self.config.preferences.start_mkdocs_early = start_mkdocs
            self.config.preferences.preferred_port = port

            self.dismiss({
                "start_mkdocs": start_mkdocs,
                "port": port,
            })

    def action_go_back(self) -> None:
        self.dismiss(None)
