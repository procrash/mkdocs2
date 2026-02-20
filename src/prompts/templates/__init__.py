"""Prompt templates for different stakeholders and document types."""


def format_guideline_section(ctx) -> str:
    """Build the skeleton guideline section for injection into prompts.

    Returns an empty string when no guideline is available, so templates
    can unconditionally include ``{guideline_section}`` without branching.
    """
    if not ctx.skeleton_guidelines:
        return ""
    target = ctx.target_page_path or "unbekannt"
    return f"""
## Inhaltsrichtlinie der Zielseite ({target}):
{ctx.skeleton_guidelines}

WICHTIG: Halte dich an diese Inhaltsrichtlinie. Erzeuge NUR Inhalte die
laut Richtlinie auf diese Seite gehören. Inhalte die laut Abgrenzung
auf andere Seiten gehören, NICHT hier einfügen.
Falls der generierte Inhalt auf KEINE bestehende Seite passt, kannst du
eine neue Seite vorschlagen im Format:
<<<NEW_PAGE path="pfad/zur/seite.md" title="Seitentitel">>>
Markdown-Inhalt...
<<<END>>>
"""
