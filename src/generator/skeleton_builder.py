"""Build documentation skeleton with rich placeholder markdown before generation.

Each skeleton page contains detailed content guidelines describing what
should eventually appear there — useful both as LLM prompt context and
as a human-readable roadmap visible in the early MkDocs preview.

The skeleton reflects a comprehensive, general-purpose software documentation
template applicable to any project.
"""
from __future__ import annotations
import logging
from pathlib import Path

from ..config.schema import SkeletonSuggestionEntry

logger = logging.getLogger(__name__)

# Default skeleton structure: (relative_path, title, body_template)
# {project_name} is replaced at creation time.
DEFAULT_SKELETON: list[tuple[str, str, str]] = [
    # ━━ Root ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ("index.md", "Projektdokumentation", """
Willkommen zur Dokumentation für **{project_name}**.

## Dokumentationsstruktur

| Bereich | Inhalt |
|---------|--------|
| [Erste Schritte](getting-started/installation.md) | Installation, Schnellstart, Systemanforderungen |
| [Benutzerhandbuch](user-guide/overview.md) | Konfiguration, Bedienung, erweiterte Funktionen |
| [Bedienungsanleitung](manual/overview.md) | UI-Beschreibung, Workflows, Tastenkürzel, Import/Export |
| [Dateiformate](formats/overview.md) | Ein-/Ausgabeformate, Konfigurationsdateien, DB-Schema |
| [Architektur](architecture/overview.md) | Systemdesign, Komponenten, Datenfluss |
| [API-Referenz](api/overview.md) | Endpunkte, Datenmodelle, Authentifizierung |
| [Developer Guide](generated/developer/index.md) | Auto-generierte Klassen- und Modul-Dokumentation |
| [Entwicklung](development/contributing.md) | Contributing, Code-Richtlinien, Tests, Release |
| [Betrieb](operations/deployment.md) | Deployment, Monitoring, Backup, Sicherheit |
| [Referenz](reference/faq.md) | FAQ, Troubleshooting, Glossar, Changelog, Lizenz |
"""),

    # ━━ Erste Schritte ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ("getting-started/installation.md", "Installation", """
!!! tip "Inhaltsrichtlinie"
    Komplette Schritt-für-Schritt Installationsanleitung.

## Voraussetzungen

Hier sollte stehen:

- **Systemanforderungen**: Betriebssystem, Hardware-Minimum, Festplattenspeicher
- **Software-Abhängigkeiten**: Programmiersprachen, Runtime-Versionen, Paketmanager
- **Netzwerk-Anforderungen**: Ports, Firewall-Regeln, externe Dienste

## Installation

1. **Repository klonen** oder Paket herunterladen
2. **Abhängigkeiten installieren** (z.B. `pip install`, `npm install`)
3. **Konfigurationsdatei erstellen** und anpassen
4. **Installation verifizieren** (Health-Check, Testlauf)

## Docker / Container

Falls zutreffend:

- `docker pull` / `docker-compose up` Anleitung
- Umgebungsvariablen und Volumes
- Port-Mapping
"""),

    ("getting-started/quickstart.md", "Schnellstart", """
!!! tip "Inhaltsrichtlinie"
    Minimaler Guide: vom Start zum ersten Ergebnis in wenigen Minuten.

## Schnellstart in 5 Minuten

1. **Minimalste Installation** (ein Befehl wenn möglich)
2. **Erstes Beispiel ausführen** (Hello World / Demo)
3. **Ergebnis prüfen** — was sollte man sehen?
4. **Nächste Schritte** — Verweis auf tiefergehende Dokumentation

## Beispiel-Konfiguration

```yaml
# Minimale Konfiguration hier einfügen
```

## Typischer Workflow

Beschreibung des üblichen Arbeitsablaufs mit dem Projekt.
"""),

    ("getting-started/requirements.md", "Systemanforderungen", """
!!! tip "Inhaltsrichtlinie"
    Detaillierte Systemvoraussetzungen für alle unterstützten Plattformen.

## Hardware-Anforderungen

| Komponente | Minimum | Empfohlen |
|-----------|---------|-----------|
| CPU | TODO | TODO |
| RAM | TODO | TODO |
| Festplatte | TODO | TODO |

## Software-Anforderungen

TODO: Betriebssysteme, Laufzeitumgebungen, Datenbanken

## Netzwerk-Anforderungen

TODO: Ports, Protokolle, Firewall-Regeln, externe Dienste
"""),

    # ━━ Benutzerhandbuch ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ("user-guide/overview.md", "Benutzerhandbuch — Überblick", """
!!! tip "Inhaltsrichtlinie"
    Einstieg ins Benutzerhandbuch mit Übersicht der Funktionen.

## Überblick

Beschreibung der Hauptfunktionen und des typischen Einsatzzwecks.

## Inhalte

| Kapitel | Inhalt |
|---------|--------|
| [Konfiguration](configuration.md) | Alle Einstellungsmöglichkeiten |
| [Grundlegende Bedienung](basic-usage.md) | Erste Schritte nach der Installation |
| [Erweiterte Funktionen](advanced-features.md) | Fortgeschrittene Features |
| [Beispiele & Rezepte](examples.md) | Praxisnahe Anleitungen |
"""),

    ("user-guide/configuration.md", "Konfiguration", """
!!! tip "Inhaltsrichtlinie"
    Alle Konfigurationsoptionen mit Erklärungen und Beispielen.

## Konfigurationsdatei

TODO: Pfad, Format (YAML/JSON/TOML), Beispiel der vollständigen Konfiguration

## Optionen-Referenz

| Option | Typ | Standard | Beschreibung |
|--------|-----|---------|-------------|
| TODO | TODO | TODO | TODO |

## Umgebungsvariablen

TODO: Welche Umgebungsvariablen werden unterstützt?
"""),

    ("user-guide/basic-usage.md", "Grundlegende Bedienung", """
!!! tip "Inhaltsrichtlinie"
    Schritt-für-Schritt Anleitung für die ersten Aufgaben nach der Installation.

## Erste Schritte

TODO: Was macht der Benutzer als erstes?

## Grundfunktionen

TODO: Die wichtigsten Funktionen mit Beispielen
"""),

    ("user-guide/advanced-features.md", "Erweiterte Funktionen", """
!!! tip "Inhaltsrichtlinie"
    Fortgeschrittene Features für erfahrene Benutzer.

## Fortgeschrittene Konfiguration

TODO: Erweiterte Einstellungen und Anpassungen

## Automatisierung

TODO: Scripting, Batch-Verarbeitung, Integration in CI/CD

## Erweiterbarkeit

TODO: Plugins, Hooks, API-Integration
"""),

    ("user-guide/examples.md", "Beispiele & Rezepte", """
!!! tip "Inhaltsrichtlinie"
    Praxisnahe Beispiele und Copy-Paste-Rezepte für häufige Aufgaben.

## Beispiele

TODO: Konkrete Anwendungsfälle mit vollständigem Code/Konfiguration

## Rezepte

TODO: Schritt-für-Schritt Lösungen für typische Szenarien
"""),

    # ━━ Bedienungsanleitung ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ("manual/overview.md", "Bedienungsanleitung — Überblick", """
!!! tip "Inhaltsrichtlinie"
    Überblick für Endanwender über die Bedienung der Applikation.

Richtet sich an **Endanwender** und beschreibt die praktische Nutzung.

## Kapitel

| Kapitel | Inhalt |
|---------|--------|
| [Benutzeroberfläche](ui-overview.md) | Aufbau, Navigation, Menüs und Dialoge |
| [Workflows & Abläufe](workflows.md) | Schritt-für-Schritt-Anleitungen |
| [Tastenkürzel](shortcuts.md) | Keyboard-Shortcuts |
| [Import & Export](import-export.md) | Daten laden und exportieren |
| [Drucken & Berichte](reports.md) | Berichte erzeugen |
| [Barrierefreiheit](accessibility.md) | Bedienungshilfen |
"""),

    ("manual/ui-overview.md", "Benutzeroberfläche", """
!!! tip "Inhaltsrichtlinie"
    Aufbau des Hauptbildschirms, Navigation, Menüs, Dialoge, Statusleiste.

## Bildschirmaufbau

TODO: Screenshot oder ASCII-Diagramm der Hauptansicht

## Hauptbereiche

TODO: Menüleiste, Sidebar, Hauptbereich, Statusleiste beschreiben

## Dialoge

TODO: Einstellungen, Datei-Öffnen, Bestätigungsdialoge
"""),

    ("manual/workflows.md", "Workflows & Abläufe", """
!!! tip "Inhaltsrichtlinie"
    Schritt-für-Schritt-Anleitungen für typische Aufgaben der Endanwender.

## Typische Arbeitsabläufe

TODO: Neues Projekt erstellen, bearbeiten, speichern, suchen/filtern etc.

Jeder Workflow als nummerierte Schrittfolge mit Erklärungen.
"""),

    ("manual/shortcuts.md", "Tastenkürzel & Shortcuts", """
!!! tip "Inhaltsrichtlinie"
    Vollständige Tastenkürzel-Referenz.

## Allgemeine Tastenkürzel

| Tastenkombination | Aktion |
|-------------------|--------|
| `Strg+N` | Neu |
| `Strg+O` | Öffnen |
| `Strg+S` | Speichern |
| `Strg+Z` | Rückgängig |

TODO: Alle Tastenkürzel der Anwendung auflisten
"""),

    ("manual/import-export.md", "Import & Export", """
!!! tip "Inhaltsrichtlinie"
    Daten importieren und exportieren: unterstützte Formate, Optionen, Beispiele.

## Daten importieren

TODO: Unterstützte Formate, Import-Vorgang, Optionen

## Daten exportieren

TODO: Unterstützte Formate, Export-Vorgang, Optionen
"""),

    ("manual/reports.md", "Drucken & Berichte", """
!!! tip "Inhaltsrichtlinie"
    Berichte erstellen, Druckvorschau, PDF-Export.

## Berichte erstellen

TODO: Verfügbare Berichtstypen, Generierung, Vorlagen

## Drucken

TODO: Druckvorschau, Seitenformat, PDF-Export
"""),

    ("manual/accessibility.md", "Barrierefreiheit", """
!!! tip "Inhaltsrichtlinie"
    Bedienungshilfen: Tastaturnavigation, Screenreader, visuelle Anpassungen.

## Tastaturnavigation

TODO: Tab-Reihenfolge, Fokus-Management

## Screenreader-Unterstützung

TODO: Unterstützte Screenreader, ARIA-Labels

## Visuelle Anpassungen

TODO: Dark Mode, Schriftgröße, Kontrast
"""),

    # ━━ Dateiformate ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ("formats/overview.md", "Dateiformate — Überblick", """
!!! tip "Inhaltsrichtlinie"
    Übersicht aller Dateiformate die von der Anwendung verarbeitet oder erzeugt werden.

## Format-Kategorien

| Kategorie | Beschreibung |
|-----------|-------------|
| [Eingabeformate](input-formats.md) | Formate die importiert werden können |
| [Ausgabeformate](output-formats.md) | Formate die exportiert werden |
| [Konfigurationsdateien](config-files.md) | Interne Konfigurationsformate |
| [Datenbank-Schema](database-schema.md) | Struktur der persistierten Daten |
| [Migrationsformate](migration-formats.md) | Formate für Daten-Migration |

## Allgemeine Konventionen

- **Encoding**: UTF-8 (Standard)
- **Zeilenenden**: Betriebssystem-abhängig
"""),

    ("formats/input-formats.md", "Eingabeformate", """
!!! tip "Inhaltsrichtlinie"
    Alle Dateiformate die importiert/gelesen werden können, mit Schema und Beispielen.

## Unterstützte Formate

| Format | Endung | Beschreibung |
|--------|--------|-------------|
| TODO | TODO | TODO |

Für jedes Format: Schema, Validierung, Beispiel, Encoding-Hinweise.
"""),

    ("formats/output-formats.md", "Ausgabeformate", """
!!! tip "Inhaltsrichtlinie"
    Alle Dateiformate die exportiert/geschrieben werden, mit Schema und Beispielen.

## Unterstützte Formate

| Format | Endung | Beschreibung |
|--------|--------|-------------|
| TODO | TODO | TODO |

Für jedes Format: Struktur, Export-Optionen, Beispiel.
"""),

    ("formats/config-files.md", "Konfigurationsdateien", """
!!! tip "Inhaltsrichtlinie"
    Alle internen Konfigurationsdateien mit vollständiger Feldreferenz.

## Hauptkonfiguration

TODO: Format, Pfad, alle Felder mit Typ/Default/Beschreibung

## Umgebungsvariablen

TODO: Mapping Umgebungsvariable → Konfigurationsoption

## Prioritätsreihenfolge

1. Umgebungsvariablen (höchste Priorität)
2. Konfigurationsdatei
3. Standardwerte
"""),

    ("formats/database-schema.md", "Datenbank-Schema", """
!!! tip "Inhaltsrichtlinie"
    Datenbank-Schema mit ER-Diagramm, Tabellendefinitionen, Indizes.

## ER-Diagramm

```mermaid
erDiagram
    TabelleA ||--o{ TabelleB : "hat viele"
```

TODO: ER-Diagramm an tatsächliches Schema anpassen

## Tabellen

TODO: Jede Tabelle mit Spalten, Typen, Constraints, Indizes
"""),

    ("formats/migration-formats.md", "Migrationsformate", """
!!! tip "Inhaltsrichtlinie"
    Formate für Datenbank-Migrationen und Daten-Migration zwischen Versionen.

## Migrations-Dateien

TODO: Namenskonvention, Struktur, Up/Down-Migrationen

## Daten-Migrationen

TODO: Konvertierung zwischen Format-Versionen
"""),

    # ━━ Architektur ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ("architecture/overview.md", "Systemübersicht", """
!!! tip "Inhaltsrichtlinie"
    High-Level-Architektur des Gesamtsystems.

## Systemarchitektur

```mermaid
graph LR
    subgraph System
        A[Eingabe] --> B[Verarbeitung]
        B --> C[Ausgabe]
    end
```

TODO: Architekturdiagramm anpassen

## Technologie-Stack

TODO: Frameworks, Bibliotheken, Datenbanken mit Begründung

## Architekturmuster

TODO: MVC, Microservices, Event-driven etc.
"""),

    ("architecture/components.md", "Komponenten", """
!!! tip "Inhaltsrichtlinie"
    Detailbeschreibung jeder Hauptkomponente: Verantwortlichkeit, Schnittstellen, Abhängigkeiten.

## Komponentenübersicht

| Komponente | Verantwortlichkeit | Abhängigkeiten |
|-----------|-------------------|----------------|
| TODO | TODO | TODO |

Für jede Komponente:
- Was macht sie?
- Welche Schnittstellen bietet sie?
- Von welchen anderen Komponenten hängt sie ab?
"""),

    ("architecture/data-flow.md", "Datenfluss", """
!!! tip "Inhaltsrichtlinie"
    Wie fließen Daten durch das System? Sequenzdiagramme typischer Abläufe.

## Datenfluss-Übersicht

```mermaid
sequenceDiagram
    participant Client
    participant Server
    participant Database
    Client->>Server: Request
    Server->>Database: Query
    Database-->>Server: Result
    Server-->>Client: Response
```

TODO: Typische Workflows als Sequenzdiagramme

## Datenformate an Schnittstellen

TODO: Welche Formate werden zwischen Komponenten ausgetauscht?
"""),

    ("architecture/decisions.md", "Entscheidungslog (ADR)", """
!!! tip "Inhaltsrichtlinie"
    Architecture Decision Records: Wichtige Designentscheidungen mit Kontext und Begründung.

## Format

Jede Entscheidung im ADR-Format:

- **Status**: Akzeptiert / Abgelehnt / Ersetzt
- **Kontext**: Welches Problem wird gelöst?
- **Entscheidung**: Was wurde beschlossen?
- **Begründung**: Warum diese Lösung?
- **Konsequenzen**: Welche Auswirkungen hat das?

## ADR-001: TODO

- **Status**: Akzeptiert
- **Kontext**: TODO
- **Entscheidung**: TODO
- **Begründung**: TODO
"""),

    # ━━ API-Referenz ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ("api/overview.md", "API-Referenz — Übersicht", """
!!! tip "Inhaltsrichtlinie"
    Einstieg in die API-Dokumentation: Base URL, Versioning, Authentifizierung, Rate Limiting.

## Übersicht

| Seite | Inhalt |
|-------|--------|
| [Endpunkte](endpoints.md) | Alle REST-Endpunkte |
| [Datenmodelle](models.md) | Schemas und Typen |
| [Authentifizierung](authentication.md) | API-Keys, Token, Rollen |
| [Fehlerbehandlung](errors.md) | Fehlercodes und Retry-Strategien |

## Base URL

```
TODO: https://api.example.com/v1
```

## Versioning

TODO: Wie wird die API versioniert?
"""),

    ("api/endpoints.md", "API-Endpunkte", """
!!! tip "Inhaltsrichtlinie"
    Alle Endpunkte mit Methode, Pfad, Parametern, Request/Response-Beispielen.

## Endpunkt-Übersicht

| Methode | Pfad | Beschreibung |
|---------|------|-------------|
| TODO | TODO | TODO |

Für jeden Endpunkt: HTTP-Methode, Pfad, Parameter, Request/Response-Body, Fehler-Antworten.
"""),

    ("api/models.md", "Datenmodelle", """
!!! tip "Inhaltsrichtlinie"
    Alle API-Datenmodelle/Schemas mit Feldern, Typen, Validierung und Beispielen.

## Modelle

TODO: Für jedes Modell: Name, Felder-Tabelle, JSON-Beispiel, Validierungsregeln

## Beziehungen

```mermaid
erDiagram
    ModelA ||--o{ ModelB : "hat viele"
```

TODO: ER-Diagramm der API-Modelle
"""),

    ("api/authentication.md", "Authentifizierung", """
!!! tip "Inhaltsrichtlinie"
    Authentifizierungsmethoden, Token-Management, Rollen und Berechtigungen.

## Authentifizierungsmethode

TODO: API-Key, OAuth2, JWT, Basic Auth?

## Verwendung

```bash
curl -H "Authorization: Bearer <token>" https://api.example.com/v1/resource
```

## Rollen und Berechtigungen

| Rolle | Beschreibung | Zugriffsrechte |
|-------|-------------|---------------|
| TODO | TODO | TODO |
"""),

    ("api/errors.md", "Fehlerbehandlung", """
!!! tip "Inhaltsrichtlinie"
    HTTP-Statuscodes, Fehlercodes, Retry-Strategien, Client-Beispiele.

## Fehlerformat

```json
{
  "status": "error",
  "code": "ERROR_CODE",
  "message": "Beschreibung"
}
```

## HTTP-Statuscodes

| Code | Bedeutung |
|------|----------|
| 200 | Erfolg |
| 400 | Ungültige Anfrage |
| 401 | Nicht authentifiziert |
| 403 | Zugriff verweigert |
| 404 | Nicht gefunden |
| 429 | Rate Limit |
| 500 | Interner Fehler |

## Retry-Strategie

TODO: Welche Fehler mit Retry? Exponentielles Backoff?
"""),

    # ━━ Developer Guide (auto-generiert) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ("generated/developer/index.md", "Developer Guide", """
!!! tip "Inhaltsrichtlinie"
    Auto-generierte technische Dokumentation: Klassen, Module, Diagramme.

## Abschnitte

- [Klassen](classes/index.md) — Klassenhierarchie und Verantwortlichkeiten
- [Module](modules/index.md) — Modulstruktur und Abhängigkeiten
- [Diagramme](diagrams/index.md) — Visualisierungen der Architektur

Dieser Bereich wird automatisch aus dem Quellcode generiert.
"""),

    ("generated/developer/classes/index.md", "Klassen", """
!!! tip "Inhaltsrichtlinie"
    Auto-generierte Dokumentation aller Klassen: Konstruktor, Methoden, Vererbung.
"""),

    ("generated/developer/modules/index.md", "Module", """
!!! tip "Inhaltsrichtlinie"
    Auto-generierte Dokumentation aller Module: Zweck, Schnittstelle, Abhängigkeiten.
"""),

    ("generated/developer/diagrams/index.md", "Diagramme", """
!!! tip "Inhaltsrichtlinie"
    Auto-generierte Mermaid-Diagramme: Klassen, Sequenz, Komponenten, Zustandsdiagramme.
"""),

    # ━━ Entwicklung ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ("development/contributing.md", "Contributing", """
!!! tip "Inhaltsrichtlinie"
    Beitragsrichtlinien: Issues, Pull Requests, Code-Konventionen, Review-Prozess.

## Wie kann ich beitragen?

- Bug-Reports als Issues erstellen
- Feature-Requests vorschlagen
- Code-Beiträge via Pull Request
- Dokumentation verbessern

## Workflow

1. Issue erstellen oder finden
2. Branch erstellen (`feature/...` oder `fix/...`)
3. Änderungen implementieren
4. Tests ausführen
5. Pull Request erstellen

## Commit-Konventionen

```
feat: Neue Funktion
fix: Bug behoben
docs: Dokumentation aktualisiert
refactor: Code-Umstrukturierung
test: Tests hinzugefügt
```
"""),

    ("development/setup.md", "Entwicklungsumgebung", """
!!! tip "Inhaltsrichtlinie"
    Einrichtung der lokalen Entwicklungsumgebung: Klonen, venv, Abhängigkeiten, IDE.

## Repository klonen

```bash
git clone <repo-url>
cd <projekt>
```

## Python-Umgebung

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## IDE-Einrichtung

TODO: Empfohlene IDE-Einstellungen (VS Code, PyCharm)

## Verifizierung

```bash
pytest
```
"""),

    ("development/code-style.md", "Code-Richtlinien", """
!!! tip "Inhaltsrichtlinie"
    Code-Stil: Formatierung, Namenskonventionen, Docstrings, Logging, Error-Handling.

## Formatierung

TODO: Formatter (Black/Prettier), Linter (flake8/ruff/eslint)

## Namenskonventionen

| Element | Konvention | Beispiel |
|---------|-----------|----------|
| Module | snake_case | `my_module.py` |
| Klassen | PascalCase | `MyClass` |
| Funktionen | snake_case | `calculate_total()` |
| Konstanten | UPPER_SNAKE | `MAX_RETRIES` |

## Fehlerbehandlung

- Spezifische Exceptions verwenden
- Keine leeren `except:`-Blöcke
- Eigene Exception-Klassen für Domänenfehler
"""),

    ("development/testing.md", "Tests", """
!!! tip "Inhaltsrichtlinie"
    Test-Strategie: Unit/Integration/E2E, Framework, Fixtures, Coverage, CI.

## Tests ausführen

```bash
pytest
pytest --cov=src --cov-report=html
```

## Test-Struktur

TODO: Verzeichnisstruktur, Namenskonventionen, Fixtures

## Coverage-Ziele

TODO: Mindest-Coverage, CI-Integration
"""),

    ("development/release.md", "Release-Prozess", """
!!! tip "Inhaltsrichtlinie"
    Versionierung (SemVer), Release-Checkliste, Artefakte, Hotfix-Prozess.

## Versionierung

Semantic Versioning: `MAJOR.MINOR.PATCH`

## Release-Checkliste

- [ ] Tests bestehen
- [ ] Changelog aktualisiert
- [ ] Version angepasst
- [ ] Tag erstellt

## Artefakte

TODO: PyPI, Docker-Image, GitHub-Release?
"""),

    # ━━ Betrieb ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ("operations/deployment.md", "Deployment", """
!!! tip "Inhaltsrichtlinie"
    Deployment-Strategien, Umgebungen, Docker, CI/CD, Rollback.

## Umgebungen

| Umgebung | Zweck |
|----------|-------|
| Development | Lokale Entwicklung |
| Staging | Test vor Production |
| Production | Live-System |

## Docker Deployment

```bash
docker build -t projekt:latest .
docker-compose -f docker-compose.prod.yml up -d
```

## Rollback

TODO: Schnelles Rollback auf vorherige Version
"""),

    ("operations/monitoring.md", "Monitoring & Logging", """
!!! tip "Inhaltsrichtlinie"
    Metriken, Logging-Konventionen, Alerting, Dashboards, Incident Response.

## Wichtige Metriken

| Metrik | Schwellwert |
|--------|-------------|
| CPU | < 80% |
| RAM | < 85% |
| Antwortzeit P95 | < 500ms |
| Fehlerrate | < 1% |

## Logging

TODO: Log-Level, Format, Aggregation

## Alerting

TODO: Alert-Regeln, Eskalation, Benachrichtigungskanäle
"""),

    ("operations/backup.md", "Backup & Recovery", """
!!! tip "Inhaltsrichtlinie"
    Backup-Strategie, Zeitpläne, Recovery-Verfahren, RTO/RPO.

## Was wird gesichert?

| Komponente | Häufigkeit | Aufbewahrung |
|-----------|-----------|-------------|
| Datenbank | TODO | TODO |
| Konfiguration | TODO | TODO |
| Uploads/Medien | TODO | TODO |

## Recovery

TODO: Wiederherstellungsschritte, RTO/RPO-Ziele
"""),

    ("operations/security.md", "Sicherheit", """
!!! tip "Inhaltsrichtlinie"
    Sicherheitsrichtlinien: Authentifizierung, Secrets, Netzwerk, Input-Validierung, Audit.

## Grundprinzipien

- Least Privilege
- Defense in Depth
- Secure by Default

## Secrets-Management

- Niemals Secrets in den Quellcode
- Umgebungsvariablen oder Secret-Manager verwenden
- Regelmäßige Rotation

## Sicherheitslücke melden

TODO: Responsible-Disclosure-Prozess
"""),

    # ━━ Referenz ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ("reference/faq.md", "Häufig gestellte Fragen (FAQ)", """
!!! tip "Inhaltsrichtlinie"
    Häufige Fragen zu Installation, Konfiguration, Verwendung, Fehlerbehebung.

## Installation

TODO: Häufige Fragen zur Installation

## Verwendung

TODO: Häufige Fragen zur Nutzung

## Entwicklung

TODO: Häufige Fragen für Entwickler
"""),

    ("reference/troubleshooting.md", "Fehlerbehebung", """
!!! tip "Inhaltsrichtlinie"
    Systematische Fehlersuche: Häufige Probleme, Debug-Modus, Log-Analyse.

## Allgemeine Vorgehensweise

1. Fehlermeldung lesen
2. Log-Dateien prüfen
3. Konfiguration überprüfen
4. Abhängigkeiten prüfen

## Häufige Probleme

TODO: Installation, Konfiguration, Laufzeit, Docker — jeweils mit Ursache und Lösung
"""),

    ("reference/glossary.md", "Glossar", """
!!! tip "Inhaltsrichtlinie"
    Begriffserklärungen: Fachbegriffe, Abkürzungen, projektspezifische Terminologie.

Alphabetisch sortierte Begriffsdefinitionen.

TODO: Projektspezifische Fachbegriffe ergänzen
"""),

    ("reference/changelog.md", "Changelog", """
!!! tip "Inhaltsrichtlinie"
    Versionshistorie nach [Keep a Changelog](https://keepachangelog.com/) Format.

## [Unreleased]

### Hinzugefügt
- TODO

## Kategorien

- **Hinzugefügt** — Neue Features
- **Geändert** — Änderungen an bestehender Funktionalität
- **Behoben** — Bugfixes
- **Entfernt** — Entfernte Features
- **Sicherheit** — Sicherheitsrelevante Änderungen
"""),

    ("reference/license.md", "Lizenz", """
!!! tip "Inhaltsrichtlinie"
    Projektlizenz, Drittanbieter-Lizenzen, Lizenz-Kompatibilität.

## Projektlizenz

TODO: Welche Lizenz? (MIT, Apache 2.0, GPL, etc.)

## Abhängigkeiten

| Bibliothek | Lizenz |
|-----------|--------|
| TODO | TODO |
"""),
]


def create_skeleton(output_dir: Path, project_name: str = "Documentation") -> list[Path]:
    """Create the documentation skeleton with rich placeholder pages.

    Returns list of created file paths.  Existing files are never overwritten.
    """
    docs_dir = output_dir / "docs"
    created: list[Path] = []

    for rel_path, title, body_template in DEFAULT_SKELETON:
        file_path = docs_dir / rel_path
        if file_path.exists():
            continue

        file_path.parent.mkdir(parents=True, exist_ok=True)
        body = body_template.format(project_name=project_name) if "{project_name}" in body_template else body_template
        content = f"# {title}\n{body}"
        file_path.write_text(content.strip() + "\n", encoding="utf-8")
        created.append(file_path)

    logger.info("Skeleton created: %d files in %s", len(created), docs_dir)
    return created


def create_suggestion_files(
    output_dir: Path,
    suggestions: list[SkeletonSuggestionEntry],
) -> list[Path]:
    """Create markdown files for accepted LLM skeleton suggestions.

    Only creates files for suggestions where accepted=True.
    Returns list of created file paths.
    """
    docs_dir = output_dir / "docs"
    created: list[Path] = []

    for suggestion in suggestions:
        if not suggestion.accepted:
            continue
        file_path = docs_dir / suggestion.path
        if file_path.exists():
            continue

        file_path.parent.mkdir(parents=True, exist_ok=True)
        content = f"""# {suggestion.title}

!!! tip "Inhaltsrichtlinie"
    {suggestion.description or 'Dieser Abschnitt wird durch die Dokumentationsgenerierung ergänzt.'}

*Inhalt wird generiert...*
"""
        file_path.write_text(content, encoding="utf-8")
        created.append(file_path)
        logger.info("Created suggestion file: %s", file_path)

    return created


def get_skeleton_tree(output_dir: Path) -> list[tuple[str, int]]:
    """Get the skeleton structure as a tree for display.

    Returns list of (display_line, depth) tuples.
    """
    docs_dir = output_dir / "docs"
    if not docs_dir.exists():
        return []

    tree: list[tuple[str, int]] = []
    _walk_tree(docs_dir, docs_dir, tree, depth=0)
    return tree


def _walk_tree(base: Path, current: Path, tree: list[tuple[str, int]], depth: int) -> None:
    """Recursively walk directory and build tree display."""
    entries = sorted(current.iterdir(), key=lambda p: (not p.is_dir(), p.name))
    for entry in entries:
        if entry.is_dir():
            tree.append((f"{entry.name}/", depth))
            _walk_tree(base, entry, tree, depth + 1)
        elif entry.suffix == ".md":
            tree.append((entry.name, depth))
