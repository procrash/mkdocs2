"""Prompt template for class documentation (developer stakeholder)."""
from ..registry import register


@register("developer", "classes")
def render(ctx) -> str:
    doxygen = ""
    if ctx.doxygen_section:
        doxygen = f"\n## Vorhandene Doxygen-Dokumentation:\n{ctx.doxygen_section}\n"

    return f"""Du bist ein Senior Technical Writer. Analysiere die folgende {ctx.language} Klasse und erstelle
eine vollständige technische Dokumentation im Markdown-Format.

## Anforderungen:
1. **Klassenübersicht**: Zweck, Verantwortlichkeiten, Design-Pattern
2. **Konstruktor**: Parameter, Default-Werte, Exceptions
3. **Öffentliche Methoden**: Für jede Methode:
   - Signatur
   - Parameter mit Typen und Beschreibung
   - Rückgabewert
   - Exceptions
   - Beispiel-Aufruf
4. **Klassendiagramm**: Erstelle ein Mermaid classDiagram mit allen Attributen, Methoden und Beziehungen zu anderen Klassen
5. **Sequenzdiagramm**: Falls die Klasse komplexe Interaktionen hat, erstelle ein Mermaid sequenceDiagram für den wichtigsten Ablauf
6. **Mathematische Formeln**: Falls der Code mathematische Berechnungen enthält,
   dokumentiere die Formeln in LaTeX-Notation ($...$)
7. **Abhängigkeiten**: Welche anderen Klassen/Module werden verwendet
8. **Thread-Safety**: Falls relevant

WICHTIG: Nutze Mermaid-Diagramme großzügig! Jede Klasse MUSS mindestens ein classDiagram haben.
Verwende ```mermaid als Code-Block-Sprache.
{doxygen}
## Code:
Datei: {ctx.file_path}
```{ctx.language}
{ctx.code_content}
```

Ausgabe ausschließlich in Markdown. Nutze ## für Hauptabschnitte."""
