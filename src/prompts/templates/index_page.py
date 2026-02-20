"""Prompt template for index/overview page generation."""
from ..registry import register
from . import format_guideline_section


@register("generator", "index")
def render(ctx) -> str:
    guideline_section = format_guideline_section(ctx)

    return f"""Erstelle eine Index-Seite (Inhaltsverzeichnis) für den folgenden Dokumentationsbereich.
{guideline_section}

Bereich: {ctx.section_name}
Enthaltene Seiten:
{ctx.page_listing}

## Anforderungen:
1. Kurze Einleitung (2-3 Sätze)
2. Kategorisierte Auflistung aller Seiten mit Kurzbeschreibung
3. Nutze relative Markdown-Links: [Titel](./pfad/datei.md)
4. Visueller Quick-Start Bereich falls passend"""
