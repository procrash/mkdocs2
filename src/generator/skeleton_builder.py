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
| [Erste Schritte](getting-started/installation.md) | Installation, Schnellstart, Systemanforderungen, Upgrade, Migration |
| [Benutzerhandbuch](user-guide/overview.md) | Konfiguration, Bedienung, Berechtigungen, Plugins, CLI |
| [Tutorials](tutorials/overview.md) | Einsteiger-, Fortgeschrittenen- und Experten-Tutorials |
| [Bedienungsanleitung](manual/overview.md) | UI, Workflows, Shortcuts, Import/Export, Suche, Benachrichtigungen |
| [Dateiformate](formats/overview.md) | Ein-/Ausgabeformate, Konfigurationsdateien, DB-Schema, Protokolle |
| [Architektur](architecture/overview.md) | Systemdesign, Komponenten, Datenfluss, Sicherheit, Skalierung |
| [API-Referenz](api/overview.md) | Endpunkte, Datenmodelle, Auth, Webhooks, Rate Limiting, SDKs |
| [Integrationen](integrations/overview.md) | Drittanbieter, SSO, Webhooks, Plugins, CI/CD |
| [Developer Guide](generated/developer/index.md) | Auto-generierte Klassen- und Modul-Dokumentation |
| [Entwicklung](development/contributing.md) | Contributing, Setup, Code-Stil, Tests, CI/CD, Debugging |
| [Betrieb](operations/deployment.md) | Deployment, Monitoring, Backup, Sicherheit, Skalierung, Runbooks |
| [Compliance](compliance/overview.md) | Datenschutz, DSGVO, Audit, SLA |
| [Referenz](reference/faq.md) | FAQ, Troubleshooting, CLI-Referenz, Fehlercodes, Glossar, Changelog |
"""),

    # ━━ Erste Schritte ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ("getting-started/installation.md", "Installation", """
!!! tip "Inhaltsrichtlinie"
    Komplette Schritt-für-Schritt Installationsanleitung für alle Plattformen.

## Voraussetzungen

Hier sollte stehen:

- **Systemanforderungen**: Betriebssystem, Hardware-Minimum, Festplattenspeicher
- **Software-Abhängigkeiten**: Programmiersprachen, Runtime-Versionen, Paketmanager
- **Netzwerk-Anforderungen**: Ports, Firewall-Regeln, externe Dienste

## Installation per Paketmanager

```bash
# pip / npm / apt / brew — je nach Ökosystem
pip install {project_name}
```

## Installation aus Quellcode

```bash
git clone <repo-url>
cd <projekt>
pip install -r requirements.txt
```

## Docker / Container

- `docker pull` / `docker-compose up` Anleitung
- Umgebungsvariablen und Volumes
- Port-Mapping
- Beispiel `docker-compose.yml`

## Plattform-spezifische Hinweise

### Linux

TODO: Besonderheiten für Linux-Distributionen (Debian, Ubuntu, RHEL, Arch)

### macOS

TODO: Homebrew, XCode-CLI-Tools

### Windows

TODO: WSL, native Installation, Chocolatey/Scoop

## Installation verifizieren

```bash
# Versions-Check
<command> --version

# Health-Check
<command> doctor
```
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

## Nächste Schritte

- [Konfiguration anpassen](../user-guide/configuration.md)
- [Grundlegende Bedienung](../user-guide/basic-usage.md)
- [Tutorials durcharbeiten](../tutorials/overview.md)
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
| GPU | TODO (falls relevant) | TODO |

## Software-Anforderungen

| Software | Version | Pflicht | Hinweis |
|----------|---------|---------|---------|
| Python / Node.js / Java | TODO | Ja | TODO |
| Datenbank | TODO | Optional | TODO |
| Docker | TODO | Optional | TODO |

## Betriebssysteme

| OS | Version | Status |
|-----|---------|--------|
| Ubuntu | 20.04+ | Unterstützt |
| macOS | 12+ | Unterstützt |
| Windows | 10/11 | Unterstützt |

## Netzwerk-Anforderungen

| Port | Protokoll | Richtung | Dienst |
|------|----------|----------|--------|
| TODO | TCP | Eingehend | TODO |

## Browser-Anforderungen (falls Web-UI)

| Browser | Mindestversion |
|---------|---------------|
| Chrome | TODO |
| Firefox | TODO |
| Safari | TODO |
| Edge | TODO |
"""),

    ("getting-started/upgrade.md", "Upgrade-Anleitung", """
!!! tip "Inhaltsrichtlinie"
    Anleitung zum Upgrade von einer Version auf die nächste.

## Vor dem Upgrade

- [ ] Backup erstellen (siehe [Backup & Recovery](../operations/backup.md))
- [ ] Changelog lesen (siehe [Changelog](../reference/changelog.md))
- [ ] Breaking Changes prüfen
- [ ] Abhängigkeiten prüfen
- [ ] Wartungsfenster planen

## Upgrade-Schritte

### Upgrade per Paketmanager

```bash
pip install --upgrade {project_name}
```

### Upgrade per Docker

```bash
docker pull <image>:latest
docker-compose up -d
```

### Upgrade aus Quellcode

```bash
git pull origin main
pip install -r requirements.txt
```

## Datenbank-Migrationen

```bash
# TODO: Migrations-Befehl
```

## Nach dem Upgrade

- [ ] Anwendung starten und testen
- [ ] Logs auf Fehler prüfen
- [ ] Funktionalität verifizieren
- [ ] Monitoring prüfen

## Rollback

Falls Probleme auftreten: siehe [Rollback](../operations/deployment.md#rollback)

## Versions-spezifische Hinweise

### Von 1.x auf 2.x

TODO: Breaking Changes, Migrations-Schritte
"""),

    ("getting-started/migration.md", "Migration von anderen Systemen", """
!!! tip "Inhaltsrichtlinie"
    Anleitungen zur Migration von verbreiteten Alternativprodukten.

## Unterstützte Migrationsquellen

| System | Status | Anleitung |
|--------|--------|----------|
| TODO (Alternative A) | Unterstützt | Siehe unten |
| TODO (Alternative B) | Teilweise | Siehe unten |

## Allgemeiner Migrationsprozess

1. **Bestandsaufnahme**: Welche Daten müssen migriert werden?
2. **Export**: Daten aus Altsystem exportieren
3. **Transformation**: Daten in Zielformat konvertieren
4. **Import**: Daten in neues System importieren
5. **Verifikation**: Daten auf Vollständigkeit prüfen
6. **Umstellung**: Benutzer auf neues System umstellen

## Migration von Alternative A

TODO: Schritt-für-Schritt Anleitung

## Daten-Mapping

| Feld im Altsystem | Feld im neuen System | Transformation |
|-------------------|---------------------|----------------|
| TODO | TODO | TODO |

## Bekannte Einschränkungen

TODO: Was kann nicht migriert werden?

## Parallelbetrieb

TODO: Können beide Systeme vorübergehend parallel laufen?
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
| [Berechtigungen & Rollen](permissions.md) | Benutzer, Rollen, Zugriffsrechte |
| [Plugins & Erweiterungen](plugins.md) | Plugin-System, verfügbare Plugins |
| [CLI-Referenz](cli-reference.md) | Kommandozeilen-Befehle |
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

## Konfigurationsprofile

TODO: Verschiedene Profile für verschiedene Umgebungen (dev, staging, prod)

## Konfiguration validieren

```bash
# TODO: Befehl zur Konfigurationsvalidierung
```

## Beispiel-Konfigurationen

### Minimale Konfiguration

```yaml
# TODO
```

### Produktions-Konfiguration

```yaml
# TODO
```
"""),

    ("user-guide/basic-usage.md", "Grundlegende Bedienung", """
!!! tip "Inhaltsrichtlinie"
    Schritt-für-Schritt Anleitung für die ersten Aufgaben nach der Installation.

## Erste Schritte

TODO: Was macht der Benutzer als erstes?

## Grundfunktionen

TODO: Die wichtigsten Funktionen mit Beispielen

## Typische Aufgaben

### Aufgabe 1: TODO

TODO: Schritt-für-Schritt

### Aufgabe 2: TODO

TODO: Schritt-für-Schritt

## Ergebnisse prüfen

TODO: Wie verifiziert man, dass alles richtig funktioniert?
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

## Templates & Vorlagen

TODO: Benutzerdefinierte Vorlagen erstellen und verwenden

## Scheduling & Zeitpläne

TODO: Automatische Ausführung, Cron-Jobs, Timer

## Erweiterte Filterung & Abfragen

TODO: Komplexe Filter, Abfragesprache, reguläre Ausdrücke
"""),

    ("user-guide/permissions.md", "Berechtigungen & Rollen", """
!!! tip "Inhaltsrichtlinie"
    Benutzerverwaltung, Rollen, Zugriffsrechte und Berechtigungskonzept.

## Rollenmodell

| Rolle | Beschreibung | Standardberechtigungen |
|-------|-------------|----------------------|
| Admin | Vollzugriff auf alle Funktionen | Alles |
| Editor | Inhalte erstellen und bearbeiten | Lesen, Schreiben |
| Viewer | Nur lesender Zugriff | Lesen |

TODO: Rollen an Projekt anpassen

## Berechtigungen

| Berechtigung | Beschreibung | Admin | Editor | Viewer |
|-------------|-------------|-------|--------|--------|
| Lesen | Daten anzeigen | ✓ | ✓ | ✓ |
| Schreiben | Daten erstellen/ändern | ✓ | ✓ | ✗ |
| Löschen | Daten entfernen | ✓ | ✗ | ✗ |
| Konfigurieren | Einstellungen ändern | ✓ | ✗ | ✗ |
| Benutzerverwaltung | Benutzer anlegen/ändern | ✓ | ✗ | ✗ |

## Benutzer verwalten

TODO: Benutzer anlegen, Rollen zuweisen, deaktivieren

## Gruppen / Teams

TODO: Falls Gruppenberechtigungen unterstützt werden

## Audit-Log

TODO: Welche Aktionen werden protokolliert?
"""),

    ("user-guide/plugins.md", "Plugins & Erweiterungen", """
!!! tip "Inhaltsrichtlinie"
    Plugin-System: Installation, Konfiguration, verfügbare Plugins, eigene Plugins schreiben.

## Plugin-System

TODO: Wie funktioniert das Plugin-System? Architektur, Hooks, Lifecycle.

## Verfügbare Plugins

| Plugin | Beschreibung | Status |
|--------|-------------|--------|
| TODO | TODO | Stabil |

## Plugin installieren

```bash
# TODO: Installations-Befehl
```

## Plugin konfigurieren

```yaml
plugins:
  - name: plugin-name
    config:
      option: value
```

## Eigene Plugins schreiben

TODO: Plugin-API, Template, Beispiel

## Plugin-Verzeichnis

TODO: Wo findet man weitere Plugins? (Registry, GitHub, etc.)
"""),

    ("user-guide/cli-reference.md", "CLI-Referenz", """
!!! tip "Inhaltsrichtlinie"
    Vollständige Referenz aller Kommandozeilen-Befehle und -Optionen.

## Übersicht

```bash
<command> [global-options] <subcommand> [options] [arguments]
```

## Globale Optionen

| Option | Kurz | Beschreibung |
|--------|------|-------------|
| `--help` | `-h` | Hilfe anzeigen |
| `--version` | `-V` | Version anzeigen |
| `--verbose` | `-v` | Ausführliche Ausgabe |
| `--config` | `-c` | Konfigurationsdatei |
| `--quiet` | `-q` | Keine Ausgabe |

## Befehle

### `<command> init`

Initialisiert ein neues Projekt.

```bash
<command> init [--name NAME] [--template TEMPLATE]
```

| Option | Beschreibung |
|--------|-------------|
| `--name` | Projektname |
| `--template` | Vorlage verwenden |

TODO: Alle Befehle nach diesem Schema dokumentieren

### `<command> run`

TODO

### `<command> build`

TODO

### `<command> test`

TODO

### `<command> deploy`

TODO

## Exit-Codes

| Code | Bedeutung |
|------|----------|
| 0 | Erfolg |
| 1 | Allgemeiner Fehler |
| 2 | Ungültige Argumente |
| TODO | TODO |

## Shell-Completion

```bash
# Bash
eval "$(<command> --completion bash)"

# Zsh
eval "$(<command> --completion zsh)"
```
"""),

    ("user-guide/examples.md", "Beispiele & Rezepte", """
!!! tip "Inhaltsrichtlinie"
    Praxisnahe Beispiele und Copy-Paste-Rezepte für häufige Aufgaben.

## Beispiele

TODO: Konkrete Anwendungsfälle mit vollständigem Code/Konfiguration

## Rezepte

### Rezept 1: TODO

TODO: Schritt-für-Schritt Lösung

### Rezept 2: TODO

TODO: Schritt-für-Schritt Lösung

## Integrations-Beispiele

TODO: Zusammenspiel mit häufig genutzten Tools (Docker, CI/CD, Cloud)

## Skripte & Automatisierung

TODO: Beispiel-Skripte für wiederkehrende Aufgaben
"""),

    # ━━ Tutorials ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ("tutorials/overview.md", "Tutorials — Überblick", """
!!! tip "Inhaltsrichtlinie"
    Übersicht der verfügbaren Tutorials nach Schwierigkeitsgrad.

## Einsteiger

| Tutorial | Dauer | Voraussetzungen |
|----------|-------|-----------------|
| [Erstes Projekt](beginner-first-project.md) | ~15 Min | Installation abgeschlossen |
| [Grundkonfiguration](beginner-configuration.md) | ~10 Min | Erstes Projekt |

## Fortgeschritten

| Tutorial | Dauer | Voraussetzungen |
|----------|-------|-----------------|
| [Automatisierung](advanced-automation.md) | ~30 Min | Grundkonfiguration |
| [Eigene Erweiterungen](advanced-extensions.md) | ~45 Min | Grundkonfiguration |

## Experten

| Tutorial | Dauer | Voraussetzungen |
|----------|-------|-----------------|
| [Performance-Optimierung](expert-performance.md) | ~30 Min | Fortgeschritten |
| [Produktions-Deployment](expert-production.md) | ~60 Min | Fortgeschritten |

## Konventionen

Jedes Tutorial folgt dem gleichen Aufbau:

1. **Ziel**: Was wird am Ende erreicht?
2. **Voraussetzungen**: Was muss vorher erledigt sein?
3. **Schritte**: Nummerierte Anleitung
4. **Ergebnis**: Was sollte am Ende funktionieren?
5. **Nächste Schritte**: Weiterführende Tutorials
"""),

    ("tutorials/beginner-first-project.md", "Tutorial: Erstes Projekt", """
!!! tip "Inhaltsrichtlinie"
    Einsteiger-Tutorial: Vom leeren Zustand zum ersten funktionierenden Projekt.

## Ziel

Am Ende dieses Tutorials haben Sie ein funktionierendes Projekt erstellt.

## Voraussetzungen

- [Installation](../getting-started/installation.md) abgeschlossen
- Terminal / Kommandozeile geöffnet

## Schritte

### Schritt 1: Projekt initialisieren

```bash
# TODO: Befehl
```

### Schritt 2: Konfiguration anpassen

TODO: Minimale Anpassungen

### Schritt 3: Erstes Ergebnis

```bash
# TODO: Befehl
```

### Schritt 4: Ergebnis prüfen

TODO: Was sollte man sehen?

## Zusammenfassung

TODO: Was wurde in diesem Tutorial gelernt?

## Nächste Schritte

- [Grundkonfiguration](beginner-configuration.md)
"""),

    ("tutorials/beginner-configuration.md", "Tutorial: Grundkonfiguration", """
!!! tip "Inhaltsrichtlinie"
    Einsteiger-Tutorial: Die wichtigsten Konfigurationsoptionen verstehen und anpassen.

## Ziel

Die Konfiguration verstehen und an eigene Bedürfnisse anpassen.

## Voraussetzungen

- [Erstes Projekt](beginner-first-project.md) abgeschlossen

## Schritte

### Schritt 1: Konfigurationsdatei öffnen

TODO

### Schritt 2: Grundeinstellungen anpassen

TODO

### Schritt 3: Änderungen testen

TODO

## Zusammenfassung

TODO: Die wichtigsten Konfigurationsoptionen

## Nächste Schritte

- [Automatisierung](advanced-automation.md)
"""),

    ("tutorials/advanced-automation.md", "Tutorial: Automatisierung", """
!!! tip "Inhaltsrichtlinie"
    Fortgeschrittenen-Tutorial: Aufgaben automatisieren, Skripte erstellen, CI/CD integrieren.

## Ziel

Wiederkehrende Aufgaben automatisieren und in CI/CD-Pipelines integrieren.

## Voraussetzungen

- Grundkonfiguration verstanden

## Schritte

### Schritt 1: Batch-Verarbeitung

TODO

### Schritt 2: Skript erstellen

TODO

### Schritt 3: CI/CD-Integration

TODO

## Zusammenfassung

TODO

## Nächste Schritte

- [Eigene Erweiterungen](advanced-extensions.md)
"""),

    ("tutorials/advanced-extensions.md", "Tutorial: Eigene Erweiterungen", """
!!! tip "Inhaltsrichtlinie"
    Fortgeschrittenen-Tutorial: Das Plugin-/Erweiterungssystem nutzen.

## Ziel

Eine eigene Erweiterung/Plugin schreiben und einbinden.

## Voraussetzungen

- Grundkonfiguration verstanden
- Grundkenntnisse in der Programmiersprache des Projekts

## Schritte

TODO: Plugin-Erstellung Schritt für Schritt

## Zusammenfassung

TODO
"""),

    ("tutorials/expert-performance.md", "Tutorial: Performance-Optimierung", """
!!! tip "Inhaltsrichtlinie"
    Experten-Tutorial: Performance messen, Engpässe finden, optimieren.

## Ziel

Performance messen und gezielt optimieren.

## Voraussetzungen

- Fortgeschrittene Kenntnisse

## Schritte

### Schritt 1: Performance messen

TODO: Benchmarking, Profiling

### Schritt 2: Engpässe identifizieren

TODO: Häufige Bottlenecks

### Schritt 3: Optimierungen anwenden

TODO: Caching, Indexierung, Parallelisierung

## Zusammenfassung

TODO
"""),

    ("tutorials/expert-production.md", "Tutorial: Produktions-Deployment", """
!!! tip "Inhaltsrichtlinie"
    Experten-Tutorial: Vom Entwicklungsmodus zum produktionsreifen System.

## Ziel

Ein robustes Produktions-Setup aufbauen.

## Voraussetzungen

- Fortgeschrittene Kenntnisse
- Zugang zu Produktionsinfrastruktur

## Schritte

### Schritt 1: Härtung

TODO: Sicherheit, Debug-Modus aus, HTTPS

### Schritt 2: Monitoring einrichten

TODO: Health Checks, Alerting

### Schritt 3: Backup konfigurieren

TODO: Automatische Backups

### Schritt 4: Deployment automatisieren

TODO: CI/CD-Pipeline

## Zusammenfassung

TODO
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
| [Suche & Filter](search.md) | Daten finden, filtern, sortieren |
| [Benachrichtigungen](notifications.md) | Alerts, E-Mails, System-Benachrichtigungen |
| [Tastenkürzel](shortcuts.md) | Keyboard-Shortcuts |
| [Import & Export](import-export.md) | Daten laden und exportieren |
| [Drucken & Berichte](reports.md) | Berichte erzeugen |
| [Einstellungen](settings.md) | Persönliche Einstellungen anpassen |
| [Mehrbenutzerbetrieb](multi-user.md) | Zusammenarbeit, Rechte, Konflikte |
| [Barrierefreiheit](accessibility.md) | Bedienungshilfen |
"""),

    ("manual/ui-overview.md", "Benutzeroberfläche", """
!!! tip "Inhaltsrichtlinie"
    Aufbau des Hauptbildschirms, Navigation, Menüs, Dialoge, Statusleiste.

## Bildschirmaufbau

```
┌──────────────────────────────────────────────┐
│  Menüleiste / Toolbar                        │
├────────┬─────────────────────────────────────┤
│        │                                     │
│  Side- │     Hauptbereich / Arbeitsbereich   │
│  bar   │                                     │
│        │                                     │
├────────┴─────────────────────────────────────┤
│  Statusleiste                                │
└──────────────────────────────────────────────┘
```

TODO: Screenshot oder angepasstes Diagramm

## Hauptbereiche

### Menüleiste

| Menü | Inhalt |
|------|--------|
| **Datei** | Neu, Öffnen, Speichern, Exportieren, Beenden |
| **Bearbeiten** | Rückgängig, Wiederherstellen, Suchen, Ersetzen |
| **Ansicht** | Zoom, Sidebar ein/ausblenden, Vollbild |
| **Extras** | Einstellungen, Plugins, Erweiterungen |
| **Hilfe** | Dokumentation, Über, Updates |

### Sidebar / Navigation

TODO: Projektbaum, Filter, Favoriten, Ein/Ausklappbar

### Hauptbereich

TODO: Tabs, Kontextmenü, Drag & Drop

### Statusleiste

TODO: Status, Fortschritt, Cursor-Position, Verbindung

## Dialoge

TODO: Einstellungen, Datei-Öffnen, Bestätigungsdialoge

## Benachrichtigungen

- **Info** (blau): Allgemeine Hinweise
- **Erfolg** (grün): Aktion erfolgreich
- **Warnung** (gelb): Mögliches Problem
- **Fehler** (rot): Aktion fehlgeschlagen

## Theme / Dark Mode

TODO: Wie zwischen Themes wechseln?
"""),

    ("manual/workflows.md", "Workflows & Abläufe", """
!!! tip "Inhaltsrichtlinie"
    Schritt-für-Schritt-Anleitungen für typische Aufgaben der Endanwender.

## Neues Projekt erstellen

1. **Datei** → **Neues Projekt** (oder `Strg+N`)
2. Name und Speicherort angeben
3. Template auswählen
4. **Erstellen** klicken

## Bestehendes Projekt öffnen

TODO

## Daten bearbeiten

TODO: Einfache und Mehrfachbearbeitung

## Rückgängig / Wiederherstellen

- `Strg+Z`: Rückgängig
- `Strg+Y`: Wiederherstellen
- **Bearbeiten** → **Verlauf**: Kompletten Aktionsverlauf anzeigen

## Speichern und Autosave

- `Strg+S`: Manuell speichern
- Autosave: TODO (Intervall, Konfiguration)

## Zusammenarbeit

TODO: Gleichzeitige Bearbeitung, Kommentare, Freigabe

## Fehlersituationen

### Ungespeicherte Änderungen

TODO: Dialog bei Schließen

### Absturz-Recovery

TODO: Automatische Backups, Wiederherstellung
"""),

    ("manual/search.md", "Suche & Filter", """
!!! tip "Inhaltsrichtlinie"
    Suchfunktionen, Filter, Sortierung, gespeicherte Suchen.

## Einfache Suche

- `Strg+F`: Suchfeld öffnen
- Suchbegriff eingeben → Ergebnisse werden markiert
- `Enter`: Nächster Treffer
- `Shift+Enter`: Vorheriger Treffer

## Erweiterte Suche

TODO: Reguläre Ausdrücke, Feld-spezifische Suche, Volltextsuche

## Filter

TODO: Daten nach Kriterien filtern

| Filter | Beschreibung | Beispiel |
|--------|-------------|---------|
| TODO | TODO | TODO |

## Sortierung

TODO: Nach welchen Feldern kann sortiert werden?

## Gespeicherte Suchen / Filter

TODO: Häufig genutzte Filter speichern und wiederverwenden

## Suche über alle Dateien / Projekte

TODO: Globale Suche, `Strg+Shift+F`
"""),

    ("manual/notifications.md", "Benachrichtigungen", """
!!! tip "Inhaltsrichtlinie"
    System-Benachrichtigungen, E-Mail-Alerts, Push-Notifications, Konfiguration.

## Benachrichtigungstypen

| Typ | Kanal | Beschreibung |
|-----|-------|-------------|
| System | In-App | Benachrichtigungen in der Anwendung |
| E-Mail | SMTP | E-Mail-Benachrichtigungen bei wichtigen Events |
| Push | Browser/OS | Desktop-Benachrichtigungen |
| Webhook | HTTP | Programmatische Benachrichtigungen |

TODO: An Projekt anpassen

## Benachrichtigungen konfigurieren

TODO: Wo und wie konfiguriert man Benachrichtigungen?

## Events

| Event | Beschreibung | Standard |
|-------|-------------|---------|
| TODO | TODO | Aktiv/Inaktiv |

## Benachrichtigungs-Verlauf

TODO: Wo findet man vergangene Benachrichtigungen?

## Stille Stunden / Do Not Disturb

TODO: Benachrichtigungen zeitweise unterdrücken
"""),

    ("manual/shortcuts.md", "Tastenkürzel & Shortcuts", """
!!! tip "Inhaltsrichtlinie"
    Vollständige Tastenkürzel-Referenz.

## Allgemein

| Tastenkombination | Aktion |
|-------------------|--------|
| `Strg+N` | Neues Projekt / Dokument |
| `Strg+O` | Öffnen |
| `Strg+S` | Speichern |
| `Strg+Shift+S` | Speichern unter |
| `Strg+W` | Tab schließen |
| `Strg+Q` | Beenden |

## Navigation

| Tastenkombination | Aktion |
|-------------------|--------|
| `Strg+Tab` | Nächster Tab |
| `Strg+Shift+Tab` | Vorheriger Tab |
| `Strg+G` | Gehe zu Zeile/Position |
| `Strg+P` | Schnellzugriff / Dateien |
| `F11` | Vollbild |
| `Strg+B` | Sidebar |

## Bearbeitung

| Tastenkombination | Aktion |
|-------------------|--------|
| `Strg+Z` | Rückgängig |
| `Strg+Y` | Wiederherstellen |
| `Strg+D` | Duplizieren |
| `Strg+Shift+K` | Zeile löschen |

## Suche

| Tastenkombination | Aktion |
|-------------------|--------|
| `Strg+F` | Suchen |
| `Strg+H` | Suchen & Ersetzen |
| `Strg+Shift+F` | Globale Suche |

## Anpassen

TODO: Können Tastenkürzel angepasst werden?
"""),

    ("manual/import-export.md", "Import & Export", """
!!! tip "Inhaltsrichtlinie"
    Daten importieren und exportieren: unterstützte Formate, Optionen, Mapping, Beispiele.

## Daten importieren

### Unterstützte Formate

TODO: Formate-Tabelle, Verweis auf [Eingabeformate](../formats/input-formats.md)

### Import-Vorgang

1. **Datei** → **Importieren**
2. Quelldatei wählen
3. Encoding und Optionen konfigurieren
4. Feld-Mapping prüfen
5. Vorschau kontrollieren
6. **Importieren**

### Häufige Probleme

TODO: Encoding, fehlende Felder, Duplikate

## Daten exportieren

### Unterstützte Formate

TODO: Formate-Tabelle, Verweis auf [Ausgabeformate](../formats/output-formats.md)

### Export-Vorgang

1. Daten auswählen (oder alles)
2. **Datei** → **Exportieren**
3. Zielformat und Optionen wählen
4. **Exportieren**

## Batch-Import / Batch-Export

TODO: Mehrere Dateien auf einmal verarbeiten
"""),

    ("manual/reports.md", "Drucken & Berichte", """
!!! tip "Inhaltsrichtlinie"
    Berichte erstellen, Druckvorschau, PDF-Export, Berichts-Vorlagen.

## Berichte erstellen

TODO: Berichtstypen, Generierung, Zeitraum/Datenbereich

## Berichts-Vorlagen

TODO: Standard-Vorlagen, benutzerdefinierte Vorlagen, Logo/Branding

## Druckvorschau

TODO: `Strg+Shift+P`, Seitenformat, Kopf-/Fußzeile

## PDF-Export

TODO: Optionen (Komprimierung, Metadaten, Passwortschutz)

## Geplante Berichte

TODO: Automatische Erstellung nach Zeitplan, E-Mail-Versand
"""),

    ("manual/settings.md", "Einstellungen", """
!!! tip "Inhaltsrichtlinie"
    Alle benutzerspezifischen Einstellungsmöglichkeiten.

## Einstellungen öffnen

**Extras** → **Einstellungen** (oder `Strg+,`)

## Allgemein

| Einstellung | Beschreibung | Standard |
|------------|-------------|---------|
| Sprache | Anzeigesprache | Systemsprache |
| Theme | Hell / Dunkel / System | System |
| Autosave | Automatisch speichern | An (30s) |
| Startseite | Was beim Start anzeigen | Letztes Projekt |

## Darstellung

TODO: Schriftgröße, Schriftart, Farbschema, Kompaktmodus

## Editor

TODO: Zeilennummern, Einrückung, Syntax-Highlighting, Wortumbruch

## Benachrichtigungen

TODO: Welche Benachrichtigungen an/aus

## Datenschutz

TODO: Telemetrie, Analyse, Datensammlung

## Einstellungen zurücksetzen

TODO: Auf Standardwerte zurücksetzen
"""),

    ("manual/multi-user.md", "Mehrbenutzerbetrieb", """
!!! tip "Inhaltsrichtlinie"
    Zusammenarbeit mehrerer Benutzer: gleichzeitiger Zugriff, Konflikte, Berechtigungen.

## Übersicht

TODO: Unterstützt die Anwendung Mehrbenutzerbetrieb?

## Gleichzeitige Bearbeitung

TODO: Wird gleichzeitige Bearbeitung unterstützt? Real-time Collaboration?

## Konfliktvermeidung

TODO: Locking, Merge-Strategien, Benachrichtigungen bei Konflikten

## Benutzer-Sichtbarkeit

TODO: Wer ist gerade online? Wer bearbeitet was?

## Kommentare & Diskussionen

TODO: Inline-Kommentare, Diskussionen, @-Mentions

## Freigabe & Teilen

TODO: Projekte/Dokumente mit anderen teilen, Links generieren

## Audit-Trail

TODO: Wer hat wann was geändert?
"""),

    ("manual/accessibility.md", "Barrierefreiheit", """
!!! tip "Inhaltsrichtlinie"
    Bedienungshilfen: Tastaturnavigation, Screenreader, visuelle Anpassungen, Sprachunterstützung.

## Standards

TODO: WCAG 2.1, BITV 2.0 — welcher Level wird eingehalten?

## Tastaturnavigation

- **Tab** / **Shift+Tab**: Zwischen Elementen navigieren
- **Enter** / **Leertaste**: Element aktivieren
- **Escape**: Dialog schließen
- **Pfeiltasten**: In Listen/Menüs navigieren

## Screenreader

TODO: Unterstützte Screenreader (NVDA, JAWS, VoiceOver, Orca), ARIA-Labels

## Visuelle Anpassungen

- Hochkontrast-Modus
- Dark Mode / Light Mode
- Schriftgröße: `Strg++` / `Strg+-`
- Zoom zurücksetzen: `Strg+0`

## Sprachunterstützung

| Sprache | Status |
|---------|--------|
| Deutsch | TODO |
| Englisch | TODO |

## Feedback

TODO: Accessibility-Probleme melden
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
| [Protokolle & Logs](log-formats.md) | Log-Formate und Audit-Dateien |
| [API-Formate](api-formats.md) | Request/Response-Formate der API |

## Allgemeine Konventionen

- **Encoding**: UTF-8 (Standard)
- **Zeilenenden**: Betriebssystem-abhängig
- **Dateinamen**: keine Sonderzeichen, Kleinschreibung empfohlen

## Schema-Validierung

TODO: Werden Dateien gegen Schemas validiert? (JSON Schema, XSD)

## Versionierung von Formaten

TODO: Wie wird Abwärtskompatibilität sichergestellt?
"""),

    ("formats/input-formats.md", "Eingabeformate", """
!!! tip "Inhaltsrichtlinie"
    Alle Dateiformate die importiert/gelesen werden können, mit Schema und Beispielen.

## Unterstützte Formate

| Format | Endung | MIME-Type | Beschreibung |
|--------|--------|-----------|-------------|
| JSON | `.json` | `application/json` | JavaScript Object Notation |
| CSV | `.csv` | `text/csv` | Comma-Separated Values |
| XML | `.xml` | `application/xml` | Extensible Markup Language |
| YAML | `.yml`, `.yaml` | `application/x-yaml` | YAML Ain't Markup Language |
| Markdown | `.md` | `text/markdown` | Markdown-Textdateien |

TODO: Projektspezifische Formate ergänzen

Für jedes Format: Schema, Validierung, Beispiel, Encoding-Hinweise, Größenlimits.
"""),

    ("formats/output-formats.md", "Ausgabeformate", """
!!! tip "Inhaltsrichtlinie"
    Alle Dateiformate die exportiert/geschrieben werden, mit Schema und Beispielen.

## Unterstützte Formate

| Format | Endung | MIME-Type | Beschreibung |
|--------|--------|-----------|-------------|
| JSON | `.json` | `application/json` | Maschinenlesbarer Datenexport |
| CSV | `.csv` | `text/csv` | Tabellarischer Export |
| PDF | `.pdf` | `application/pdf` | Druckfertiger Bericht |
| HTML | `.html` | `text/html` | Web-taugliche Ausgabe |

TODO: Projektspezifische Formate ergänzen

## Format-Vergleich

| Eigenschaft | JSON | CSV | PDF | HTML |
|------------|------|-----|-----|------|
| Maschinenlesbar | Ja | Ja | Nein | Bedingt |
| Bearbeitbar | Ja | Ja | Nein | Ja |
| Druckfertig | Nein | Nein | Ja | Ja |
"""),

    ("formats/config-files.md", "Konfigurationsdateien", """
!!! tip "Inhaltsrichtlinie"
    Alle internen Konfigurationsdateien mit vollständiger Feldreferenz.

## Übersicht

| Datei | Format | Zweck | Ort |
|-------|--------|-------|-----|
| TODO | YAML | Hauptkonfiguration | Projektverzeichnis |
| `.env` | Key=Value | Secrets / Umgebung | Projektverzeichnis |
| TODO | JSON | Benutzereinstellungen | Benutzerverzeichnis |

## Hauptkonfiguration

TODO: Vollständige Referenz aller Felder

## Umgebungsvariablen

TODO: Mapping Umgebungsvariable → Konfigurationsoption

## Prioritätsreihenfolge

1. Kommandozeilen-Argumente (höchste)
2. Umgebungsvariablen
3. .env-Datei
4. Konfigurationsdatei
5. Standardwerte (niedrigste)

## Validierung

TODO: Werden Konfigurationsdateien beim Start validiert?
"""),

    ("formats/database-schema.md", "Datenbank-Schema", """
!!! tip "Inhaltsrichtlinie"
    Datenbank-Schema mit ER-Diagramm, Tabellendefinitionen, Indizes, Migrationen.

## ER-Diagramm

```mermaid
erDiagram
    User ||--o{ Project : "besitzt"
    Project ||--o{ Document : "enthält"
    Document ||--o{ Version : "hat Versionen"
```

TODO: ER-Diagramm an tatsächliches Schema anpassen

## Tabellen

TODO: Jede Tabelle mit Spalten, Typen, Constraints, Indizes, Fremdschlüssel

## Seed-Daten

TODO: Initiale Testdaten / Referenzdaten

## Migrations-Werkzeug

TODO: Alembic, Flyway, Django Migrations — Befehle für Up/Down
"""),

    ("formats/migration-formats.md", "Migrationsformate", """
!!! tip "Inhaltsrichtlinie"
    Formate für Datenbank-Migrationen und Daten-Migration zwischen Versionen.

## Migrations-Dateien

TODO: Namenskonvention, Struktur, Up/Down-Migrationen

## Daten-Migrationen

TODO: Konvertierung zwischen Format-Versionen

## Best Practices

1. Immer Up + Down bereitstellen
2. Keine Datenverluste
3. Idempotenz
4. Kleine Schritte
5. In Staging testen
"""),

    ("formats/log-formats.md", "Protokolle & Log-Formate", """
!!! tip "Inhaltsrichtlinie"
    Formate von Log-Dateien, Audit-Logs, Access-Logs.

## Application-Log

### Format

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "ERROR",
  "logger": "src.module",
  "message": "Beschreibung",
  "trace_id": "abc-123",
  "extra": {}
}
```

TODO: An tatsächliches Log-Format anpassen

### Log-Level

| Level | Wann verwenden |
|-------|---------------|
| DEBUG | Detaillierte Diagnose |
| INFO | Normaler Betrieb |
| WARNING | Unerwarteter Zustand |
| ERROR | Fehler aufgetreten |
| CRITICAL | System instabil |

## Access-Log

TODO: Format der HTTP-Access-Logs (falls Web-Anwendung)

## Audit-Log

TODO: Format der Audit-Logs (wer hat wann was getan)

| Feld | Typ | Beschreibung |
|------|-----|-------------|
| timestamp | datetime | Zeitpunkt |
| user_id | string | Benutzer |
| action | string | Ausgeführte Aktion |
| resource | string | Betroffene Ressource |
| result | enum | success/failure |

## Log-Rotation

TODO: Wie werden Logs rotiert? Aufbewahrungsdauer?
"""),

    ("formats/api-formats.md", "API-Formate", """
!!! tip "Inhaltsrichtlinie"
    Request/Response-Formate, Content-Types, Pagination, Filtering in der API.

## Content-Types

| Content-Type | Verwendung |
|-------------|-----------|
| `application/json` | Standard für Request/Response |
| `multipart/form-data` | Datei-Upload |
| `text/csv` | CSV-Export |

## Standard-Response-Format

```json
{
  "status": "success",
  "data": {},
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 150
  }
}
```

## Pagination

TODO: Offset/Limit, Cursor-basiert, Link-Header

## Filtering

TODO: Query-Parameter, Filter-Syntax

## Sortierung

TODO: `?sort=name&order=asc`

## Felder einschränken

TODO: `?fields=id,name,status`
"""),

    # ━━ Architektur ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ("architecture/overview.md", "Systemübersicht", """
!!! tip "Inhaltsrichtlinie"
    High-Level-Architektur des Gesamtsystems.

## Systemarchitektur

```mermaid
graph LR
    subgraph Frontend
        A[Web-UI / CLI / TUI]
    end
    subgraph Backend
        B[API-Layer]
        C[Business Logic]
        D[Data Access]
    end
    subgraph Infrastruktur
        E[Datenbank]
        F[Cache]
        G[Message Queue]
    end
    A --> B --> C --> D
    D --> E
    D --> F
    C --> G
```

TODO: Architekturdiagramm anpassen

## Schichtenmodell

| Schicht | Verantwortlichkeit |
|---------|-------------------|
| Präsentation | UI, API-Endpunkte, Input-Validierung |
| Geschäftslogik | Regeln, Workflows, Orchestrierung |
| Datenzugriff | Persistenz, Caching, externe Dienste |
| Infrastruktur | Datenbank, Queue, Dateisystem |

## Technologie-Stack

TODO: Verweis auf [Technologie-Stack](tech-stack.md)

## Architekturmuster

TODO: MVC, Clean Architecture, Hexagonal, Event-driven, CQRS etc.
"""),

    ("architecture/components.md", "Komponenten", """
!!! tip "Inhaltsrichtlinie"
    Detailbeschreibung jeder Hauptkomponente: Verantwortlichkeit, Schnittstellen, Abhängigkeiten.

## Komponentendiagramm

```mermaid
graph TD
    A[Komponente A] --> B[Komponente B]
    A --> C[Komponente C]
    B --> D[Komponente D]
    C --> D
```

TODO: An tatsächliche Komponenten anpassen

## Komponentenübersicht

| Komponente | Verantwortlichkeit | Schnittstellen | Abhängigkeiten |
|-----------|-------------------|----------------|----------------|
| TODO | TODO | TODO | TODO |

## Detailbeschreibung

### Komponente A

TODO: Verantwortlichkeit, API, Konfiguration, Fehlerbehandlung

### Komponente B

TODO: ...
"""),

    ("architecture/data-flow.md", "Datenfluss", """
!!! tip "Inhaltsrichtlinie"
    Wie fließen Daten durch das System? Sequenzdiagramme typischer Abläufe.

## Datenfluss-Übersicht

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Service
    participant Database
    participant Cache
    Client->>API: Request
    API->>Cache: Check Cache
    alt Cache Hit
        Cache-->>API: Cached Data
    else Cache Miss
        API->>Service: Process
        Service->>Database: Query
        Database-->>Service: Result
        Service-->>API: Processed Data
        API->>Cache: Store
    end
    API-->>Client: Response
```

TODO: An tatsächliche Abläufe anpassen

## Datenformate an Schnittstellen

TODO: Welche Formate werden zwischen Komponenten ausgetauscht?

## Event-/Message-Fluss

TODO: Falls Event-driven: Welche Events, Queues, Topics?
"""),

    ("architecture/decisions.md", "Entscheidungslog (ADR)", """
!!! tip "Inhaltsrichtlinie"
    Architecture Decision Records: Wichtige Designentscheidungen mit Kontext und Begründung.

## Format

Jede Entscheidung im ADR-Format:

- **Status**: Akzeptiert / Abgelehnt / Ersetzt
- **Kontext**: Welches Problem wird gelöst?
- **Optionen**: Welche Alternativen wurden erwogen?
- **Entscheidung**: Was wurde beschlossen?
- **Begründung**: Warum diese Lösung?
- **Konsequenzen**: Welche Auswirkungen hat das?

## ADR-001: TODO

- **Status**: Akzeptiert
- **Datum**: TODO
- **Kontext**: TODO
- **Optionen**: A) ..., B) ..., C) ...
- **Entscheidung**: TODO
- **Begründung**: TODO
- **Konsequenzen**: TODO
"""),

    ("architecture/tech-stack.md", "Technologie-Stack", """
!!! tip "Inhaltsrichtlinie"
    Alle verwendeten Technologien mit Version, Zweck und Begründung.

## Übersicht

### Kernsprache & Runtime

| Technologie | Version | Zweck | Begründung |
|-----------|---------|-------|-----------|
| TODO | TODO | Hauptsprache | TODO |

### Frameworks

| Framework | Version | Zweck | Begründung |
|----------|---------|-------|-----------|
| TODO | TODO | TODO | TODO |

### Datenbanken & Storage

| Technologie | Version | Zweck |
|-----------|---------|-------|
| TODO | TODO | Primäre Datenbank |
| TODO | TODO | Cache |

### Infrastruktur

| Technologie | Zweck |
|-----------|-------|
| Docker | Containerisierung |
| TODO | CI/CD |
| TODO | Monitoring |

### Entwicklungswerkzeuge

| Tool | Zweck |
|------|-------|
| TODO | Linter |
| TODO | Formatter |
| TODO | Test-Framework |

## Abhängigkeitsmanagement

TODO: Wie werden Abhängigkeiten verwaltet? Lock-Files? Update-Strategie?

## Technologie-Radar

TODO: Welche Technologien werden evaluiert, eingeführt, beibehalten oder abgelöst?
"""),

    ("architecture/security-architecture.md", "Sicherheitsarchitektur", """
!!! tip "Inhaltsrichtlinie"
    Sicherheitsaspekte der Architektur: Authentifizierung, Autorisierung, Verschlüsselung, Trust Boundaries.

## Trust Boundaries

```mermaid
graph LR
    subgraph "Öffentlich"
        A[Browser/Client]
    end
    subgraph "DMZ"
        B[Load Balancer]
        C[WAF]
    end
    subgraph "Intern"
        D[Application Server]
        E[Database]
    end
    A -->|HTTPS| B --> C --> D --> E
```

TODO: Trust Boundaries an Projekt anpassen

## Authentifizierung

TODO: Wo und wie wird authentifiziert? Verweis auf [API-Auth](../api/authentication.md)

## Autorisierung

TODO: RBAC, ABAC, ACL? Verweis auf [Berechtigungen](../user-guide/permissions.md)

## Verschlüsselung

| Kontext | Methode | Details |
|---------|---------|---------|
| Transport (TLS) | TODO | TODO |
| Ruhezustand (at rest) | TODO | TODO |
| Secrets | TODO | TODO |

## Eingabevalidierung

TODO: Wo wird validiert? Welche Methoden (Sanitization, Parameterized Queries)?

## Logging & Audit

TODO: Sicherheitsrelevante Events, Verweis auf [Audit](../compliance/audit.md)
"""),

    ("architecture/scalability.md", "Skalierung & Performance", """
!!! tip "Inhaltsrichtlinie"
    Skalierungsstrategien, Engpässe, Caching, horizontale/vertikale Skalierung.

## Aktuelle Kapazitäten

| Metrik | Wert | Gemessen |
|--------|------|---------|
| Max. Benutzer gleichzeitig | TODO | TODO |
| Max. Requests/Sekunde | TODO | TODO |
| Max. Datenbankgröße | TODO | TODO |

## Skalierungsstrategien

### Horizontale Skalierung

TODO: Load Balancing, Stateless Design, Session Handling

### Vertikale Skalierung

TODO: CPU/RAM erhöhen, Limits

## Caching-Strategie

| Cache-Ebene | Technologie | TTL | Invalidierung |
|------------|-------------|-----|---------------|
| Application | TODO | TODO | TODO |
| Database | TODO | TODO | TODO |
| CDN / HTTP | TODO | TODO | TODO |

## Bekannte Engpässe

TODO: Wo sind die Grenzen? Was ist der Flaschenhals?

## Performance-Ziele

| Metrik | Ziel |
|--------|------|
| Antwortzeit (P50) | < 100ms |
| Antwortzeit (P95) | < 500ms |
| Antwortzeit (P99) | < 2s |
| Verfügbarkeit | 99.9% |
"""),

    # ━━ API-Referenz ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ("api/overview.md", "API-Referenz — Übersicht", """
!!! tip "Inhaltsrichtlinie"
    Einstieg in die API-Dokumentation: Base URL, Versioning, Konventionen.

## Übersicht

| Seite | Inhalt |
|-------|--------|
| [Endpunkte](endpoints.md) | Alle REST-Endpunkte |
| [Datenmodelle](models.md) | Schemas und Typen |
| [Authentifizierung](authentication.md) | API-Keys, Token, Rollen |
| [Fehlerbehandlung](errors.md) | Fehlercodes und Retry-Strategien |
| [Rate Limiting](rate-limiting.md) | Anfragelimits |
| [Webhooks](webhooks.md) | Event-Benachrichtigungen |
| [Versionierung](versioning.md) | API-Versions-Strategie |
| [SDKs & Client-Bibliotheken](sdks.md) | Offizielle Client-Bibliotheken |
| [Beispiele](examples.md) | Praxisnahe API-Nutzung |

## Base URL

```
TODO: https://api.example.com/v1
```

## Konventionen

- JSON als Standard-Format
- UTF-8 Encoding
- ISO 8601 für Datum/Zeit
- Snake_case für Feldnamen
"""),

    ("api/endpoints.md", "API-Endpunkte", """
!!! tip "Inhaltsrichtlinie"
    Alle Endpunkte mit Methode, Pfad, Parametern, Request/Response-Beispielen.

## Endpunkt-Übersicht

| Methode | Pfad | Beschreibung |
|---------|------|-------------|
| TODO | TODO | TODO |

## Endpunkt-Detail-Format

Für jeden Endpunkt:

- HTTP-Methode und Pfad
- Beschreibung
- Path-Parameter, Query-Parameter, Request-Body
- Response (Erfolg + Fehler)
- cURL-Beispiel
- Berechtigungen
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

## Enum-Werte

TODO: Alle Enum-Typen mit möglichen Werten
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

## Token-Lebensdauer

TODO: Wie lange gültig? Refresh-Token?

## Rollen und Berechtigungen

| Rolle | Beschreibung | Zugriffsrechte |
|-------|-------------|---------------|
| TODO | TODO | TODO |

## Sicherheitshinweise

- Tokens niemals in URLs übergeben
- HTTPS immer verwenden
- Tokens regelmäßig rotieren
"""),

    ("api/errors.md", "Fehlerbehandlung", """
!!! tip "Inhaltsrichtlinie"
    HTTP-Statuscodes, Fehlercodes, Retry-Strategien, Client-Beispiele.

## Fehlerformat

```json
{
  "status": "error",
  "code": "ERROR_CODE",
  "message": "Menschenlesbare Beschreibung",
  "details": {}
}
```

## HTTP-Statuscodes

| Code | Bedeutung | Wann |
|------|----------|------|
| 200 | Erfolg | Anfrage erfolgreich |
| 201 | Erstellt | Ressource angelegt |
| 204 | Kein Inhalt | Erfolgreich, keine Antwort |
| 400 | Ungültige Anfrage | Fehlende/ungültige Parameter |
| 401 | Nicht authentifiziert | Kein/ungültiger Token |
| 403 | Zugriff verweigert | Keine Berechtigung |
| 404 | Nicht gefunden | Ressource existiert nicht |
| 409 | Konflikt | Ressource existiert bereits |
| 422 | Validierungsfehler | Semantisch ungültig |
| 429 | Rate Limit | Zu viele Anfragen |
| 500 | Interner Fehler | Unerwarteter Serverfehler |
| 503 | Nicht verfügbar | Wartung/Überlastung |

## Retry-Strategie

TODO: Welche Fehler mit Retry? Exponentielles Backoff?
"""),

    ("api/rate-limiting.md", "Rate Limiting", """
!!! tip "Inhaltsrichtlinie"
    Anfragelimits, Quotas, Header, Strategien bei Limit-Überschreitung.

## Limits

| Endpunkt | Limit | Fenster |
|----------|-------|---------|
| Standard | TODO Req/Min | 1 Minute |
| Auth | TODO Req/Min | 1 Minute |
| Upload | TODO Req/Stunde | 1 Stunde |

## Response-Header

| Header | Beschreibung |
|--------|-------------|
| `X-RateLimit-Limit` | Maximale Anfragen im Fenster |
| `X-RateLimit-Remaining` | Verbleibende Anfragen |
| `X-RateLimit-Reset` | Zeitpunkt des Resets (Unix-Timestamp) |
| `Retry-After` | Sekunden bis zum nächsten Versuch (bei 429) |

## Bei Limit-Überschreitung

```json
{
  "status": "error",
  "code": "RATE_LIMIT_EXCEEDED",
  "message": "Too many requests",
  "retry_after": 30
}
```

## Best Practices

- Anfragen bündeln wo möglich
- `Retry-After` Header respektieren
- Exponentielles Backoff implementieren
- Caching nutzen
"""),

    ("api/webhooks.md", "Webhooks & Events", """
!!! tip "Inhaltsrichtlinie"
    Event-basierte Benachrichtigungen: Webhook-Konfiguration, Events, Payload, Retry, Sicherheit.

## Übersicht

Webhooks senden HTTP-POST-Anfragen an eine konfigurierte URL, wenn bestimmte Events auftreten.

## Events

| Event | Beschreibung | Payload |
|-------|-------------|---------|
| TODO | TODO | TODO |

## Webhook konfigurieren

TODO: Wie registriert man einen Webhook? (API, UI, Config)

## Payload-Format

```json
{
  "event": "resource.created",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {}
}
```

## Sicherheit

- **Signatur**: Jeder Webhook enthält einen HMAC-SHA256 Header zur Verifikation
- **Geheimnis**: Bei Registrierung wird ein Shared Secret erzeugt

```python
import hmac, hashlib
expected = hmac.new(secret, body, hashlib.sha256).hexdigest()
assert hmac.compare_digest(expected, header_signature)
```

## Retry-Verhalten

TODO: Wie oft wird bei Fehler wiederholt? Zeitabstände? Dead-Letter?
"""),

    ("api/versioning.md", "API-Versionierung", """
!!! tip "Inhaltsrichtlinie"
    Versionierungsstrategie, Deprecation-Policy, Migration zwischen Versionen.

## Strategie

TODO: URL-basiert (`/v1/`), Header-basiert, Query-Parameter?

## Aktuelle Versionen

| Version | Status | End-of-Life |
|---------|--------|------------|
| v1 | Aktiv | - |

## Deprecation-Policy

TODO: Wie lange werden alte Versionen unterstützt? Sunset-Header?

## Breaking vs. Non-Breaking Changes

| Art | Beispiel | Version-Bump? |
|-----|---------|---------------|
| Neues Feld in Response | `"new_field": ...` | Nein |
| Neuer optionaler Parameter | `?filter=...` | Nein |
| Feld entfernt | `"old_field"` weg | Ja (Breaking) |
| URL geändert | `/users` → `/accounts` | Ja (Breaking) |

## Migration

TODO: Anleitungen für Migration von v(n) auf v(n+1)
"""),

    ("api/sdks.md", "SDKs & Client-Bibliotheken", """
!!! tip "Inhaltsrichtlinie"
    Offizielle und Community-Client-Bibliotheken für verschiedene Sprachen.

## Offizielle SDKs

| Sprache | Paket | Installation | Status |
|---------|-------|-------------|--------|
| Python | TODO | `pip install ...` | Stabil |
| JavaScript | TODO | `npm install ...` | Stabil |
| Go | TODO | `go get ...` | Beta |

TODO: An tatsächliche SDKs anpassen

## Verwendungsbeispiel (Python)

```python
from sdk import Client

client = Client(api_key="...")
result = client.resource.list()
```

## Verwendungsbeispiel (JavaScript)

```javascript
import { Client } from 'sdk';

const client = new Client({ apiKey: '...' });
const result = await client.resource.list();
```

## Community-Bibliotheken

TODO: Von der Community gepflegte SDKs

## SDK-Versionierung

TODO: Wie hängen SDK-Versionen mit API-Versionen zusammen?
"""),

    ("api/examples.md", "API-Beispiele", """
!!! tip "Inhaltsrichtlinie"
    Praxisnahe Beispiele: cURL, Python, JavaScript für typische API-Workflows.

## Schnellstart

### Authentifizierung

```bash
curl -X POST https://api.example.com/v1/auth/token \\
  -H "Content-Type: application/json" \\
  -d '{"username": "user", "password": "pass"}'
```

### Ressource erstellen

```bash
curl -X POST https://api.example.com/v1/resources \\
  -H "Authorization: Bearer <token>" \\
  -H "Content-Type: application/json" \\
  -d '{"name": "Beispiel"}'
```

### Ressource abrufen

```bash
curl https://api.example.com/v1/resources/123 \\
  -H "Authorization: Bearer <token>"
```

## Typische Workflows

### Workflow 1: TODO

TODO: Mehrstufiger Ablauf mit mehreren API-Aufrufen

## Fehlerbehandlung

```python
import requests

response = requests.get(url, headers=headers)
if response.status_code == 429:
    retry_after = int(response.headers.get("Retry-After", 30))
    time.sleep(retry_after)
    response = requests.get(url, headers=headers)
```

## Pagination

```bash
# Erste Seite
curl "https://api.example.com/v1/resources?page=1&per_page=20"

# Nächste Seite
curl "https://api.example.com/v1/resources?page=2&per_page=20"
```
"""),

    # ━━ Integrationen ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ("integrations/overview.md", "Integrationen — Überblick", """
!!! tip "Inhaltsrichtlinie"
    Übersicht aller verfügbaren Integrationen mit Drittanbieter-Systemen.

## Verfügbare Integrationen

| Integration | Typ | Status | Details |
|------------|-----|--------|---------|
| [SSO / LDAP](sso.md) | Authentifizierung | TODO | Single Sign-On |
| [Webhooks](webhooks.md) | Events | TODO | Event-Benachrichtigungen |
| [CI/CD](ci-cd.md) | Automatisierung | TODO | GitHub Actions, GitLab CI |
| [Drittanbieter](third-party.md) | Extern | TODO | Andere Dienste |

## Integrations-Architektur

TODO: Wie werden Integrationen technisch angebunden? (API, Plugins, Webhooks, Message Queue)
"""),

    ("integrations/sso.md", "SSO / LDAP / OAuth", """
!!! tip "Inhaltsrichtlinie"
    Single Sign-On Anbindung: LDAP, SAML, OAuth2, OpenID Connect.

## Unterstützte Protokolle

| Protokoll | Status | Anbieter |
|----------|--------|---------|
| OAuth2 | TODO | Google, GitHub, Azure AD |
| SAML 2.0 | TODO | ADFS, Okta, Keycloak |
| LDAP | TODO | Active Directory, OpenLDAP |
| OpenID Connect | TODO | Auth0, Keycloak |

## Konfiguration

TODO: Für jedes Protokoll: Konfigurationsschritte, Beispiel-Config

## Benutzer-Mapping

TODO: Wie werden externe Benutzer auf interne Rollen gemappt?

## Fehlerbehandlung

TODO: Häufige SSO-Probleme und Lösungen
"""),

    ("integrations/ci-cd.md", "CI/CD-Integration", """
!!! tip "Inhaltsrichtlinie"
    Integration in CI/CD-Pipelines: GitHub Actions, GitLab CI, Jenkins.

## GitHub Actions

```yaml
name: Build & Deploy
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run
        run: |
          # TODO: Befehle
```

## GitLab CI

```yaml
stages:
  - build
  - test
  - deploy

build:
  stage: build
  script:
    - # TODO: Befehle
```

## Jenkins

TODO: Jenkinsfile-Beispiel

## Allgemeine Hinweise

- Secrets über CI/CD-Umgebungsvariablen bereitstellen
- Artefakte cachen wo möglich
- Tests vor Deployment ausführen
"""),

    ("integrations/webhooks.md", "Webhook-Integrationen", """
!!! tip "Inhaltsrichtlinie"
    Webhook-Anbindung an externe Dienste: Slack, Teams, Jira, E-Mail.

## Slack

TODO: Webhook-URL konfigurieren, Nachrichtenformat

## Microsoft Teams

TODO: Incoming Webhook, Adaptive Cards

## Jira

TODO: Automatisch Issues erstellen bei bestimmten Events

## E-Mail

TODO: SMTP-Konfiguration für E-Mail-Benachrichtigungen

## Eigene Webhooks

TODO: Verweis auf [API-Webhooks](../api/webhooks.md)
"""),

    ("integrations/third-party.md", "Drittanbieter-Integrationen", """
!!! tip "Inhaltsrichtlinie"
    Integration mit häufig genutzten externen Diensten und Tools.

## Cloud-Dienste

| Dienst | Typ | Beschreibung |
|--------|-----|-------------|
| AWS S3 | Storage | Datei-Speicherung |
| Google Cloud | TODO | TODO |
| Azure | TODO | TODO |

TODO: An tatsächliche Integrationen anpassen

## Datenbanken

TODO: Verbindung zu externen Datenbanken

## Monitoring-Dienste

TODO: Datadog, New Relic, Prometheus etc.

## Benachrichtigungsdienste

TODO: PagerDuty, Opsgenie, etc.
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
    Auto-generierte Dokumentation aller Klassen: Konstruktor, Methoden, Vererbung, Verwendungsbeispiele.
"""),

    ("generated/developer/modules/index.md", "Module", """
!!! tip "Inhaltsrichtlinie"
    Auto-generierte Dokumentation aller Module: Zweck, Schnittstelle, Abhängigkeiten, Konfiguration.
"""),

    ("generated/developer/diagrams/index.md", "Diagramme", """
!!! tip "Inhaltsrichtlinie"
    Auto-generierte Mermaid-Diagramme: Klassen-, Sequenz-, Komponenten-, Zustandsdiagramme.
"""),

    # ━━ Entwicklung ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ("development/contributing.md", "Contributing", """
!!! tip "Inhaltsrichtlinie"
    Beitragsrichtlinien: Issues, Pull Requests, Code-Konventionen, Review-Prozess, Code of Conduct.

## Wie kann ich beitragen?

- Bug-Reports als Issues erstellen
- Feature-Requests vorschlagen
- Code-Beiträge via Pull Request
- Dokumentation verbessern
- Übersetzungen beisteuern

## Workflow

1. Issue erstellen oder finden
2. Fork erstellen
3. Branch erstellen (`feature/...` oder `fix/...`)
4. Änderungen implementieren
5. Tests schreiben und ausführen
6. Pull Request erstellen

## Commit-Konventionen

```
feat: Neue Funktion hinzugefügt
fix: Bug in Komponente X behoben
docs: Dokumentation aktualisiert
refactor: Code-Umstrukturierung
test: Tests hinzugefügt
chore: Build/CI-Änderungen
perf: Performance-Verbesserung
```

## Code of Conduct

TODO: Verhaltensregeln für die Community
"""),

    ("development/setup.md", "Entwicklungsumgebung", """
!!! tip "Inhaltsrichtlinie"
    Einrichtung der lokalen Entwicklungsumgebung: Klonen, venv, Abhängigkeiten, IDE, Docker.

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

### VS Code

TODO: Extensions, `settings.json`

### PyCharm

TODO: Interpreter, Run Configurations

## Docker-Entwicklungsumgebung

```bash
docker-compose -f docker-compose.dev.yml up -d
```

## Pre-Commit Hooks

```bash
pre-commit install
```

## Verifizierung

```bash
pytest
flake8 src/
```
"""),

    ("development/code-style.md", "Code-Richtlinien", """
!!! tip "Inhaltsrichtlinie"
    Code-Stil: Formatierung, Namenskonventionen, Docstrings, Logging, Error-Handling, Type Hints.

## Formatierung

TODO: Formatter (Black/Prettier), Linter (flake8/ruff/eslint), Zeilenlänge

## Namenskonventionen

| Element | Konvention | Beispiel |
|---------|-----------|----------|
| Module | snake_case | `my_module.py` |
| Klassen | PascalCase | `MyClass` |
| Funktionen | snake_case | `calculate_total()` |
| Konstanten | UPPER_SNAKE | `MAX_RETRIES` |
| Private | _prefix | `_internal()` |

## Type Hints

TODO: Werden Type Hints verwendet? Welcher Standard?

## Docstrings

TODO: Format (Google, NumPy, Sphinx)

## Fehlerbehandlung

- Spezifische Exceptions verwenden
- Keine leeren `except:`-Blöcke
- Eigene Exception-Klassen für Domänenfehler

## Logging

TODO: Logger-Konventionen, Level-Verwendung
"""),

    ("development/testing.md", "Tests", """
!!! tip "Inhaltsrichtlinie"
    Test-Strategie: Unit/Integration/E2E, Framework, Fixtures, Mocking, Coverage, CI.

## Tests ausführen

```bash
pytest
pytest --cov=src --cov-report=html
pytest tests/test_specific.py -v
pytest -m "not slow"
```

## Test-Pyramide

- **Unit Tests**: Einzelne Funktionen/Klassen
- **Integrationstests**: Komponenten-Zusammenspiel
- **End-to-End Tests**: Gesamter Workflow

## Test-Struktur

TODO: Verzeichnisstruktur, Namenskonventionen

## Fixtures & Mocking

TODO: Gemeinsame Fixtures, Mock-Strategien

## Coverage-Ziele

TODO: Mindest-Coverage, CI-Integration

## Tests für neue Beiträge

Jeder Pull Request muss:

- [ ] Bestehende Tests bestehen
- [ ] Neue Tests für neuen Code enthalten
- [ ] Coverage nicht reduzieren
"""),

    ("development/release.md", "Release-Prozess", """
!!! tip "Inhaltsrichtlinie"
    Versionierung (SemVer), Release-Checkliste, Artefakte, Hotfix, Automatisierung.

## Versionierung

Semantic Versioning: `MAJOR.MINOR.PATCH`

| Segment | Wann | Beispiel |
|---------|------|---------|
| MAJOR | Breaking Changes | 1.0→2.0 |
| MINOR | Neue Features | 1.0→1.1 |
| PATCH | Bugfixes | 1.0.0→1.0.1 |

## Release-Checkliste

- [ ] Alle Tests bestehen
- [ ] Code-Review abgeschlossen
- [ ] Changelog aktualisiert
- [ ] Version angepasst
- [ ] Tag erstellt
- [ ] Artefakte gebaut

## Artefakte

TODO: PyPI, Docker-Image, GitHub-Release?

## Hotfix-Prozess

TODO: Branch von Release-Tag, Fix, PATCH-Version, Merge zurück
"""),

    ("development/debugging.md", "Debugging", """
!!! tip "Inhaltsrichtlinie"
    Debug-Strategien, Werkzeuge, Logging, Profiling, häufige Fehlerquellen.

## Debug-Modus aktivieren

```bash
# Umgebungsvariable
export LOG_LEVEL=DEBUG

# oder Kommandozeile
<command> --verbose
```

## Debugger

### VS Code

TODO: Launch-Configuration, Breakpoints

### pdb (Python)

```python
import pdb; pdb.set_trace()
# oder ab Python 3.7
breakpoint()
```

## Logging analysieren

TODO: Log-Dateien finden, filtern, analysieren

## Profiling

```bash
# CPU-Profiling
python -m cProfile -o profile.out script.py

# Memory-Profiling
python -m memory_profiler script.py
```

## Häufige Fehlerquellen

TODO: Typische Bugs und wie man sie findet

## Remote-Debugging

TODO: Debugging in Docker/Kubernetes/Remote-Servern
"""),

    ("development/ci-cd.md", "CI/CD-Pipeline", """
!!! tip "Inhaltsrichtlinie"
    Aufbau der CI/CD-Pipeline: Stages, Jobs, Secrets, Deployment, Notifications.

## Pipeline-Übersicht

```mermaid
graph LR
    A[Push] --> B[Lint]
    B --> C[Test]
    C --> D[Build]
    D --> E{Branch?}
    E -->|main| F[Deploy Staging]
    F --> G[Deploy Production]
    E -->|feature| H[Preview]
```

## Stages

### 1. Lint

TODO: Welche Linter, Konfiguration

### 2. Test

TODO: Test-Befehle, Coverage-Upload

### 3. Build

TODO: Artefakte bauen (Docker, Pakete)

### 4. Deploy

TODO: Deployment-Strategie pro Umgebung

## Secrets

TODO: Wie werden Secrets in der Pipeline verwaltet?

## Notifications

TODO: Benachrichtigungen bei Build-Fehlern (Slack, E-Mail)

## Pipeline-Konfiguration

TODO: Verweis auf `.github/workflows/`, `.gitlab-ci.yml` o.ä.
"""),

    ("development/dependencies.md", "Abhängigkeiten", """
!!! tip "Inhaltsrichtlinie"
    Abhängigkeitsmanagement: Pakete, Versionen, Updates, Sicherheits-Audits, Lock-Files.

## Direkte Abhängigkeiten

| Paket | Version | Zweck | Lizenz |
|-------|---------|-------|--------|
| TODO | TODO | TODO | TODO |

## Entwicklungs-Abhängigkeiten

| Paket | Version | Zweck |
|-------|---------|-------|
| pytest | TODO | Testing |
| TODO | TODO | TODO |

## Abhängigkeiten aktualisieren

```bash
# Updates prüfen
pip list --outdated

# Sicherheits-Audit
pip audit
# oder
safety check
```

## Lock-Files

TODO: Werden Lock-Files verwendet? (`poetry.lock`, `package-lock.json`)

## Update-Strategie

TODO: Wie oft werden Abhängigkeiten aktualisiert? Automatisiert (Dependabot)?

## Bekannte Inkompatibilitäten

TODO: Versionen die nicht zusammen funktionieren
"""),

    ("development/documentation.md", "Dokumentation schreiben", """
!!! tip "Inhaltsrichtlinie"
    Richtlinien für die Dokumentation: Stil, Format, Struktur, Tools, Build.

## Dokumentations-Stack

- **MkDocs** mit Material Theme
- **Markdown** als Basis-Format
- **Mermaid** für Diagramme
- **Admonitions** für Hinweise

## Dokumentation lokal bauen

```bash
mkdocs serve --dev-addr 0.0.0.0:8000
```

## Stilrichtlinien

- Klare, kurze Sätze
- Aktiv statt Passiv
- Fachbegriffe bei erster Verwendung erklären
- Screenshots / Diagramme wo hilfreich
- Alle Texte auf Deutsch (sofern nicht anders vereinbart)

## Admonitions verwenden

```markdown
!!! note "Hinweis"
    Zusätzliche Information.

!!! warning "Achtung"
    Wichtige Warnung.

!!! tip "Tipp"
    Hilfreicher Tipp.
```

## Diagramme erstellen

```markdown
```mermaid
graph LR
    A --> B --> C
`` `
```

## Code-Beispiele

- Immer lauffähig und getestet
- Sprache im Code-Block angeben
- Kommentare für nicht-offensichtliche Stellen
"""),

    # ━━ Betrieb ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ("operations/deployment.md", "Deployment", """
!!! tip "Inhaltsrichtlinie"
    Deployment-Strategien, Umgebungen, Docker, CI/CD, Rollback, Health Checks.

## Deployment-Strategien

| Strategie | Beschreibung | Risiko |
|-----------|-------------|--------|
| Rolling Update | Schrittweise | Niedrig |
| Blue-Green | Parallele Umgebungen | Mittel |
| Canary | Schrittweise Ausrollung | Niedrig |

## Umgebungen

| Umgebung | Zweck | URL |
|----------|-------|-----|
| Development | Lokal | `localhost:8000` |
| Staging | Test | TODO |
| Production | Live | TODO |

## Docker Deployment

```bash
docker build -t projekt:latest .
docker-compose -f docker-compose.prod.yml up -d
```

## Health Checks

```bash
curl https://app.example.com/health
```

## Rollback

TODO: Schnelles Rollback auf vorherige Version
"""),

    ("operations/monitoring.md", "Monitoring & Logging", """
!!! tip "Inhaltsrichtlinie"
    Metriken, Logging-Konventionen, Alerting, Dashboards, Tracing, Incident Response.

## Wichtige Metriken

| Metrik | Schwellwert | Alert |
|--------|-------------|-------|
| CPU | < 80% | Warning bei 80%, Critical bei 95% |
| RAM | < 85% | Warning bei 85% |
| Antwortzeit P95 | < 500ms | Warning bei 1s |
| Fehlerrate | < 1% | Critical bei 5% |
| Disk | < 90% | Warning bei 85% |

## Logging

TODO: Log-Level, Format, Aggregation (ELK, Loki, CloudWatch)

## Alerting

TODO: Alert-Regeln, Eskalation, Benachrichtigungskanäle

## Dashboards

TODO: Links zu Grafana/Datadog Dashboards

## Distributed Tracing

TODO: OpenTelemetry, Jaeger, Zipkin

## Incident Response

1. Erkennen (Alert)
2. Bestätigen (Acknowledge)
3. Diagnostizieren (Logs, Metriken)
4. Beheben (Fix oder Rollback)
5. Dokumentieren (Post-Mortem)
"""),

    ("operations/backup.md", "Backup & Recovery", """
!!! tip "Inhaltsrichtlinie"
    Backup-Strategie, Zeitpläne, Recovery-Verfahren, RTO/RPO, Verifizierung.

## Was wird gesichert?

| Komponente | Häufigkeit | Aufbewahrung | Methode |
|-----------|-----------|-------------|---------|
| Datenbank | TODO | TODO | TODO |
| Konfiguration | TODO | TODO | TODO |
| Uploads/Medien | TODO | TODO | TODO |
| Logs | TODO | TODO | TODO |

## RTO und RPO

| Metrik | Ziel |
|--------|------|
| **RTO** (Recovery Time Objective) | TODO |
| **RPO** (Recovery Point Objective) | TODO |

## Recovery

TODO: Vollständige Wiederherstellungsschritte

## Backup-Verifizierung

TODO: Wie oft und wie werden Backups getestet?
"""),

    ("operations/security.md", "Sicherheit (Betrieb)", """
!!! tip "Inhaltsrichtlinie"
    Operative Sicherheit: Härtung, Secrets-Rotation, Updates, Netzwerk, Audit.

## Härtungs-Checkliste

- [ ] Debug-Modus deaktiviert
- [ ] HTTPS erzwungen
- [ ] Unnötige Ports geschlossen
- [ ] Default-Credentials geändert
- [ ] Secrets aus Umgebungsvariablen

## Secrets-Rotation

TODO: Welche Secrets, wie oft, automatisiert?

## Sicherheits-Updates

TODO: Wie werden Sicherheitsupdates eingespielt?

## Netzwerk

TODO: Firewall-Regeln, Netzwerk-Segmentierung

## Sicherheitslücke melden

```
Sicherheitslücken bitte per E-Mail an: security@example.com
KEINE öffentlichen Issues für Sicherheitsprobleme.
```

## Verweis

- [Sicherheitsarchitektur](../architecture/security-architecture.md)
- [Compliance & Audit](../compliance/audit.md)
"""),

    ("operations/scaling.md", "Skalierung", """
!!! tip "Inhaltsrichtlinie"
    Praktische Skalierungsanleitungen: Horizontal/Vertikal, Load Balancing, Auto-Scaling.

## Horizontale Skalierung

TODO: Mehr Instanzen hinzufügen

### Load Balancer konfigurieren

TODO: Nginx, HAProxy, Cloud Load Balancer

### Session-Handling

TODO: Sticky Sessions vs. Stateless

## Vertikale Skalierung

TODO: CPU/RAM erhöhen

## Auto-Scaling

TODO: Kubernetes HPA, Cloud Auto-Scaling

## Datenbank-Skalierung

TODO: Read Replicas, Sharding, Connection Pooling

## Verweis

- [Skalierungsarchitektur](../architecture/scalability.md)
"""),

    ("operations/performance.md", "Performance-Tuning", """
!!! tip "Inhaltsrichtlinie"
    Performance messen, Engpässe finden, Optimierungen anwenden.

## Performance messen

### Benchmarks

```bash
# TODO: Benchmark-Befehle
```

### Profiling

TODO: CPU, Memory, I/O Profiling

## Häufige Engpässe

| Engpass | Symptom | Lösung |
|---------|---------|--------|
| Langsame DB-Queries | Hohe Antwortzeit | Indizes, Query-Optimierung |
| Memory Leak | Steigender RAM | Profiling, Fix |
| N+1 Queries | Viele DB-Aufrufe | Eager Loading |
| Kein Caching | Wiederholte Berechnungen | Cache einführen |

## Optimierungen

### Datenbank

TODO: Indizes, Connection Pooling, Query-Optimierung

### Caching

TODO: Redis/Memcached einrichten, Cache-Invalidierung

### Anwendung

TODO: Async I/O, Batch-Verarbeitung, Lazy Loading
"""),

    ("operations/disaster-recovery.md", "Disaster Recovery", """
!!! tip "Inhaltsrichtlinie"
    Notfall-Wiederherstellung: Szenarien, Prozeduren, Kommunikation, Nachbereitung.

## Szenarien

| Szenario | Schwere | RTO | Prozedur |
|---------|---------|-----|---------|
| Datenbank-Ausfall | Hoch | TODO | TODO |
| Komplett-Ausfall | Kritisch | TODO | TODO |
| Datenverlust | Kritisch | TODO | TODO |
| Sicherheitsvorfall | Hoch | TODO | TODO |

## Wiederherstellungs-Prozeduren

### Szenario 1: Datenbank-Ausfall

1. TODO

### Szenario 2: Komplett-Ausfall

1. TODO

## Kommunikationsplan

| Wer | Wann | Wie |
|-----|------|-----|
| Team | Sofort | Slack/Chat |
| Management | < 30 Min | E-Mail |
| Kunden | < 1 Std | Statusseite |

## Post-Mortem Template

- **Datum**: TODO
- **Dauer**: TODO
- **Auswirkung**: TODO
- **Ursache**: TODO
- **Timeline**: TODO
- **Maßnahmen**: TODO
"""),

    ("operations/runbooks.md", "Runbooks", """
!!! tip "Inhaltsrichtlinie"
    Standard Operating Procedures: wiederkehrende Betriebsaufgaben Schritt für Schritt.

## Runbook: Service neustarten

```bash
# 1. Service stoppen
systemctl stop <service>

# 2. Logs prüfen
journalctl -u <service> --since "5 minutes ago"

# 3. Service starten
systemctl start <service>

# 4. Health Check
curl -f http://localhost:8000/health
```

## Runbook: Datenbank-Backup manuell

TODO

## Runbook: Log-Rotation manuell

TODO

## Runbook: SSL-Zertifikat erneuern

TODO

## Runbook: Festplatte voll

TODO

## Runbook: Benutzer sperren

TODO
"""),

    ("operations/infrastructure.md", "Infrastruktur", """
!!! tip "Inhaltsrichtlinie"
    Infrastruktur-Dokumentation: Server, Netzwerk, DNS, Zertifikate, Cloud-Ressourcen.

## Server-Übersicht

| Server | Rolle | OS | Ressourcen | Standort |
|--------|-------|-----|-----------|----------|
| TODO | Application | TODO | TODO | TODO |
| TODO | Database | TODO | TODO | TODO |
| TODO | Load Balancer | TODO | TODO | TODO |

## Netzwerk

TODO: Netzwerk-Diagramm, VPN, Firewalls

## DNS

| Domain | Typ | Ziel | TTL |
|--------|-----|------|-----|
| TODO | A | TODO | TODO |

## SSL-Zertifikate

| Domain | Aussteller | Ablauf | Auto-Renewal |
|--------|----------|--------|-------------|
| TODO | TODO | TODO | TODO |

## Cloud-Ressourcen

TODO: AWS/GCP/Azure Ressourcen-Übersicht

## Infrastructure as Code

TODO: Terraform, Ansible, Pulumi — Verweis auf Repository/Verzeichnis
"""),

    # ━━ Compliance ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ("compliance/overview.md", "Compliance — Überblick", """
!!! tip "Inhaltsrichtlinie"
    Überblick über Compliance-Anforderungen, Datenschutz und regulatorische Pflichten.

## Relevante Regelwerke

| Regelwerk | Beschreibung | Status |
|----------|-------------|--------|
| [DSGVO / Datenschutz](data-protection.md) | EU-Datenschutzgrundverordnung | TODO |
| [Audit & Nachverfolgung](audit.md) | Audit-Trail, Compliance-Berichte | TODO |
| [SLA](sla.md) | Service Level Agreements | TODO |

## Verantwortlichkeiten

TODO: Wer ist für welchen Compliance-Bereich zuständig?

## Regelmäßige Prüfungen

TODO: Welche Prüfungen, wie oft, durch wen?
"""),

    ("compliance/data-protection.md", "Datenschutz & DSGVO", """
!!! tip "Inhaltsrichtlinie"
    Datenschutzmaßnahmen, DSGVO-Konformität, personenbezogene Daten, Löschkonzept.

## Personenbezogene Daten

| Datenfeld | Kategorie | Speicherdauer | Rechtsgrundlage |
|----------|----------|-------------|----------------|
| E-Mail | Kontaktdaten | Während Vertragslaufzeit | Art. 6(1)(b) |
| IP-Adresse | Technisch | 30 Tage | Art. 6(1)(f) |
| TODO | TODO | TODO | TODO |

## Betroffenenrechte

| Recht | Umsetzung |
|-------|----------|
| Auskunft (Art. 15) | TODO |
| Berichtigung (Art. 16) | TODO |
| Löschung (Art. 17) | TODO |
| Datenübertragbarkeit (Art. 20) | TODO |

## Technische Maßnahmen

- Verschlüsselung (Transport + Ruhezustand)
- Pseudonymisierung wo möglich
- Zugriffskontrollen
- Regelmäßige Sicherheitsaudits

## Löschkonzept

TODO: Wann und wie werden Daten gelöscht?

## Auftragsverarbeiter

TODO: Welche Drittanbieter verarbeiten Daten?

## Datenschutz-Folgenabschätzung

TODO: Wurde eine DSFA durchgeführt? Ergebnis?
"""),

    ("compliance/audit.md", "Audit & Nachverfolgung", """
!!! tip "Inhaltsrichtlinie"
    Audit-Trail, Nachverfolgbarkeit von Änderungen, Compliance-Berichte.

## Audit-Trail

### Protokollierte Ereignisse

| Ereignis | Details | Aufbewahrung |
|---------|---------|-------------|
| Login/Logout | User, IP, Zeitpunkt | TODO |
| Datenänderung | User, Vorher/Nachher | TODO |
| Berechtigungsänderung | User, Rolle, Durch wen | TODO |
| Admin-Aktionen | Aktion, Parameter | TODO |

### Audit-Log-Format

TODO: Verweis auf [Log-Formate](../formats/log-formats.md)

## Compliance-Berichte

TODO: Welche Berichte werden automatisch erstellt?

## Zugriff auf Audit-Daten

TODO: Wer darf Audit-Logs einsehen? Wie?

## Manipulationsschutz

TODO: Wie werden Audit-Logs vor Veränderung geschützt?

## Externe Audits

TODO: Wann finden externe Audits statt? Vorbereitung?
"""),

    ("compliance/sla.md", "Service Level Agreements", """
!!! tip "Inhaltsrichtlinie"
    SLA-Definitionen, Verfügbarkeits-Ziele, Reaktionszeiten, Eskalation, Reporting.

## Verfügbarkeit

| Level | Verfügbarkeit | Max. Ausfallzeit/Monat |
|-------|-------------|----------------------|
| Gold | 99.9% | ~44 Minuten |
| Silber | 99.5% | ~3.6 Stunden |
| Bronze | 99.0% | ~7.3 Stunden |

TODO: Welches Level gilt?

## Reaktionszeiten

| Priorität | Beschreibung | Reaktionszeit | Lösungszeit |
|----------|-------------|-------------|-------------|
| P1 — Kritisch | System nicht verfügbar | < 15 Min | < 4 Std |
| P2 — Hoch | Wesentliche Funktion gestört | < 1 Std | < 8 Std |
| P3 — Mittel | Eingeschränkte Funktion | < 4 Std | < 2 Tage |
| P4 — Niedrig | Kosmetisch / Wunsch | < 1 Tag | Nächstes Release |

## Wartungsfenster

TODO: Geplante Wartungsfenster, Benachrichtigung

## Reporting

TODO: SLA-Berichte, Verfügbarkeits-Dashboard

## Eskalation

TODO: Eskalationspfade bei SLA-Verletzung
"""),

    # ━━ Referenz ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ("reference/faq.md", "Häufig gestellte Fragen (FAQ)", """
!!! tip "Inhaltsrichtlinie"
    Häufige Fragen zu Installation, Konfiguration, Verwendung, Fehlerbehebung.

## Allgemein

TODO: Was ist das Projekt? Für wen? Wo Quellcode?

## Installation

TODO: Häufige Installationsprobleme und Lösungen

## Konfiguration

TODO: Häufige Konfigurationsfragen

## Verwendung

TODO: Häufige Nutzungsfragen

## Entwicklung

TODO: Häufige Fragen für Entwickler

## Sonstiges

TODO: Lizenz, Support, Roadmap
"""),

    ("reference/troubleshooting.md", "Fehlerbehebung", """
!!! tip "Inhaltsrichtlinie"
    Systematische Fehlersuche: Häufige Probleme mit Ursache und Lösung, Debug-Modus.

## Allgemeine Vorgehensweise

1. Fehlermeldung lesen
2. Log-Dateien prüfen
3. Konfiguration überprüfen
4. Abhängigkeiten prüfen
5. [FAQ](faq.md) und [Bekannte Probleme](known-issues.md) konsultieren

## Häufige Probleme

### Installation

TODO

### Konfiguration

TODO

### Laufzeit

TODO

### Docker

TODO

### Datenbank

TODO

## Debug-Modus

```bash
export LOG_LEVEL=DEBUG
```

## Hilfe erhalten

TODO: Issue Tracker, Support-Kanäle
"""),

    ("reference/error-codes.md", "Fehlercodes", """
!!! tip "Inhaltsrichtlinie"
    Vollständige Liste aller Fehlercodes mit Beschreibung und Lösung.

## Fehlercodes

| Code | Kategorie | Beschreibung | Lösung |
|------|----------|-------------|--------|
| TODO | TODO | TODO | TODO |

## Fehlercode-Format

```
ERR-<KATEGORIE>-<NUMMER>
```

| Kategorie | Beschreibung |
|----------|-------------|
| AUTH | Authentifizierung & Autorisierung |
| CONFIG | Konfigurationsfehler |
| DB | Datenbankfehler |
| IO | Dateisystem / Netzwerk |
| VALID | Validierungsfehler |
| INTERNAL | Interne Fehler |
"""),

    ("reference/env-variables.md", "Umgebungsvariablen", """
!!! tip "Inhaltsrichtlinie"
    Vollständige Referenz aller unterstützten Umgebungsvariablen.

## Übersicht

| Variable | Pflicht | Standard | Beschreibung |
|----------|---------|---------|-------------|
| `DATABASE_URL` | Ja | - | Datenbank-Verbindung |
| `SECRET_KEY` | Ja | - | Kryptographischer Schlüssel |
| `LOG_LEVEL` | Nein | `INFO` | Logging-Level |
| `PORT` | Nein | `8000` | HTTP-Port |
| `DEBUG` | Nein | `false` | Debug-Modus |

TODO: Alle Umgebungsvariablen auflisten

## Beispiel `.env`

```bash
DATABASE_URL=postgresql://user:pass@localhost/db
SECRET_KEY=ein-langer-zufaelliger-string
LOG_LEVEL=INFO
PORT=8000
DEBUG=false
```

## Priorität

Umgebungsvariablen überschreiben Werte aus der Konfigurationsdatei.
"""),

    ("reference/known-issues.md", "Bekannte Probleme", """
!!! tip "Inhaltsrichtlinie"
    Aktuell bekannte Einschränkungen, Bugs und deren Workarounds.

## Aktuelle Probleme

| # | Beschreibung | Seit | Workaround | Fix geplant |
|---|-------------|------|-----------|-------------|
| TODO | TODO | TODO | TODO | TODO |

## Bekannte Einschränkungen

TODO: Design-bedingte Einschränkungen die kein Bug sind

## Geplante Verbesserungen

TODO: Verweis auf Roadmap / Issue Tracker
"""),

    ("reference/migration-guide.md", "Migrations-Handbuch", """
!!! tip "Inhaltsrichtlinie"
    Anleitungen für die Migration zwischen Major-Versionen.

## Übersicht

| Von | Nach | Schwierigkeit | Anleitung |
|-----|------|-------------|----------|
| 1.x | 2.x | TODO | Siehe unten |

## Migration 1.x → 2.x

### Breaking Changes

TODO

### Schritt-für-Schritt

1. TODO
2. TODO
3. TODO

### Datenbank-Migration

TODO

### Konfigurationsänderungen

| Alt | Neu | Beschreibung |
|-----|-----|-------------|
| TODO | TODO | TODO |
"""),

    ("reference/glossary.md", "Glossar", """
!!! tip "Inhaltsrichtlinie"
    Begriffserklärungen: Fachbegriffe, Abkürzungen, projektspezifische Terminologie.

Alphabetisch sortierte Begriffsdefinitionen.

**API**
: Application Programming Interface — Programmierschnittstelle.

**CRUD**
: Create, Read, Update, Delete — die vier grundlegenden Datenbankoperationen.

**DSGVO**
: Datenschutz-Grundverordnung — EU-Verordnung zum Schutz personenbezogener Daten.

**SLA**
: Service Level Agreement — Vereinbarung über Dienstleistungsqualität.

**SSO**
: Single Sign-On — Einmalige Anmeldung für mehrere Systeme.

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
- **Veraltet** — Features die in Zukunft entfernt werden
- **Entfernt** — Entfernte Features
- **Behoben** — Bugfixes
- **Sicherheit** — Sicherheitsrelevante Änderungen
"""),

    ("reference/license.md", "Lizenz", """
!!! tip "Inhaltsrichtlinie"
    Projektlizenz, Drittanbieter-Lizenzen, Lizenz-Kompatibilität, Beitragsvereinbarung.

## Projektlizenz

TODO: Welche Lizenz? (MIT, Apache 2.0, GPL, etc.)

## Abhängigkeiten

| Bibliothek | Version | Lizenz |
|-----------|---------|--------|
| TODO | TODO | TODO |

## Lizenz-Kompatibilität

TODO: Sind alle Abhängigkeits-Lizenzen kompatibel?

## Beiträge

Durch das Einreichen von Pull Requests erklären Sie sich damit einverstanden,
dass Ihre Beiträge unter derselben Lizenz veröffentlicht werden.
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
