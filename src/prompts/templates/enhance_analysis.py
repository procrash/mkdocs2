"""Prompt template for KI-gesteuerte Verbesserung der Dokumentation.

Analysiert die nav:-Sektion der mkdocs.yml, identifiziert fehlende
Dokumentationsabschnitte, ergänzt bestehende Dateien oder erzeugt neue,
und aktualisiert die mkdocs.yml-Navigation entsprechend.
"""
from ..registry import register


@register("enhance", "analysis")
def render(ctx) -> str:
    project_name = ctx.section_name or "das Projekt"

    skeleton_section = ""
    if ctx.skeleton_page_map:
        skeleton_section = f"""
## Vorhandene Skeleton-Seiten mit Inhaltsrichtlinien:
{ctx.skeleton_page_map}

Nutze die Inhaltsrichtlinien oben um zu entscheiden, welche Inhalte auf
welche bestehende Seite gehören. Erstelle neue Dateien NUR wenn keine
passende Skeleton-Seite existiert.
"""

    return f"""Du bist ein erfahrener MkDocs-Experte und Technical Writer.

## Projekt: {project_name}
{skeleton_section}
## Aktuelle mkdocs.yml:
```yaml
{ctx.code_content}
```

## Vorhandene Dokumentations-Dateien (Pfad + Inhalt-Vorschau):
{ctx.file_listing}

## Deine Aufgabe:

Analysiere den `nav:`-Abschnitt der mkdocs.yml und die vorhandenen Markdown-Dateien.
Überlege welche Abschnitte eine vollständige, professionelle Dokumentation für
dieses Projekt enthalten sollte.

Typische Abschnitte die oft fehlen (prüfe ob sie vorhanden und sinnvoll sind):
- Startseite / Überblick
- Installation / Erste Schritte (Getting Started)
- Konfiguration / Einrichtung
- Benutzerhandbuch / Anleitungen
- API-Referenz (falls relevant)
- Architektur / Technische Übersicht
- Entwickler-Dokumentation (Contributing, Development Setup)
- FAQ / Häufige Fragen
- Changelog / Versionshistorie
- Fehlerbehebung / Troubleshooting

## Vorgehen für fehlende Inhalte:

Entscheide für jeden fehlenden Abschnitt:

**Option A — In bestehende Datei einfügen:**
Wenn eine vorhandene Markdown-Datei thematisch passt, ergänze den fehlenden
Inhalt dort. Gib dann die **komplette Datei** aus (bestehender + neuer Inhalt).

**Option B — Neue Datei anlegen:**
Wenn kein passendes bestehendes Dokument existiert, erstelle eine neue
Markdown-Datei in der passenden Verzeichnishierarchie (z.B. docs/guides/,
docs/reference/, docs/development/).

In beiden Fällen:
- Füge den Eintrag an der richtigen Stelle in die `nav:`-Hierarchie ein
- Schreibe strukturierten Inhalt in die Markdown-Datei:
  - Überschriften (## / ###) für die geplanten Unterabschnitte
  - Unter jeder Überschrift ein Absatz der beschreibt was dort stehen soll
  - Konkrete Hinweise wie "TODO: Installationsschritte für Docker ergänzen"
  - Falls möglich bereits hilfreiche Inhalte (Übersichten, Aufzählungen, Strukturen)

## Regeln:
- Gib die **komplette mkdocs.yml** aus (mit bestehenden + neuen nav-Einträgen)
- Bestehende nav-Einträge NICHT löschen oder umbenennen
- Wenn du eine bestehende Datei erweiterst: bestehenden Inhalt BEIBEHALTEN und ergänzen
- Neue Dateien in eine sinnvolle Verzeichnisstruktur legen
- Alle Texte auf Deutsch
- Nur Abschnitte ergänzen die wirklich fehlen und für das Projekt sinnvoll sind
- Keine leeren Platzhalter-Dateien — jede Datei soll beschreiben WAS rein soll

## Ausgabeformat (STRIKT einhalten):

Für jede geänderte oder neue Datei genau dieses Format verwenden:

<<<FILE mkdocs.yml
DESCRIPTION: Navigation um fehlende Abschnitte ergänzt
>>>
(hier die komplette mkdocs.yml mit ergänzter nav-Sektion)
<<<END>>>

<<<FILE docs/pfad/zur/datei.md
DESCRIPTION: Kurze Beschreibung der Änderung oder neuen Seite
>>>
(hier der komplette Markdown-Inhalt)
<<<END>>>

Wichtig:
- Jede Datei MUSS mit <<<FILE beginnen und mit <<<END>>> enden
- Kein anderes Format verwenden
- mkdocs.yml IMMER als erste Datei ausgeben
- Dateipfade relativ zum Projektverzeichnis (z.B. docs/guides/installation.md)"""
