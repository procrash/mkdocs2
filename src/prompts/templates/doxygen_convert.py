"""Prompt template for Doxygen to Markdown conversion."""
from ..registry import register


@register("developer", "doxygen")
def render(ctx) -> str:
    return f"""Der folgende Code enthält Doxygen-Kommentare (/** ... */, /// , //!, @param, @return etc.).
Konvertiere diese in modernes Markdown-Format.

## Regeln:
1. @param name desc -> **Parameter `name`**: desc
2. @return desc -> **Returns**: desc
3. @brief desc -> Erste Zeile der Beschreibung
4. @note -> > **Note:** ...
5. @warning -> > **Warning:** ...
6. @see -> **See also**: [link]
7. @deprecated -> > **Deprecated:** ...
8. Formeln in @f$ ... @f$ -> $ ... $ (LaTeX)
9. Code-Beispiele in @code/@endcode -> ```cpp ... ```

Erhalte ALLE Informationen. Füge nichts hinzu, was nicht im Original steht.

## Code mit Doxygen:
```{ctx.language}
{ctx.code_content}
```"""
