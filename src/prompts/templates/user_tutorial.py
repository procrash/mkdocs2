"""Prompt template for user tutorial generation."""
from ..registry import register
from . import format_guideline_section


@register("user", "tutorials")
def render(ctx) -> str:
    guideline_section = format_guideline_section(ctx)

    return f"""Erstelle ein Schritt-für-Schritt Tutorial basierend auf dem folgenden Code.
{guideline_section}

## Anforderungen:
1. **Titel**: Klarer, aktionsorientierter Titel
2. **Voraussetzungen**: Was muss der User vorher gemacht haben?
3. **Ablauf-Übersicht**: Erstelle ein Mermaid flowchart das den gesamten Tutorial-Ablauf als Übersicht zeigt (Schritte als Knoten, Entscheidungen als Rauten)
4. **Schritte**: Nummerierte Schritte mit klaren Anweisungen
5. **Erwartetes Ergebnis**: Was sieht der User nach jedem Schritt?
6. **Troubleshooting**: Häufige Probleme - erstelle ein Mermaid flowchart für die Fehlerdiagnose (Problem → Lösung)

Keine Code-Blöcke. Benutze Screenshots-Platzhalter wo nötig: `[Screenshot: Beschreibung]`
WICHTIG: Nutze Mermaid-Diagramme (```mermaid) um Abläufe visuell darzustellen. Halte die Diagramme einfach und übersichtlich.

## Code-Kontext:
```{ctx.language}
{ctx.code_content}
```"""
