"""Prompt template for API schema/data model documentation."""
from ..registry import register
from . import format_guideline_section


@register("api", "schemas")
def render(ctx) -> str:
    guideline_section = format_guideline_section(ctx)

    return f"""Dokumentiere das folgende Datenmodell/Schema für eine API-Referenz.
{guideline_section}

## Anforderungen:
1. **Schema-Name und Zweck**
2. **Felder-Tabelle**: | Feld | Typ | Required | Beschreibung | Constraints |
3. **JSON-Beispiel**: Valides Beispiel-Objekt
4. **Entity-Relationship-Diagramm**: Erstelle ein Mermaid erDiagram das die Beziehungen zwischen diesem Schema und verwandten Schemas zeigt
5. **Klassendiagramm**: Erstelle ein Mermaid classDiagram mit allen Feldern und Typen
6. **Validierungsregeln**: Min/Max, Patterns, Enums

WICHTIG: Nutze Mermaid-Diagramme (```mermaid) um Schema-Strukturen und Beziehungen visuell darzustellen.

## Code:
```{ctx.language}
{ctx.code_content}
```"""
