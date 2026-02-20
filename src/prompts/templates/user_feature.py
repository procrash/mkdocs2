"""Prompt template for user-facing feature documentation."""
from ..registry import register
from . import format_guideline_section


@register("user", "features")
def render(ctx) -> str:
    guideline_section = format_guideline_section(ctx)

    return f"""Erkläre die folgende Software-Funktionalität für Endanwender.
Verwende KEINE Code-Blöcke. Keine technischen Details.
{guideline_section}

## Anforderungen:
1. **Was macht diese Funktion?** (2-3 einfache Sätze)
2. **Wann benutze ich das?** (Anwendungsfälle)
3. **Ablaufdiagramm**: Erstelle ein Mermaid flowchart das den typischen Nutzungsablauf zeigt (einfach und verständlich, keine technischen Details)
4. **Wie benutze ich das?** (Schritt-für-Schritt Anleitung)
5. **Was kann schiefgehen?** (Häufige Probleme und Lösungen)
6. **Tipps & Tricks**

Schreibe in einfacher, verständlicher Sprache. Zielgruppe: Nicht-technische Anwender.
WICHTIG: Nutze mindestens ein Mermaid-Diagramm (```mermaid) um den Ablauf visuell darzustellen. Halte die Diagramme einfach und benutzerfreundlich.

## Kontext:
Funktionalität aus Datei: {ctx.file_path}

## Code (nur zur Analyse, nicht in der Ausgabe verwenden):
```{ctx.language}
{ctx.code_content}
```"""
