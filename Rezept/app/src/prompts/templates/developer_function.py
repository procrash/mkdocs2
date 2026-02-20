"""Prompt template for function documentation (developer stakeholder)."""
from ..registry import register


@register("developer", "functions")
def render(ctx) -> str:
    doxygen = ""
    if ctx.doxygen_section:
        doxygen = f"\n## Vorhandene Doxygen-Dokumentation:\n{ctx.doxygen_section}\n"

    sig = ctx.function_signature or "(see code below)"
    return f"""Dokumentiere die folgende {ctx.language}-Funktion technisch präzise.

## Format:
### `{sig}`
**Zweck**: (1 Satz)
**Parameter**:
| Name | Typ | Default | Beschreibung |
|---|---|---|---|
**Rückgabe**: Typ und Beschreibung
**Exceptions**: Welche und wann
**Komplexität**: O-Notation falls relevant
**Mathematik**: LaTeX-Formeln falls Berechnungen enthalten ($...$)
**Ablaufdiagramm**: Erstelle ein Mermaid flowchart das den Ablauf der Funktion zeigt (Entscheidungen, Schleifen, Rückgabewerte). Verwende ```mermaid als Code-Block-Sprache.
**Beispiel**:
```{ctx.language}
// Beispiel-Aufruf
```
{doxygen}
## Code:
```{ctx.language}
{ctx.code_content}
```"""
