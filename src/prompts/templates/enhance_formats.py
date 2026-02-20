"""Prompt template for file format analysis.

Analyzes source code for file format usage (reading, writing, parsing,
serialization) and generates documentation for the formats/ section
of the mkdocs documentation.
"""
from ..registry import register


@register("enhance", "formats")
def render(ctx) -> str:
    project_name = ctx.section_name or "das Projekt"

    skeleton_section = ""
    if ctx.skeleton_guidelines:
        skeleton_section = f"""
## Inhaltsrichtlinien für Dateiformat-Seiten:
{ctx.skeleton_guidelines}

Nutze die Richtlinien oben um die Inhalte korrekt auf die bestehenden
Skeleton-Seiten zu verteilen.
"""

    return f"""Du bist ein erfahrener Software-Dokumentar und Dateiformat-Spezialist.

## Projekt: {project_name}
{skeleton_section}
## Quellcode des Projekts:
{ctx.code_content}

## Aktuelle mkdocs.yml:
```yaml
{ctx.file_listing}
```

## Deine Aufgabe:

Analysiere den Quellcode systematisch auf alle Dateiformate, die die Anwendung:
- **Liest / Importiert** (Eingabeformate)
- **Schreibt / Exportiert** (Ausgabeformate)
- **Intern verwendet** (Konfigurationsdateien, Caches, Datenbanken)

### Wonach du suchen sollst:

1. **Dateioperationen**: `open()`, `read()`, `write()`, `Path.read_text()`, `Path.write_text()`
2. **Parser/Serializer**: `json.load/dump`, `yaml.safe_load/dump`, `csv.reader/writer`,
   `xml.etree`, `toml.load`, `configparser`, `pickle`, `sqlite3`, etc.
3. **Bibliotheken**: pandas (`read_csv`, `to_excel`), openpyxl, Pillow, PyPDF2, etc.
4. **Web-Formate**: HTTP Requests/Responses, Content-Types, API-Payloads
5. **Datenbanken**: SQLAlchemy, sqlite3, pymongo — Schema und Tabellenstruktur
6. **Template-Engines**: Jinja2, Mako — Template-Formate
7. **Dateiendungen**: Alle Endungen die im Code referenziert werden (.json, .yaml, .csv, .md, etc.)

### Für jedes erkannte Format dokumentiere:

- **Name und Dateiendung** (z.B. "JSON (.json)")
- **Zweck**: Wofür wird es verwendet?
- **Richtung**: Eingabe, Ausgabe, oder beides
- **Schema/Struktur**: Welche Felder/Struktur hat die Datei? (aus dem Code ableiten)
- **Beispiel**: Ein konkretes Beispiel der Dateistruktur
- **Validierung**: Werden die Daten validiert? Welche Regeln?
- **Encoding**: Zeichensatz (falls erkennbar)

## Ausgabe-Anweisungen:

Erzeuge oder aktualisiere die folgenden Dokumentationsseiten im `docs/formats/`-Verzeichnis:
- `docs/formats/overview.md` — Übersicht aller erkannten Formate
- `docs/formats/input-formats.md` — Alle Eingabeformate mit Schema und Beispielen
- `docs/formats/output-formats.md` — Alle Ausgabeformate mit Schema und Beispielen
- `docs/formats/config-files.md` — Konfigurationsdateien mit vollständiger Feldreferenz
- `docs/formats/database-schema.md` — Datenbank-Schema (falls vorhanden)

Falls Formate gefunden werden die in keine bestehende Kategorie passen,
erstelle eine neue passende Datei und füge sie in die mkdocs.yml nav ein.

## Regeln:
- Ersetze TODO-Platzhalter durch die aus dem Code abgeleiteten Informationen
- Bestehende Inhalte die korrekt sind BEIBEHALTEN
- Nur Informationen aufnehmen die aus dem Quellcode ableitbar sind
- Wenn eine Information nicht aus dem Code erkennbar ist: TODO-Marker belassen
- Schema und Beispiele aus dem Code ableiten (Felddefinitionen, Dataclasses, TypedDicts)
- Alle Texte auf Deutsch
- Keine Spekulation — nur was im Code nachweisbar ist

## Ausgabeformat (STRIKT einhalten):

Für jede geänderte oder neue Datei:

<<<FILE docs/formats/overview.md
DESCRIPTION: Übersicht der erkannten Dateiformate aktualisiert
>>>
(kompletter Markdown-Inhalt)
<<<END>>>

<<<FILE docs/formats/input-formats.md
DESCRIPTION: Eingabeformate aus Quellcode-Analyse dokumentiert
>>>
(kompletter Markdown-Inhalt)
<<<END>>>

Wichtig:
- Jede Datei MUSS mit <<<FILE beginnen und mit <<<END>>> enden
- Dateipfade relativ zum Projektverzeichnis
- Falls die mkdocs.yml nav angepasst werden muss (neue Dateien), gib sie als erste Datei aus"""
