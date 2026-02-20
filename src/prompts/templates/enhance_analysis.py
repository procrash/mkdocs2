"""Prompt template for KI-gesteuerte Verbesserung der Dokumentation."""
from ..registry import register


@register("enhance", "analysis")
def render(ctx) -> str:
    return f"""Du bist ein erfahrener MkDocs-Experte und Technical Writer.

Analysiere die folgende Dokumentationsstruktur und mkdocs.yml-Konfiguration.
Schlage konkrete Verbesserungen vor als geänderte Dateien.

## Aktuelle mkdocs.yml:
```yaml
{ctx.code_content}
```

## Vorhandene Dokumentations-Dateien:
{ctx.file_listing}

## Deine Aufgabe:
1. Analysiere die Struktur auf Schwächen (fehlende Seiten, schlechte Navigation, etc.)
2. Prüfe die mkdocs.yml auf Optimierungspotenzial (Theme-Einstellungen, Features, etc.)
3. Schlage neue oder verbesserte Markdown-Seiten vor
4. Schlage mkdocs.yml-Änderungen vor falls sinnvoll

## Ausgabeformat (STRIKT einhalten):

Für jede geänderte/neue Datei:
<<<FILE pfad/zur/datei.md
DESCRIPTION: Kurze Beschreibung der Änderung
>>>
Kompletter neuer Dateiinhalt hier
<<<END>>>

Nur Dateien ausgeben die sich tatsächlich ändern oder neu sind.
Bestehende Inhalte verbessern, nicht löschen.
Alle Texte auf Deutsch."""
