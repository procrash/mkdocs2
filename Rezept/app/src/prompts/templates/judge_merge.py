"""Prompt template for the judge model to merge/select best drafts."""
from ..registry import register


@register("judge", "merge")
def render(ctx) -> str:
    return f"""Du bist ein erfahrener Technical Writer und Quality Reviewer.
Du erhältst {ctx.n_drafts} Entwürfe für die Dokumentation von: {ctx.context}
Stakeholder-Typ: {ctx.stakeholder}

## Deine Aufgabe:
1. Bewerte jeden Entwurf nach: Korrektheit, Vollständigkeit, Klarheit, Format
2. Erstelle EINE finale Dokumentation die das Beste aus allen Entwürfen kombiniert
3. Korrigiere faktische Fehler
4. Stelle konsistentes Markdown-Format sicher
5. Behalte LaTeX-Formeln bei ($...$)
6. Behalte ALLE Mermaid-Diagramme bei (```mermaid ... ```). Mermaid-Diagramme sind ein PFLICHT-Bestandteil der Dokumentation.
   Falls ein Entwurf bessere/mehr Mermaid-Diagramme hat, bevorzuge diesen.
   Falls kein Entwurf Mermaid-Diagramme enthält, erstelle mindestens ein passendes Diagramm (classDiagram, flowchart, sequenceDiagram oder erDiagram).
7. Entferne Duplikate und Widersprüche

## Entwürfe:
{ctx.drafts_section}

## Ausgabe:
Die finale, perfekte Markdown-Dokumentation. Kein Meta-Kommentar."""
