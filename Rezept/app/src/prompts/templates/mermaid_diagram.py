"""Prompt template for Mermaid diagram generation."""
from ..registry import register


@register("developer", "diagrams")
def render(ctx) -> str:
    return f"""Erstelle ein Mermaid-Diagramm für den folgenden Code.

Diagramm-Typ: {ctx.diagram_type}
Mögliche Typen: classDiagram, flowchart, sequenceDiagram, erDiagram

## Regeln:
1. Nur valides Mermaid-Syntax
2. Klare, lesbare Labels
3. Keine zu tiefen Verschachtelungen (max 3 Ebenen)
4. Farbkodierung wo sinnvoll (:::style)

## Code:
```{ctx.language}
{ctx.code_content}
```

Ausgabe: NUR der Mermaid-Code-Block, kein anderer Text."""
