"""Prompt template for module overview (developer stakeholder)."""
from ..registry import register
from . import format_guideline_section


@register("developer", "modules")
def render(ctx) -> str:
    doxygen = ""
    if ctx.doxygen_section:
        doxygen = f"\n## Vorhandene Doxygen-Dokumentation:\n{ctx.doxygen_section}\n"

    guideline_section = format_guideline_section(ctx)

    return f"""Du bist ein Software-Architekt. Erstelle eine Modul-Übersicht für das folgende
{ctx.language}-Modul.
{guideline_section}

## Anforderungen:
1. **Modulzweck**: Was macht dieses Modul? (1-2 Sätze)
2. **Enthaltene Komponenten**: Tabelle mit Klasse/Funktion | Zweck | Zeile
3. **Abhängigkeitsgraph**: Mermaid flowchart der Imports/Dependencies (PFLICHT)
4. **Datenfluss**: Wie fließen Daten durch dieses Modul? Erstelle ein Mermaid flowchart oder sequenceDiagram
5. **Komponentendiagramm**: Mermaid classDiagram mit allen Klassen/Funktionen des Moduls und ihren Beziehungen
6. **Konfiguration**: Welche Einstellungen/Konstanten gibt es?
7. **Bekannte Patterns**: Welche Design Patterns werden verwendet?

WICHTIG: Jedes Modul MUSS mindestens 2 Mermaid-Diagramme enthalten (Abhängigkeitsgraph + Datenfluss oder Klassendiagramm).
Verwende ```mermaid als Code-Block-Sprache.
{doxygen}
## Dateien im Modul:
{ctx.file_listing}

## Code:
```{ctx.language}
{ctx.code_content}
```

Ausgabe ausschließlich in Markdown."""
