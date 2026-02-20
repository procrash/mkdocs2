"""Prompt template for API endpoint documentation."""
from ..registry import register
from . import format_guideline_section


@register("api", "endpoints")
def render(ctx) -> str:
    guideline_section = format_guideline_section(ctx)

    return f"""Du dokumentierst eine API für externe Entwickler. Beschreibe NUR die öffentliche
Schnittstelle. Keine Implementierungsdetails.
{guideline_section}

## Anforderungen:
1. **Endpunkt-Übersicht**: Method, Path, Beschreibung
2. **Request**: Headers, Query-Parameter, Body (JSON Schema)
3. **Response**: Status-Codes, Body (JSON Schema), Beispiel
4. **Authentifizierung**: Falls erkennbar
5. **Rate Limits**: Falls erkennbar
6. **Fehler**: Mögliche Fehlercodes mit Beschreibung
7. **cURL Beispiel**: Vollständiges Beispiel
8. **Request/Response-Flow**: Erstelle ein Mermaid sequenceDiagram das den Ablauf eines typischen API-Aufrufs zeigt (Client → Server → Response)
9. **Statuscode-Übersicht**: Erstelle ein Mermaid flowchart das zeigt, welche Bedingungen zu welchen Status-Codes führen

Zielgruppe: Externe Entwickler die diese API integrieren.
Ignoriere interne Implementierungsdetails komplett.
WICHTIG: Nutze Mermaid-Diagramme (```mermaid) um API-Flows visuell darzustellen.

## Code:
```{ctx.language}
{ctx.code_content}
```"""
