"""Prompt template for architecture overview."""
from ..registry import register


@register("developer", "architecture")
def render(ctx) -> str:
    return f"""Du bist ein Software-Architekt. Erstelle eine Architektur-Übersicht für das
gesamte Projekt basierend auf den folgenden Dateien.

## Anforderungen:
1. **System-Übersicht**: High-Level Beschreibung (Mermaid C4 oder flowchart)
2. **Komponentendiagramm**: Mermaid-Diagramm aller Hauptkomponenten
3. **Technologie-Stack**: Tabelle mit Komponente | Technologie | Zweck
4. **Datenfluss**: Wie fließen Daten durch das System? (Mermaid sequence diagram)
5. **Deployment**: Wie wird das System deployed?
6. **Verzeichnisstruktur**: Erklärt

## Projekt-Dateien:
{ctx.file_tree}

## Schlüssel-Dateien:
{ctx.key_files_content}"""
