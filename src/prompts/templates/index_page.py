"""Prompt template for index/overview page generation."""
from ..registry import register


@register("generator", "index")
def render(ctx) -> str:
    return f"""Erstelle eine Index-Seite (Inhaltsverzeichnis) für den folgenden Dokumentationsbereich.

Bereich: {ctx.section_name}
Enthaltene Seiten:
{ctx.page_listing}

## Anforderungen:
1. Kurze Einleitung (2-3 Sätze)
2. Kategorisierte Auflistung aller Seiten mit Kurzbeschreibung
3. Nutze relative Markdown-Links: [Titel](./pfad/datei.md)
4. Visueller Quick-Start Bereich falls passend"""
