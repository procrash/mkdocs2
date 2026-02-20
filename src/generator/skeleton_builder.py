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
| [Design-System](design/overview.md) | Farben, Typographie, Komponenten, Tokens, Animationen, Dark Mode |
| [Testdokumentation](testing/overview.md) | Testplan, Testfälle, Automatisierung, Regression, Kompatibilität, Testdaten |
| [Projektmanagement](project/overview.md) | Roadmap, Stakeholder, Risiken, Meetings, Onboarding, DoD |
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


    ("getting-started/concepts.md", "Grundkonzepte", """
!!! tip "Inhaltsrichtlinie"
    Zentrale Konzepte und Begriffe die zum Verständnis des Projekts notwendig sind.
    Diese Seite sollte ALLE grundlegenden Konzepte erklären, auf die andere Seiten verweisen.

## Kernkonzepte

Hier sollten die fundamentalen Konzepte des Projekts erklärt werden:

- **Konzept A**: Was ist es? Warum existiert es? Wie wird es verwendet?
- **Konzept B**: Definition, Beispiel, Beziehung zu anderen Konzepten

## Datenmodell (Überblick)

TODO: Vereinfachte Darstellung des Datenmodells für Einsteiger.
Verweis auf [Datenbank-Schema](../formats/database-schema.md) für technische Details.

## Terminologie

| Begriff | Definition |
|---------|-----------|
| TODO | TODO |

Verweis auf [Glossar](../reference/glossary.md) für vollständige Begriffsliste.

## Architektur (vereinfacht)

TODO: Vereinfachtes Diagramm für Einsteiger — keine technischen Details,
nur die großen Blöcke. Verweis auf [Architektur](../architecture/overview.md).

## Beziehung der Konzepte

```mermaid
graph TD
    A[Konzept A] --> B[Konzept B]
    B --> C[Konzept C]
```
"""),


    ("getting-started/hello-world.md", "Hello World — Erstes Beispiel", """
!!! tip "Inhaltsrichtlinie"
    Das kürzestmögliche lauffähige Beispiel. Copy-Paste-fähig, in unter 2 Minuten ausführbar.

## Ziel

Das absolute Minimum zum Laufen bringen — ohne Konfiguration, ohne Vorwissen.

## Voraussetzung

- [Installation](installation.md) abgeschlossen

## Hello World

```bash
# TODO: Minimaler Befehl der ein Ergebnis erzeugt
```

## Erwartetes Ergebnis

TODO: Was sieht der Benutzer? Screenshot oder Terminal-Ausgabe.

## Was passiert hier?

TODO: Kurze Erklärung der einzelnen Schritte (1-2 Sätze pro Schritt)

## Nächste Schritte

- [Schnellstart](quickstart.md) — ausführlicherer Einstieg
- [Grundkonzepte](concepts.md) — die Ideen hinter dem Projekt verstehen
"""),

    ("getting-started/faq-beginners.md", "Einsteiger-FAQ", """
!!! tip "Inhaltsrichtlinie"
    Häufige Fragen von Einsteigern — was typischerweise beim ersten Kontakt unklar ist.
    Unterschied zur [allgemeinen FAQ](../reference/faq.md): hier nur Einstiegsfragen.

## Grundlegendes

### Was genau macht dieses Projekt?

TODO: Elevator Pitch in 2-3 Sätzen

### Für wen ist es gedacht?

TODO: Zielgruppen beschreiben

### Ist es kostenlos / Open Source?

TODO: Lizenzmodell kurz erklären. Verweis auf [Lizenz](../reference/license.md)

### Wo bekomme ich Hilfe?

TODO: Support-Kanäle, Community, Dokumentation

## Technisches

### Welche Programmiersprache wird verwendet?

TODO

### Brauche ich Programmierkenntnisse?

TODO: Für Endanwender? Für Entwickler?

### Funktioniert es auf meinem System?

TODO: Verweis auf [Systemanforderungen](requirements.md) und [Plattformen](../reference/supported-platforms.md)

### Wie aktualisiere ich?

TODO: Verweis auf [Upgrade-Anleitung](upgrade.md)

## Fehler & Probleme

### Die Installation schlägt fehl

TODO: Häufigste Ursachen und Schnell-Fixes

### Es startet nicht

TODO: Erste Diagnoseschritte
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


    ("user-guide/data-management.md", "Datenverwaltung", """
!!! tip "Inhaltsrichtlinie"
    Daten erstellen, bearbeiten, löschen, archivieren.
    Import/Export wird in [Import & Export](../manual/import-export.md) behandelt.

## Daten erstellen

TODO: Neue Datensätze anlegen — Formular, Validierung, Pflichtfelder

## Daten bearbeiten

TODO: Einzelbearbeitung, Massenbearbeitung, Inline-Editing

## Daten löschen

TODO: Soft Delete vs. Hard Delete, Papierkorb, Wiederherstellung

## Daten archivieren

TODO: Archivierungsstrategie, Reaktivierung

## Datenqualität

TODO: Duplikat-Erkennung, Datenbereinigung, Validierungsregeln

## Versionierung

TODO: Werden Änderungen an Datensätzen versioniert? Historie einsehen?

## Speicherung & Limits

TODO: Speicherlimits, Dateigrößen-Limits, Quota
"""),

    ("user-guide/internationalization.md", "Mehrsprachigkeit & Lokalisierung", """
!!! tip "Inhaltsrichtlinie"
    i18n/l10n: Spracheinstellungen, Übersetzungen, Datums-/Zahlenformate, RTL-Support.

## Unterstützte Sprachen

| Sprache | Code | Status | Vollständigkeit |
|---------|------|--------|----------------|
| Deutsch | de | TODO | TODO% |
| Englisch | en | TODO | TODO% |

## Sprache einstellen

TODO: Wo und wie wird die Sprache geändert? (System, Benutzer, URL-Parameter)

## Datums- und Zahlenformate

| Locale | Datumsformat | Zahlenformat |
|--------|-------------|-------------|
| de-DE | DD.MM.YYYY | 1.234,56 |
| en-US | MM/DD/YYYY | 1,234.56 |

## Zeitzonen

TODO: Wie werden Zeitzonen gehandhabt? UTC-Speicherung, lokale Anzeige?

## Eigene Übersetzungen

TODO: Wie können Benutzer Übersetzungen beitragen oder anpassen?

## Rechts-nach-Links (RTL)

TODO: Wird RTL unterstützt? (Arabisch, Hebräisch)
"""),


    ("user-guide/backup-restore.md", "Sicherung & Wiederherstellung", """
!!! tip "Inhaltsrichtlinie"
    Benutzerorientierte Anleitung für Backup und Restore — NICHT die technischen Operations-Details.
    Technische Details in [Backup & Recovery (Betrieb)](../operations/backup.md).

## Eigene Daten sichern

TODO: Wie erstellt der Benutzer ein Backup seiner Daten? (Menü, CLI, API)

## Automatische Sicherung

TODO: Ist Autosave aktiv? Wo werden Backups gespeichert? Wie konfigurieren?

## Backup wiederherstellen

TODO: Schritt-für-Schritt Wiederherstellung aus Backup

## Versionierung & Verlauf

TODO: Können frühere Versionen einzelner Dateien/Datensätze wiederhergestellt werden?

## Export als Backup

TODO: Daten exportieren als zusätzliche Sicherung (CSV, JSON). Verweis auf [Import & Export](../manual/import-export.md)
"""),

    ("user-guide/automation-rules.md", "Automatisierungsregeln", """
!!! tip "Inhaltsrichtlinie"
    Regelbasierte Automatisierung innerhalb der Anwendung: Trigger, Bedingungen, Aktionen.

## Konzept

TODO: Was sind Automatisierungsregeln? Trigger → Bedingung → Aktion

## Regel erstellen

TODO: Schritt-für-Schritt Anleitung

### Trigger-Typen

| Trigger | Beschreibung | Beispiel |
|---------|-------------|---------|
| Zeitbasiert | Zu bestimmten Zeitpunkten | Jeden Montag 8:00 |
| Event-basiert | Bei bestimmten Ereignissen | Neuer Datensatz erstellt |
| Bedingungsbasiert | Wenn Wert sich ändert | Status wechselt auf "Fertig" |

### Bedingungen

TODO: Logische Verknüpfungen (UND, ODER, NICHT), Vergleichsoperatoren

### Aktionen

| Aktion | Beschreibung |
|--------|-------------|
| E-Mail senden | Benachrichtigung versenden |
| Feld setzen | Wert automatisch setzen |
| Webhook aufrufen | Externes System benachrichtigen |
| Datensatz erstellen | Automatisch neuen Eintrag anlegen |

TODO: An tatsächlich verfügbare Aktionen anpassen

## Beispiel-Regeln

TODO: 2-3 praxisnahe Beispiele

## Regeln testen

TODO: Testmodus, Simulation, Protokoll
"""),

    ("user-guide/templates.md", "Vorlagen & Templates", """
!!! tip "Inhaltsrichtlinie"
    Vorlagen verwenden und erstellen: Projekt-Vorlagen, Dokument-Vorlagen, Vorlagen teilen.

## Vorlagen verwenden

TODO: Wie wählt man eine Vorlage aus? Beim Erstellen eines neuen Projekts/Dokuments?

## Verfügbare Vorlagen

| Vorlage | Beschreibung | Anwendungsfall |
|---------|-------------|---------------|
| TODO | TODO | TODO |

## Eigene Vorlage erstellen

TODO: Aus bestehendem Projekt/Dokument eine Vorlage erstellen

## Vorlagen verwalten

TODO: Bearbeiten, Löschen, Duplizieren, Exportieren, Importieren

## Vorlagen teilen

TODO: Vorlagen mit Team/Organisation teilen

## Variablen in Vorlagen

TODO: Platzhalter, dynamische Felder.
Technisches Format: [Template-Formate](../formats/template-formats.md)
"""),

    ("user-guide/tags-categories.md", "Tags & Kategorien", """
!!! tip "Inhaltsrichtlinie"
    Daten organisieren mit Tags und Kategorien: Erstellen, Zuweisen, Filtern, Hierarchien.

## Tags

### Tags erstellen

TODO: Wie erstellt man einen neuen Tag? Name, Farbe, Beschreibung

### Tags zuweisen

TODO: Einem Datensatz Tags zuweisen — per Dropdown, Drag & Drop, Tastenkürzel

### Nach Tags filtern

TODO: Alle Datensätze mit bestimmtem Tag anzeigen. Verweis auf [Suche & Filter](../manual/search.md)

## Kategorien

### Kategorien vs. Tags

| Eigenschaft | Tags | Kategorien |
|-----------|------|-----------|
| Mehrfach-Zuordnung | Ja | Nein (oder begrenzt) |
| Hierarchie | Flach | Hierarchisch |
| Pflicht | Optional | Oft Pflicht |

### Kategorie-Hierarchie

TODO: Können Kategorien verschachtelt werden? Wie tief?

## Automatische Zuordnung

TODO: Regeln für automatische Tag-/Kategorie-Zuordnung.
Verweis auf [Automatisierungsregeln](automation-rules.md)
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


    ("tutorials/beginner-data-import.md", "Tutorial: Erster Datenimport", """
!!! tip "Inhaltsrichtlinie"
    Einsteiger-Tutorial: Daten aus einer externen Quelle importieren und verifizieren.

## Ziel

Am Ende dieses Tutorials haben Sie erfolgreich Daten aus einer CSV-Datei importiert.

## Voraussetzungen

- [Erstes Projekt](beginner-first-project.md) abgeschlossen
- Beispiel-CSV-Datei (siehe unten)

## Beispiel-Daten

```csv
name,email,rolle
Max Mustermann,max@example.com,Editor
Erika Muster,erika@example.com,Viewer
```

## Schritte

### Schritt 1: Import-Funktion aufrufen

TODO: Menü, CLI-Befehl oder API-Aufruf

### Schritt 2: Datei auswählen und Optionen konfigurieren

TODO: Encoding, Trennzeichen, Header-Erkennung

### Schritt 3: Feld-Mapping prüfen

TODO: Quellfelder auf Zielfelder mappen

### Schritt 4: Import ausführen und verifizieren

TODO: Ergebnis prüfen, Fehler-Log einsehen

## Nächste Schritte

- [Grundkonfiguration](beginner-configuration.md)
- [Import & Export Referenz](../manual/import-export.md)
"""),

    ("tutorials/advanced-api-usage.md", "Tutorial: API-Nutzung", """
!!! tip "Inhaltsrichtlinie"
    Fortgeschrittenen-Tutorial: Die REST-API programmatisch nutzen — Authentifizierung, CRUD, Pagination.

## Ziel

Die API mit Python/cURL nutzen um Daten programmatisch zu verwalten.

## Voraussetzungen

- [Grundkonfiguration](beginner-configuration.md) abgeschlossen
- API-Key erstellt (siehe [Authentifizierung](../api/authentication.md))

## Schritte

### Schritt 1: API-Key erstellen

TODO

### Schritt 2: Ersten API-Aufruf machen

```bash
curl -H "Authorization: Bearer <key>" https://localhost:8000/api/v1/health
```

### Schritt 3: Daten lesen (GET)

TODO: Liste abrufen, einzelnen Datensatz abrufen, Pagination

### Schritt 4: Daten erstellen (POST)

TODO: Neuen Datensatz via API erstellen

### Schritt 5: Daten aktualisieren (PUT/PATCH)

TODO

### Schritt 6: Fehlerbehandlung

TODO: HTTP-Statuscodes auswerten, Retry-Logik

## Nächste Schritte

- [API-Referenz](../api/overview.md)
- [SDKs](../api/sdks.md)
"""),

    ("tutorials/advanced-custom-reports.md", "Tutorial: Eigene Berichte", """
!!! tip "Inhaltsrichtlinie"
    Fortgeschrittenen-Tutorial: Benutzerdefinierte Berichte erstellen und automatisieren.

## Ziel

Einen eigenen Bericht erstellen, als PDF exportieren und automatisch versenden.

## Voraussetzungen

- Grundkonfiguration verstanden
- Daten im System vorhanden

## Schritte

### Schritt 1: Berichts-Vorlage erstellen

TODO: Template-Syntax, verfügbare Variablen

### Schritt 2: Datenquelle konfigurieren

TODO: Filter, Zeitraum, Aggregation

### Schritt 3: Layout anpassen

TODO: Kopf-/Fußzeile, Logo, Tabellen, Diagramme

### Schritt 4: Export und Automatisierung

TODO: PDF-Export, Zeitplan, E-Mail-Versand

## Nächste Schritte

- [Drucken & Berichte](../manual/reports.md)
"""),

    ("tutorials/expert-high-availability.md", "Tutorial: Hochverfügbarkeit", """
!!! tip "Inhaltsrichtlinie"
    Experten-Tutorial: System für Hochverfügbarkeit konfigurieren — Clustering, Failover, Monitoring.

## Ziel

Ein hochverfügbares Setup mit automatischem Failover aufbauen.

## Voraussetzungen

- Fortgeschrittene Kenntnisse
- Mehrere Server / Container verfügbar
- Load Balancer vorhanden

## Schritte

### Schritt 1: Architektur planen

TODO: Active-Active vs. Active-Passive, Diagramm

### Schritt 2: Datenbank-Replikation

TODO: Primary-Replica Setup, Synchronisation

### Schritt 3: Application-Cluster

TODO: Mehrere Instanzen, Session-Handling, Health Checks

### Schritt 4: Load Balancer konfigurieren

TODO: Routing-Regeln, Health-Check-Endpoints, Failover

### Schritt 5: Failover testen

TODO: Chaos Engineering, Instance ausschalten, Recovery prüfen

### Schritt 6: Monitoring & Alerting

TODO: Cluster-Metriken, Failover-Alerts

## Verweis

- [Skalierung](../operations/scaling.md)
- [Disaster Recovery](../operations/disaster-recovery.md)
"""),


    ("tutorials/beginner-ui-walkthrough.md", "Tutorial: UI-Rundgang", """
!!! tip "Inhaltsrichtlinie"
    Einsteiger-Tutorial: Geführter Rundgang durch die Benutzeroberfläche — jeder Bereich wird erklärt.

## Ziel

Alle wichtigen Bereiche der Benutzeroberfläche kennenlernen.

## Voraussetzungen

- [Installation](../getting-started/installation.md) abgeschlossen
- Anwendung gestartet

## Schritte

### Schritt 1: Startseite / Dashboard

TODO: Was sieht man nach dem Login? Verweis auf [Dashboard](../manual/dashboard.md)

### Schritt 2: Navigation & Sidebar

TODO: Hauptmenü, Sidebar, Breadcrumbs

### Schritt 3: Daten anzeigen und bearbeiten

TODO: Tabellen, Formulare, Inline-Editing

### Schritt 4: Suche und Filter

TODO: Daten finden. Verweis auf [Suche & Filter](../manual/search.md)

### Schritt 5: Einstellungen

TODO: Persönliche Einstellungen. Verweis auf [Einstellungen](../manual/settings.md)

### Schritt 6: Hilfe finden

TODO: Wo findet man Hilfe innerhalb der Anwendung?

## Zusammenfassung

TODO: Die wichtigsten UI-Bereiche in Kurzform
"""),

    ("tutorials/advanced-webhooks.md", "Tutorial: Webhooks einrichten", """
!!! tip "Inhaltsrichtlinie"
    Fortgeschrittenen-Tutorial: Webhooks konfigurieren, testen und in externe Dienste integrieren.

## Ziel

Einen Webhook einrichten der bei bestimmten Events externe Dienste benachrichtigt.

## Voraussetzungen

- Grundkonfiguration verstanden
- Zugang zu einem externen Dienst (Slack, Teams, oder eigener Server)

## Schritte

### Schritt 1: Webhook-URL bereitstellen

TODO: Externe URL die POST-Requests empfängt (z.B. Slack Incoming Webhook)

### Schritt 2: Webhook in der Anwendung registrieren

TODO: UI oder API. Verweis auf [Webhooks](../api/webhooks.md)

### Schritt 3: Events auswählen

TODO: Welche Events sollen den Webhook auslösen?

### Schritt 4: Testen

TODO: Test-Event senden, Payload prüfen

### Schritt 5: Signatur-Verifikation

TODO: HMAC-Signatur im Empfänger verifizieren

## Fehlerbehebung

TODO: Webhook kommt nicht an, falsche Payload, Timeout

## Verweis

- [Webhook-Integrationen](../integrations/webhooks.md)
- [API-Webhooks](../api/webhooks.md)
"""),

    ("tutorials/advanced-backup-restore.md", "Tutorial: Backup & Restore", """
!!! tip "Inhaltsrichtlinie"
    Fortgeschrittenen-Tutorial: Vollständiges Backup erstellen, verifizieren und wiederherstellen.

## Ziel

Ein komplettes Backup erstellen und die Wiederherstellung erfolgreich durchführen.

## Voraussetzungen

- Admin-Zugang
- Ausreichend Speicherplatz

## Schritte

### Schritt 1: Backup erstellen

```bash
# TODO: Backup-Befehl
```

### Schritt 2: Backup verifizieren

TODO: Integrität prüfen, Inhalt listen

### Schritt 3: Backup sicher aufbewahren

TODO: Externe Speicherung (S3, NAS, etc.)

### Schritt 4: Wiederherstellung testen

TODO: In Test-Umgebung wiederherstellen, Daten prüfen

### Schritt 5: Automatisches Backup einrichten

TODO: Cron-Job oder integrierter Scheduler

## Verweis

- [Backup & Recovery (Betrieb)](../operations/backup.md)
- [Backup-Formate](../formats/backup-formats.md)
"""),

    ("tutorials/expert-security-hardening.md", "Tutorial: Sicherheitshärtung", """
!!! tip "Inhaltsrichtlinie"
    Experten-Tutorial: System für Produktion härten — alle Sicherheitsmaßnahmen Schritt für Schritt.

## Ziel

Ein produktionsreifes, gehärtetes System aufbauen.

## Voraussetzungen

- Fortgeschrittene System-Administration
- Zugang zu Firewall, DNS, Zertifikaten

## Schritte

### Schritt 1: HTTPS erzwingen

TODO: TLS-Zertifikat einrichten (Let\\s Encrypt), HTTP → HTTPS Redirect

### Schritt 2: Firewall konfigurieren

TODO: Nur notwendige Ports öffnen

### Schritt 3: Authentifizierung härten

TODO: MFA aktivieren, Session-Timeout, Brute-Force-Schutz

### Schritt 4: Secrets schützen

TODO: Secrets aus Environment, kein Klartext in Config

### Schritt 5: Updates automatisieren

TODO: Unattended Upgrades, Dependency-Monitoring

### Schritt 6: Audit-Logging aktivieren

TODO: Alle Admin-Aktionen protokollieren

### Schritt 7: Backup verifizieren

TODO: Backup-Integrität regelmäßig testen

## Checkliste

- [ ] HTTPS erzwungen
- [ ] Debug-Modus aus
- [ ] Default-Credentials geändert
- [ ] Firewall konfiguriert
- [ ] MFA aktiviert
- [ ] Audit-Logging aktiv
- [ ] Backups getestet
- [ ] Security-Scan durchgeführt

## Verweis

- [Sicherheit (Betrieb)](../operations/security.md)
- [Sicherheitsarchitektur](../architecture/security-architecture.md)
- [Sicherheitsrichtlinien](../compliance/security-policies.md)
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


    ("manual/dashboard.md", "Dashboard & Startseite", """
!!! tip "Inhaltsrichtlinie"
    Dashboard-Aufbau: Widgets, Kennzahlen, Anpassung, Aktualisierung.

## Standard-Dashboard

TODO: Was sieht der Benutzer nach dem Login? Welche Widgets/Kacheln?

## Widgets

| Widget | Beschreibung | Konfigurierbar |
|--------|-------------|---------------|
| TODO | TODO | Ja/Nein |

## Dashboard anpassen

TODO: Widgets hinzufügen/entfernen, Reihenfolge ändern, Layout

## Kennzahlen (KPIs)

TODO: Welche Kennzahlen werden angezeigt? Wie berechnet?

## Aktualisierung

TODO: Auto-Refresh, manuelle Aktualisierung, Zeitraum-Filter

## Mehrere Dashboards

TODO: Können Benutzer mehrere Dashboards anlegen? Teilen?
"""),

    ("manual/data-views.md", "Datenansichten", """
!!! tip "Inhaltsrichtlinie"
    Verschiedene Darstellungsformen für Daten: Tabelle, Karten, Liste, Kalender, Diagramm.

## Verfügbare Ansichten

| Ansicht | Beschreibung | Geeignet für |
|---------|-------------|-------------|
| Tabelle | Zeilen und Spalten | Große Datenmengen, Sortierung |
| Karten | Kachel-Ansicht | Übersicht mit Vorschau |
| Liste | Kompakte Auflistung | Schnelles Durchblättern |
| Kalender | Zeitbasierte Darstellung | Termine, Deadlines |
| Diagramm | Visualisierung | Auswertungen, Trends |

## Tabellen-Ansicht

TODO: Spalten konfigurieren, sortieren, gruppieren, fixieren

## Karten-Ansicht

TODO: Karteninhalt, Vorschaubild, Gruppierung

## Kalender-Ansicht

TODO: Tages-/Wochen-/Monatsansicht, Drag & Drop

## Ansicht speichern

TODO: Benutzerdefinierte Ansichten speichern und teilen

## Spalten / Felder konfigurieren

TODO: Welche Felder anzeigen, Reihenfolge, Breite
"""),

    ("manual/collaboration.md", "Zusammenarbeit", """
!!! tip "Inhaltsrichtlinie"
    Echtzeit-Zusammenarbeit, Kommentare, Freigaben, Benachrichtigungen im Team-Kontext.

## Echtzeit-Zusammenarbeit

TODO: Gleichzeitige Bearbeitung, Cursor anderer Benutzer sichtbar?

## Kommentare

TODO: Inline-Kommentare, Antworten, @-Mentions, Benachrichtigungen

## Freigabe & Teilen

TODO: Projekt/Dokument teilen, öffentliche Links, Zugriffsrechte

## Aktivitätsverlauf

TODO: Wer hat wann was geändert? Feed, Timeline

## Aufgaben & Zuweisung

TODO: Aufgaben erstellen, zuweisen, Status verfolgen

## Konfliktvermeidung

TODO: Locking, Merge, Benachrichtigung bei Konflikten.
Verweis auf [Mehrbenutzerbetrieb](multi-user.md)
"""),

    ("manual/offline-mode.md", "Offline-Modus", """
!!! tip "Inhaltsrichtlinie"
    Arbeiten ohne Netzwerkverbindung: Funktionsumfang, Synchronisation, Konfliktlösung.

## Verfügbare Funktionen offline

TODO: Was geht offline? Was nicht?

| Funktion | Offline verfügbar | Hinweis |
|----------|-------------------|---------|
| Lesen | TODO | TODO |
| Bearbeiten | TODO | TODO |
| Erstellen | TODO | TODO |

## Offline-Daten vorbereiten

TODO: Welche Daten werden lokal gecacht? Wie konfigurieren?

## Synchronisation

TODO: Automatische Sync bei Wiederverbindung, manuelle Sync

## Konflikte lösen

TODO: Was passiert bei widersprüchlichen Offline-Änderungen?

## Speicherplatz

TODO: Wie viel lokaler Speicher wird benötigt?
"""),

    ("manual/mobile.md", "Mobile Nutzung", """
!!! tip "Inhaltsrichtlinie"
    Mobile App oder responsive Web-Oberfläche: Funktionsumfang, Installation, Unterschiede zur Desktop-Version.

## Mobile App

TODO: Gibt es eine native App? Wo herunterladen? (App Store, Play Store)

## Responsive Web

TODO: Wird die Web-Oberfläche mobil unterstützt? Einschränkungen?

## Funktionsumfang

| Funktion | Desktop | Mobile | Hinweis |
|----------|---------|--------|---------|
| Lesen | ✓ | TODO | TODO |
| Bearbeiten | ✓ | TODO | TODO |
| Erstellen | ✓ | TODO | TODO |
| Administration | ✓ | TODO | TODO |

## Touch-Gesten

TODO: Welche Gesten werden unterstützt? (Swipe, Pinch-to-Zoom, Long-Press)

## Offline auf Mobilgeräten

TODO: Verweis auf [Offline-Modus](offline-mode.md)

## Push-Benachrichtigungen

TODO: Konfiguration auf Mobilgeräten
"""),


    ("manual/file-management.md", "Dateiverwaltung", """
!!! tip "Inhaltsrichtlinie"
    Dateien in der Anwendung verwalten: Hochladen, Organisieren, Vorschau, Herunterladen, Löschen.

## Dateien hochladen

TODO: Drag & Drop, Datei-Dialog, maximale Größe, erlaubte Formate

## Datei-Browser

TODO: Ordnerstruktur, Ansichten (Liste, Kacheln), Sortierung

## Vorschau

| Format | Vorschau verfügbar |
|--------|-------------------|
| Bilder (PNG, JPG, SVG) | TODO |
| PDF | TODO |
| Textdateien | TODO |
| Office-Dokumente | TODO |

## Dateien organisieren

TODO: Ordner erstellen, Verschieben, Umbenennen, Tags zuweisen

## Speicherplatz

TODO: Quota-Anzeige, Speicherplatz freigeben

## Papierkorb

TODO: Gelöschte Dateien wiederherstellen, automatisches Leeren
"""),

    ("manual/templates-usage.md", "Vorlagen verwenden", """
!!! tip "Inhaltsrichtlinie"
    Endanwender-Anleitung: Vorlagen auswählen und anwenden — NICHT Vorlagen erstellen (das ist in [Vorlagen & Templates](../user-guide/templates.md)).

## Vorlage auswählen

TODO: Beim Erstellen eines neuen Dokuments/Projekts → Vorlagen-Auswahl

## Vorlagen-Galerie

TODO: Übersicht der verfügbaren Vorlagen mit Vorschau

## Vorlage anpassen

TODO: Felder ausfüllen, optionale Abschnitte ein-/ausblenden

## Favoriten

TODO: Häufig genutzte Vorlagen als Favoriten markieren

## Verweis

- [Vorlagen & Templates (Benutzerhandbuch)](../user-guide/templates.md)
- [Template-Formate (technisch)](../formats/template-formats.md)
"""),

    ("manual/history-versioning.md", "Verlauf & Versionierung", """
!!! tip "Inhaltsrichtlinie"
    Änderungsverlauf einsehen, Versionen vergleichen, frühere Version wiederherstellen.

## Verlauf anzeigen

TODO: Wo findet man den Änderungsverlauf? (Timeline, Tab, Menü)

## Versionen vergleichen

TODO: Diff-Ansicht, Änderungen farblich markiert (grün=hinzugefügt, rot=entfernt)

## Version wiederherstellen

TODO: Frühere Version als aktuelle setzen, Kopie erstellen

## Wer hat was geändert?

TODO: Benutzer, Zeitstempel, Beschreibung der Änderung

## Automatische Versionierung

TODO: Wird bei jedem Speichern eine Version erstellt? Nur bei explizitem Checkpoint?

## Aufbewahrung

TODO: Wie viele Versionen werden aufbewahrt? Verweis auf [Datenaufbewahrung](../compliance/data-retention.md)
"""),

    ("manual/bulk-operations.md", "Massenoperationen", """
!!! tip "Inhaltsrichtlinie"
    Mehrere Datensätze gleichzeitig bearbeiten: Auswahl, Aktionen, Fortschritt, Rückgängig.

## Datensätze auswählen

TODO: Einzeln per Checkbox, alle auswählen, Bereichsauswahl (Shift+Klick)

## Verfügbare Massenaktionen

| Aktion | Beschreibung |
|--------|-------------|
| Löschen | Ausgewählte Datensätze löschen |
| Tag zuweisen | Allen einen Tag hinzufügen |
| Kategorie ändern | Kategorie für alle setzen |
| Exportieren | Auswahl exportieren |
| Feld ändern | Ein Feld für alle auf gleichen Wert setzen |

TODO: An tatsächliche Aktionen anpassen

## Fortschritt & Abbruch

TODO: Fortschrittsbalken, Abbruch-Möglichkeit bei großen Mengen

## Rückgängig

TODO: Können Massenaktionen rückgängig gemacht werden?

## Limits

TODO: Maximale Anzahl Datensätze pro Massenaktion
"""),

    ("manual/admin-panel.md", "Administrations-Bereich", """
!!! tip "Inhaltsrichtlinie"
    Admin-Panel für Systemadministratoren: Benutzer, Einstellungen, System-Info, Wartung.

## Zugang

TODO: Nur für Administratoren. URL, Menüpunkt, Berechtigungen.

## Benutzer verwalten

TODO: Erstellen, Bearbeiten, Deaktivieren, Passwort zurücksetzen, Rollen zuweisen.
Verweis auf [Berechtigungen & Rollen](../user-guide/permissions.md)

## Systemeinstellungen

TODO: Globale Einstellungen die alle Benutzer betreffen

## System-Informationen

TODO: Version, Lizenz, Speicherverbrauch, aktive Sitzungen, Uptime

## Wartungsmodus

TODO: System in Wartungsmodus versetzen — Benutzer sehen Wartungsseite

## Audit-Log einsehen

TODO: Verweis auf [Audit & Nachverfolgung](../compliance/audit.md)

## Diagnose

TODO: Health-Check, Log-Viewer, System-Diagnose aus dem Admin-Panel
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


    ("formats/template-formats.md", "Template-Formate", """
!!! tip "Inhaltsrichtlinie"
    Formate von Templates und Vorlagen: Syntax, Variablen, Vererbung, Beispiele.

## Template-Engine

TODO: Welche Template-Engine? (Jinja2, Handlebars, Liquid, etc.)

## Syntax

```
{{ variable }}
{% for item in list %}
  {{ item.name }}
{% endfor %}
{% if condition %}...{% endif %}
```

TODO: An tatsächliche Template-Syntax anpassen

## Verfügbare Variablen

| Variable | Typ | Beschreibung |
|----------|-----|-------------|
| TODO | TODO | TODO |

## Template-Vererbung

TODO: Base-Templates, Blöcke, Includes

## Eigene Templates erstellen

TODO: Verzeichnis, Namenskonvention, Registrierung

## Beispiel-Template

TODO: Vollständiges Beispiel eines Custom-Templates
"""),

    ("formats/plugin-formats.md", "Plugin-Formate", """
!!! tip "Inhaltsrichtlinie"
    Plugin-Manifest, Plugin-Verzeichnisstruktur, Schnittstellen-Definition, Lifecycle-Hooks.

## Plugin-Manifest

```json
{
  "name": "mein-plugin",
  "version": "1.0.0",
  "description": "Beschreibung",
  "author": "Autor",
  "main": "index.js",
  "hooks": ["on_load", "on_save"]
}
```

TODO: An tatsächliches Format anpassen

## Verzeichnisstruktur

```
plugins/
  mein-plugin/
    manifest.json
    index.js (oder __init__.py)
    config.yaml
    README.md
```

## Lifecycle-Hooks

| Hook | Zeitpunkt | Parameter |
|------|----------|-----------|
| on_load | Plugin wird geladen | config |
| on_save | Datei wird gespeichert | file_path, content |
| TODO | TODO | TODO |

## Plugin-API

TODO: Verfügbare APIs und Methoden für Plugin-Entwickler
"""),

    ("formats/backup-formats.md", "Backup-Formate", """
!!! tip "Inhaltsrichtlinie"
    Struktur und Format von Backup-Dateien: Inhalt, Komprimierung, Verschlüsselung, Wiederherstellung.

## Backup-Format

TODO: tar.gz, zip, eigenes Format?

## Backup-Inhalt

| Komponente | Enthalten | Pfad im Backup |
|-----------|----------|----------------|
| Datenbank-Dump | Ja | `db/dump.sql` |
| Konfiguration | Ja | `config/` |
| Uploads/Medien | Optional | `media/` |
| Logs | Nein | - |

TODO: An tatsächlichen Backup-Inhalt anpassen

## Backup-Metadaten

```json
{
  "version": "1.0",
  "created_at": "2024-01-15T10:30:00Z",
  "app_version": "2.1.0",
  "components": ["db", "config", "media"]
}
```

## Verschlüsselung

TODO: Ist das Backup verschlüsselt? Welcher Algorithmus?

## Wiederherstellung

TODO: Verweis auf [Backup & Recovery](../operations/backup.md)
"""),

    ("formats/exchange-formats.md", "Austauschformate", """
!!! tip "Inhaltsrichtlinie"
    Formate für den Datenaustausch zwischen Systemen: Bulk-Export, Migration, Synchronisation.

## Standard-Austauschformat

TODO: JSON-Lines, CSV-Bundle, XML-Export?

## Bulk-Export-Format

```jsonl
{"id": "1", "type": "user", "data": {"name": "Max", "email": "max@example.com"}}
{"id": "2", "type": "user", "data": {"name": "Erika", "email": "erika@example.com"}}
```

TODO: An tatsächliches Format anpassen

## Migrations-Paket

TODO: Format für System-zu-System-Migration. Verweis auf [Migrationsformate](migration-formats.md)

## API-Bulk-Format

TODO: Format für Bulk-API-Operationen. Verweis auf [Batch-Operationen](../api/batch-operations.md)

## Validierung

TODO: Schema-Validierung für Austauschformate, Fehlerbehandlung bei ungültigen Daten

## Versionierung

TODO: Wie werden verschiedene Versionen des Austauschformats unterschieden?
"""),


    ("formats/image-formats.md", "Bild- und Medienformate", """
!!! tip "Inhaltsrichtlinie"
    Unterstützte Bildformate, Medienformate, Komprimierung, Thumbnails, Konvertierung.

## Unterstützte Bildformate

| Format | Endung | MIME-Type | Lesen | Schreiben | Thumbnail |
|--------|--------|-----------|-------|----------|----------|
| JPEG | .jpg, .jpeg | image/jpeg | TODO | TODO | TODO |
| PNG | .png | image/png | TODO | TODO | TODO |
| WebP | .webp | image/webp | TODO | TODO | TODO |
| SVG | .svg | image/svg+xml | TODO | TODO | TODO |
| GIF | .gif | image/gif | TODO | TODO | TODO |
| TIFF | .tif, .tiff | image/tiff | TODO | TODO | TODO |

## Größenlimits

| Eigenschaft | Limit |
|------------|-------|
| Max. Dateigröße | TODO MB |
| Max. Auflösung | TODO x TODO px |
| Max. Dateien pro Upload | TODO |

## Thumbnail-Generierung

TODO: Automatisch? Größen? Qualität? Cache?

## Automatische Konvertierung

TODO: Werden Bilder automatisch konvertiert? (z.B. TIFF → WebP)

## Video- und Audio-Formate

TODO: Falls unterstützt — MP4, WebM, MP3, WAV etc.
"""),

    ("formats/report-formats.md", "Berichtsformate", """
!!! tip "Inhaltsrichtlinie"
    Formate für generierte Berichte: PDF-Layout, Excel-Export, HTML-Berichte, Druckoptimierung.

## PDF-Berichte

### Layout

TODO: Seitenformat (A4/Letter), Ränder, Kopf-/Fußzeile

### Inhalte

- Titel, Datum, Ersteller
- Tabellen, Diagramme
- Seitenumbrüche
- Logo / Branding

### Metadaten

```json
{
  "title": "Bericht",
  "author": "System",
  "created": "ISO-8601",
  "pages": 5
}
```

## Excel-Export

TODO: .xlsx-Format, Formatierung, Formeln, mehrere Tabellenblätter

## HTML-Berichte

TODO: Interaktive Berichte, Druckansicht, Responsive

## Berichts-Vorlagen

TODO: Verweis auf [Template-Formate](template-formats.md)
"""),

    ("formats/i18n-formats.md", "Internationalisierungs-Formate", """
!!! tip "Inhaltsrichtlinie"
    Formate für Übersetzungen und Lokalisierung: Sprachdateien, Formate, Tools.

## Sprachdatei-Format

TODO: Welches Format? JSON, YAML, PO/MO, XLIFF, ARB?

### JSON-Format

```json
{
  "greeting": "Hallo",
  "farewell": "Auf Wiedersehen",
  "items_count": "{count} Einträge"
}
```

### PO-Format (gettext)

```
msgid "greeting"
msgstr "Hallo"

msgid "items_count"
msgstr "{count} Einträge"
```

## Datei-Struktur

```
locales/
  de/
    messages.json
    errors.json
  en/
    messages.json
    errors.json
```

## Pluralisierung

TODO: Wie werden Pluralformen behandelt?

## Kontext

TODO: Disambiguierung gleicher Strings in verschiedenen Kontexten

## Verweis

- [Mehrsprachigkeit (Benutzerhandbuch)](../user-guide/internationalization.md)
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


    ("architecture/error-handling.md", "Fehlerbehandlungsstrategie", """
!!! tip "Inhaltsrichtlinie"
    Systemweite Fehlerbehandlung: Exception-Hierarchie, Error Boundaries, Retry, Circuit Breaker.

## Exception-Hierarchie

```
BaseError
├── ValidationError
├── AuthenticationError
├── AuthorizationError
├── NotFoundError
├── ConflictError
├── ExternalServiceError
│   ├── DatabaseError
│   └── ApiClientError
└── InternalError
```

TODO: An tatsächliche Exception-Klassen anpassen

## Fehlerbehandlungs-Strategie

| Schicht | Strategie | Beispiel |
|---------|----------|---------|
| API/Controller | Fangen + HTTP-Mapping | ValidationError → 422 |
| Service | Fangen + Wrapping | DB-Fehler → ServiceError |
| Repository | Propagieren oder Retry | Connection-Timeout → Retry |

## Retry-Strategie

TODO: Exponentielles Backoff, Max-Retries, Jitter

## Circuit Breaker

TODO: Für externe Dienste — Open/Half-Open/Closed States

## Error Logging

TODO: Was wird geloggt? Stack-Traces, Kontext, Korrelations-IDs

## Benutzerfreundliche Fehlermeldungen

TODO: Mapping von technischen Fehlern auf verständliche Meldungen
"""),

    ("architecture/caching.md", "Caching-Architektur", """
!!! tip "Inhaltsrichtlinie"
    Caching-Strategien: Ebenen, Invalidierung, Cache-Aside, Write-Through, TTL.

## Cache-Ebenen

```mermaid
graph LR
    A[Client] --> B[CDN / Browser Cache]
    B --> C[Reverse Proxy Cache]
    C --> D[Application Cache]
    D --> E[Database Query Cache]
    E --> F[Database Buffer]
```

## Strategien

| Strategie | Beschreibung | Einsatz |
|----------|-------------|---------|
| Cache-Aside | App liest/schreibt Cache explizit | Allgemein |
| Write-Through | Schreibt gleichzeitig in Cache + DB | Konsistenz kritisch |
| Write-Behind | Schreibt asynchron in DB | Hoher Durchsatz |
| Read-Through | Cache lädt selbständig bei Miss | Einfache Nutzung |

## Invalidierung

TODO: TTL-basiert, Event-basiert, manuell, Tag-basiert

## Cache-Keys

TODO: Naming-Convention, Namespace, Versionierung

## Monitoring

TODO: Hit-Rate, Miss-Rate, Eviction-Rate, Speicherverbrauch

## Konfiguration

TODO: Cache-Backend (Redis, Memcached, In-Memory), TTL-Defaults
"""),

    ("architecture/event-system.md", "Event-System", """
!!! tip "Inhaltsrichtlinie"
    Event-Architektur: Event-Typen, Bus/Queue, Publisher/Subscriber, Ordering, Idempotenz.

## Architektur

```mermaid
graph LR
    A[Publisher] --> B[Event Bus / Queue]
    B --> C[Subscriber A]
    B --> D[Subscriber B]
    B --> E[Subscriber C]
```

## Event-Typen

| Event | Beschreibung | Payload |
|-------|-------------|---------|
| `entity.created` | Neuer Datensatz | `{id, type, data}` |
| `entity.updated` | Datensatz geändert | `{id, type, changes}` |
| `entity.deleted` | Datensatz gelöscht | `{id, type}` |
| `user.login` | Benutzer angemeldet | `{user_id, ip}` |

TODO: An tatsächliche Events anpassen

## Event-Format

```json
{
  "event_id": "uuid",
  "event_type": "entity.created",
  "timestamp": "ISO-8601",
  "source": "service-name",
  "data": {},
  "metadata": {"correlation_id": "..."}
}
```

## Garantien

TODO: At-least-once, at-most-once, exactly-once? Ordering?

## Idempotenz

TODO: Wie werden doppelt empfangene Events behandelt?

## Dead Letter Queue

TODO: Was passiert mit Events die nicht verarbeitet werden können?
"""),

    ("architecture/deployment-architecture.md", "Deployment-Architektur", """
!!! tip "Inhaltsrichtlinie"
    Deployment-Topologie: Zielplattformen, Container-Orchestrierung, Netzwerk-Layout, Umgebungen.

## Deployment-Diagramm

```mermaid
graph TD
    subgraph "Internet"
        U[Users]
    end
    subgraph "Edge"
        CDN[CDN]
        LB[Load Balancer]
    end
    subgraph "Application Tier"
        A1[App Instance 1]
        A2[App Instance 2]
        W1[Worker 1]
    end
    subgraph "Data Tier"
        DB[(Database Primary)]
        DBR[(Database Replica)]
        R[(Redis Cache)]
        MQ[Message Queue]
    end
    U --> CDN --> LB
    LB --> A1
    LB --> A2
    A1 & A2 --> DB
    DB --> DBR
    A1 & A2 --> R
    A1 & A2 --> MQ
    MQ --> W1
```

TODO: An tatsächliche Topologie anpassen

## Zielplattformen

| Plattform | Status | Hinweise |
|----------|--------|---------|
| Docker Compose | TODO | Entwicklung, kleine Deployments |
| Kubernetes | TODO | Produktion, Skalierung |
| Bare Metal | TODO | Legacy, spezielle Anforderungen |
| Cloud (AWS/GCP/Azure) | TODO | Managed Services |

## Netzwerk-Segmentierung

TODO: DMZ, interne Netze, Firewall-Regeln

## Container-Orchestrierung

TODO: Kubernetes Manifeste, Helm Charts, Docker Compose Files
"""),

    ("architecture/testing-architecture.md", "Test-Architektur", """
!!! tip "Inhaltsrichtlinie"
    Test-Strategie auf Architektur-Ebene: Testpyramide, Testbarkeit, Dependency Injection, Mocking.

## Test-Pyramide

```
        /  E2E  \\           wenige, langsam
       / Integr. \\         mittelviele
      /   Unit    \\        viele, schnell
```

## Testbarkeit durch Design

- **Dependency Injection**: Abhängigkeiten von außen injizieren
- **Interface-basiert**: Gegen Interfaces programmieren, nicht Implementierungen
- **Pure Functions**: Wo möglich, Seiteneffekte isolieren

## Test-Kategorien

| Kategorie | Scope | Datenbank | Netzwerk | Dauer |
|----------|-------|----------|---------|-------|
| Unit | Einzelne Klasse/Funktion | Mock | Mock | < 1s |
| Integration | Mehrere Komponenten | Test-DB | Mock | < 10s |
| E2E | Gesamtes System | Test-DB | Real | < 60s |
| Performance | Lasttest | Test-DB | Real | Minuten |

## Test-Infrastruktur

TODO: Test-Container (Testcontainers), Fixtures, Factories, Seed-Daten

## Mocking-Strategie

TODO: Was wird gemockt? External APIs, Datenbank, Dateisystem, Uhrzeit

## CI-Integration

TODO: Verweis auf [CI/CD](../development/ci-cd.md)
"""),


    ("architecture/logging-architecture.md", "Logging-Architektur", """
!!! tip "Inhaltsrichtlinie"
    Logging-Architektur: Logger-Hierarchie, Sink-Konfiguration, Korrelation, Performance.

## Logger-Hierarchie

```
root
├── app
│   ├── app.api
│   ├── app.service
│   └── app.repository
├── security
│   ├── security.auth
│   └── security.audit
└── integration
    ├── integration.db
    └── integration.http
```

TODO: An tatsächliche Logger-Struktur anpassen

## Sinks / Ausgabeziele

| Sink | Konfiguration | Verwendung |
|------|-------------|-----------|
| Console | stdout/stderr | Entwicklung |
| Datei | Rotation, Komprimierung | Produktion |
| Aggregator | ELK, Loki, CloudWatch | Zentralisiert |
| Audit-DB | Datenbank-Tabelle | Compliance |

## Korrelations-IDs

TODO: Request-ID, Trace-ID, Span-ID für verteiltes Tracing

## Structured Logging

TODO: JSON-Logging, Kontext-Felder, MDC (Mapped Diagnostic Context)

## Performance

TODO: Async-Logging, Buffering, Sampling bei hohem Volumen

## Verweis

- [Logging-Strategie (Betrieb)](../operations/logging-strategy.md)
- [Log-Formate](../formats/log-formats.md)
"""),

    ("architecture/plugin-architecture.md", "Plugin-Architektur", """
!!! tip "Inhaltsrichtlinie"
    Technische Architektur des Plugin-Systems: Lade-Mechanismus, Isolation, API, Lifecycle.

## Architektur-Übersicht

```mermaid
graph TD
    A[Plugin Manager] --> B[Plugin Registry]
    A --> C[Plugin Loader]
    C --> D[Plugin Sandbox]
    D --> E[Plugin Instance]
    E --> F[Hook: on_load]
    E --> G[Hook: on_event]
    E --> H[Hook: on_unload]
```

## Plugin-Lade-Mechanismus

TODO: Wie werden Plugins entdeckt und geladen? (Entry Points, Verzeichnis-Scan, Registry)

## Plugin-Isolation

TODO: Laufen Plugins isoliert? (Separate Prozesse, Sandboxing, Berechtigungen)

## Plugin-API

TODO: Welche APIs stehen Plugins zur Verfügung?

| API | Beschreibung |
|-----|-------------|
| `app.config` | Konfiguration lesen |
| `app.db` | Datenbank-Zugriff (eingeschränkt) |
| `app.events` | Events abonnieren/senden |
| `app.ui` | UI-Erweiterungen registrieren |

## Lifecycle

1. **Discovery**: Plugin-Verzeichnis scannen
2. **Validation**: Manifest prüfen, Abhängigkeiten auflösen
3. **Loading**: Code laden, Initialisierung
4. **Running**: Hooks werden aufgerufen
5. **Unloading**: Aufräumen, Ressourcen freigeben

## Verweis

- [Plugins & Erweiterungen (Benutzerhandbuch)](../user-guide/plugins.md)
- [Plugin-Formate](../formats/plugin-formats.md)
"""),

    ("architecture/queue-architecture.md", "Queue- & Async-Architektur", """
!!! tip "Inhaltsrichtlinie"
    Asynchrone Verarbeitung: Worker, Queues, Job-Scheduling, Retry, Dead-Letter.

## Architektur

```mermaid
graph LR
    A[API] -->|enqueue| B[Message Queue]
    B --> C[Worker 1]
    B --> D[Worker 2]
    C --> E[Result Store]
    D --> E
    B -->|failed| F[Dead Letter Queue]
```

## Queues

| Queue | Priorität | Beschreibung | Worker |
|-------|----------|-------------|--------|
| default | Normal | Allgemeine Aufgaben | 2 |
| high | Hoch | Zeitkritische Aufgaben | 1 |
| bulk | Niedrig | Massenverarbeitung | 1 |

TODO: An tatsächliche Queues anpassen

## Job-Typen

| Job | Queue | Timeout | Retry |
|-----|-------|---------|-------|
| TODO | default | 60s | 3x |

## Retry-Strategie

TODO: Exponentielles Backoff, Max-Retries, Dead Letter nach N Fehlern

## Scheduling

TODO: Wiederkehrende Jobs (Cron-artig), einmalige verzögerte Jobs

## Monitoring

TODO: Queue-Länge, Durchsatz, Fehlerrate, Worker-Status

## Verweis

- [Event-System](event-system.md)
- [Message Queue Integration](../integrations/messaging.md)
"""),

    ("architecture/database-architecture.md", "Datenbank-Architektur", """
!!! tip "Inhaltsrichtlinie"
    Datenbank-Designentscheidungen: Normalisierung, Indizierung, Partitionierung, Replikation.

## Design-Prinzipien

- **Normalisierung**: Mindestens 3. Normalform für Stammdaten
- **Denormalisierung**: Gezielt für Performance-kritische Abfragen
- **Soft Delete**: Datensätze werden markiert, nicht gelöscht
- **Audit-Felder**: `created_at`, `updated_at`, `created_by` auf allen Tabellen

## Indizierungs-Strategie

TODO: Primärschlüssel, Fremdschlüssel, häufige Abfragen, Composite Indexes

## Partitionierung

TODO: Zeitbasiert, Range-basiert? Für welche Tabellen?

## Replikation

TODO: Primary-Replica Setup, Read-Routing

## Connection Pooling

TODO: Pool-Größe, Timeout, Health Checks

## Migrationen

TODO: Verweis auf [Migrationsformate](../formats/migration-formats.md)

## Verweis

- [Datenbank-Schema](../formats/database-schema.md)
- [Externe Datenbanken](../integrations/database.md)
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


    ("api/graphql.md", "GraphQL API", """
!!! tip "Inhaltsrichtlinie"
    GraphQL-Endpunkt: Schema, Queries, Mutations, Subscriptions, Playground.
    Nur relevant falls die Anwendung eine GraphQL-API anbietet.

## Endpunkt

```
POST /graphql
```

## Schema

TODO: GraphQL-Schema oder Verweis auf Schema-Datei

## Queries

```graphql
query {
  users(first: 10) {
    edges {
      node {
        id
        name
        email
      }
    }
    pageInfo {
      hasNextPage
    }
  }
}
```

## Mutations

```graphql
mutation {
  createUser(input: {name: "Max", email: "max@example.com"}) {
    user {
      id
      name
    }
    errors {
      field
      message
    }
  }
}
```

## Subscriptions

TODO: Echtzeit-Updates via WebSocket

## Playground / Explorer

TODO: URL zum GraphQL Playground, Introspection

## Authentifizierung

TODO: Bearer Token im Header, wie bei REST-API
"""),

    ("api/websockets.md", "WebSocket API", """
!!! tip "Inhaltsrichtlinie"
    WebSocket-Endpunkte: Verbindungsaufbau, Nachrichtenformate, Events, Reconnection.
    Nur relevant falls die Anwendung WebSockets nutzt.

## Verbindungsaufbau

```javascript
const ws = new WebSocket('wss://api.example.com/ws');
ws.onopen = () => {
  ws.send(JSON.stringify({type: 'auth', token: '<token>'}));
};
```

## Nachrichtenformat

```json
{
  "type": "event_type",
  "data": {},
  "timestamp": "ISO-8601"
}
```

## Events (Server → Client)

| Event | Beschreibung | Payload |
|-------|-------------|---------|
| TODO | TODO | TODO |

## Commands (Client → Server)

| Command | Beschreibung | Parameter |
|---------|-------------|-----------|
| `subscribe` | Kanal abonnieren | `{channel: "..."}` |
| `unsubscribe` | Kanal verlassen | `{channel: "..."}` |

## Reconnection

TODO: Auto-Reconnect, Exponentielles Backoff, Zustandswiederherstellung

## Heartbeat

TODO: Ping/Pong Intervall, Timeout-Erkennung
"""),

    ("api/batch-operations.md", "Batch-Operationen", """
!!! tip "Inhaltsrichtlinie"
    Bulk/Batch-API: Mehrere Operationen in einem Request, Transaktionsverhalten, Limits.

## Batch-Endpunkt

```
POST /api/v1/batch
```

## Request-Format

```json
{
  "operations": [
    {"method": "POST", "path": "/users", "body": {"name": "A"}},
    {"method": "POST", "path": "/users", "body": {"name": "B"}},
    {"method": "DELETE", "path": "/users/123"}
  ]
}
```

## Response-Format

```json
{
  "results": [
    {"status": 201, "body": {"id": "456"}},
    {"status": 201, "body": {"id": "789"}},
    {"status": 204, "body": null}
  ]
}
```

## Transaktionsverhalten

TODO: Alle-oder-nichts? Teilerfolg möglich? Rollback?

## Limits

| Limit | Wert |
|-------|------|
| Max. Operationen pro Batch | TODO |
| Max. Request-Größe | TODO |
| Timeout | TODO |

## Fehlerbehandlung

TODO: Was passiert wenn eine Operation fehlschlägt?
"""),

    ("api/api-changelog.md", "API-Changelog", """
!!! tip "Inhaltsrichtlinie"
    Änderungshistorie der API: Neue Endpunkte, Breaking Changes, Deprecations pro Version.

## Aktuell

### API v1 (aktuell)

#### Änderungen

TODO: Chronologisch, neueste zuerst

#### [Unreleased]

- TODO

## Format

Jeder Eintrag enthält:

- **Datum**: Wann wurde die Änderung veröffentlicht?
- **Typ**: Added / Changed / Deprecated / Removed / Fixed
- **Endpunkt**: Betroffener Endpunkt
- **Beschreibung**: Was hat sich geändert?
- **Migration**: Was müssen API-Nutzer anpassen?

## Deprecation-Hinweise

TODO: Welche Endpunkte/Felder sind deprecated? Bis wann verfügbar?

## Verweis

- [API-Versionierung](versioning.md)
- [Changelog (Gesamt)](../reference/changelog.md)
"""),


    ("api/file-upload.md", "Datei-Upload API", """
!!! tip "Inhaltsrichtlinie"
    Datei-Upload via API: Multipart, Chunked Upload, Presigned URLs, Limits.

## Einfacher Upload

```bash
curl -X POST https://api.example.com/v1/files \\
  -H "Authorization: Bearer <token>" \\
  -F "file=@dokument.pdf" \\
  -F "description=Mein Dokument"
```

## Response

```json
{
  "id": "file-uuid",
  "filename": "dokument.pdf",
  "size": 1048576,
  "mime_type": "application/pdf",
  "url": "/files/file-uuid",
  "created_at": "2024-01-15T10:30:00Z"
}
```

## Chunked Upload (große Dateien)

TODO: Mehrteiliger Upload für Dateien > X MB

## Presigned URLs

TODO: Direkt-Upload zu S3/Storage ohne Umweg über API-Server

## Limits

| Limit | Wert |
|-------|------|
| Max. Dateigröße | TODO MB |
| Max. Dateien pro Request | TODO |
| Erlaubte MIME-Types | TODO |

## Verweis

- [Bild- und Medienformate](../formats/image-formats.md)
"""),

    ("api/search-api.md", "Such-API", """
!!! tip "Inhaltsrichtlinie"
    Such-Endpunkt: Volltextsuche, Filter, Facetten, Highlighting, Autocomplete.

## Endpunkt

```
GET /api/v1/search?q=suchbegriff
```

## Parameter

| Parameter | Typ | Beschreibung |
|-----------|-----|-------------|
| `q` | string | Suchbegriff (Volltextsuche) |
| `type` | string | Ressourcentyp filtern |
| `fields` | string | In welchen Feldern suchen |
| `page` | int | Seite (Pagination) |
| `per_page` | int | Ergebnisse pro Seite |
| `sort` | string | Sortierung (`relevance`, `date`, `name`) |

## Response

```json
{
  "results": [
    {
      "id": "123",
      "type": "document",
      "title": "Treffer",
      "snippet": "...relevanter <mark>Suchbegriff</mark> im Kontext...",
      "score": 0.95
    }
  ],
  "total": 42,
  "facets": {
    "type": {"document": 30, "user": 12}
  }
}
```

## Autocomplete

```
GET /api/v1/search/suggest?q=such
```

TODO: Vorschläge, Tippfehler-Korrektur

## Erweiterte Suche

TODO: Boolesche Operatoren, Phrasensuche, Wildcards, Fuzzy
"""),

    ("api/admin-api.md", "Admin-API", """
!!! tip "Inhaltsrichtlinie"
    API-Endpunkte für Administration: Benutzerverwaltung, Systemstatus, Konfiguration.
    Nur mit Admin-Berechtigung zugänglich.

## Authentifizierung

Erfordert Admin-Rolle. Verweis auf [Authentifizierung](authentication.md).

## Benutzerverwaltung

### Benutzer auflisten

```
GET /api/v1/admin/users?page=1&per_page=20
```

### Benutzer erstellen

```
POST /api/v1/admin/users
{"email": "neu@example.com", "role": "editor"}
```

### Benutzer deaktivieren

```
PATCH /api/v1/admin/users/:id
{"active": false}
```

## Systemstatus

```
GET /api/v1/admin/status
```

```json
{
  "version": "2.1.0",
  "uptime": 86400,
  "database": "ok",
  "cache": "ok",
  "storage": {"used": "5.2GB", "total": "50GB"}
}
```

## Konfiguration

```
GET /api/v1/admin/config
PUT /api/v1/admin/config
```

TODO: Welche Konfigurationen sind via API änderbar?

## Audit-Log

```
GET /api/v1/admin/audit?from=2024-01-01&to=2024-01-31
```
"""),

    ("api/health-api.md", "Health & Status API", """
!!! tip "Inhaltsrichtlinie"
    Health-Check-Endpunkte für Monitoring, Load Balancer, Kubernetes Probes.

## Endpunkte

### Liveness Probe

```
GET /health/live
```

Prüft: Prozess läuft.

```json
{"status": "ok"}
```

### Readiness Probe

```
GET /health/ready
```

Prüft: Alle Abhängigkeiten verfügbar.

```json
{
  "status": "ok",
  "checks": {
    "database": {"status": "ok", "latency_ms": 2},
    "cache": {"status": "ok", "latency_ms": 1},
    "storage": {"status": "ok"}
  }
}
```

### Detaillierter Status

```
GET /health/detail
```

Erfordert Admin-Berechtigung.

```json
{
  "status": "ok",
  "version": "2.1.0",
  "uptime_seconds": 86400,
  "checks": { "..." : "..." },
  "metrics": {
    "requests_total": 150000,
    "active_connections": 42
  }
}
```

## HTTP-Statuscodes

| Status | Bedeutung |
|--------|----------|
| 200 | Alles in Ordnung |
| 503 | Nicht bereit (Dependency down) |

## Kubernetes-Integration

```yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 8000
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8000
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


    ("integrations/monitoring.md", "Monitoring-Integration", """
!!! tip "Inhaltsrichtlinie"
    Integration mit Monitoring-Systemen: Prometheus, Grafana, Datadog, CloudWatch.

## Prometheus

### Metriken-Endpunkt

```
GET /metrics
```

### Verfügbare Metriken

| Metrik | Typ | Beschreibung |
|--------|-----|-------------|
| `app_requests_total` | Counter | Gesamtzahl Requests |
| `app_request_duration_seconds` | Histogram | Antwortzeiten |
| `app_active_connections` | Gauge | Aktive Verbindungen |

TODO: An tatsächliche Metriken anpassen

### Prometheus-Konfiguration

```yaml
scrape_configs:
  - job_name: 'app'
    static_configs:
      - targets: ['app:8000']
```

## Grafana

TODO: Dashboard-Import, vorgefertigte Dashboards

## Health-Check-Endpunkte

| Endpunkt | Prüft | Response |
|----------|-------|---------|
| `/health` | Anwendung läuft | `{"status": "ok"}` |
| `/health/ready` | Alle Abhängigkeiten | `{"db": "ok", "cache": "ok"}` |
| `/health/live` | Prozess lebt | `200 OK` |

## Verweis

- [Monitoring & Logging](../operations/monitoring.md)
"""),

    ("integrations/storage.md", "Externe Speicherdienste", """
!!! tip "Inhaltsrichtlinie"
    Anbindung externer Speicherdienste: S3, GCS, Azure Blob, MinIO, lokales Dateisystem.

## Unterstützte Backends

| Backend | Konfiguration | Beschreibung |
|---------|-------------|-------------|
| Lokal | `STORAGE_BACKEND=local` | Lokales Dateisystem |
| AWS S3 | `STORAGE_BACKEND=s3` | Amazon S3 oder kompatibel |
| GCS | `STORAGE_BACKEND=gcs` | Google Cloud Storage |
| Azure Blob | `STORAGE_BACKEND=azure` | Azure Blob Storage |
| MinIO | `STORAGE_BACKEND=s3` | S3-kompatibel, self-hosted |

## Konfiguration

### AWS S3

```bash
STORAGE_BACKEND=s3
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
S3_BUCKET=mein-bucket
S3_REGION=eu-central-1
```

### Lokales Dateisystem

```bash
STORAGE_BACKEND=local
STORAGE_PATH=/data/uploads
```

## Dateiverwaltung

TODO: Upload, Download, Löschen, Presigned URLs

## Migration zwischen Backends

TODO: Daten von einem Backend zum anderen verschieben
"""),

    ("integrations/messaging.md", "Message Queue Integration", """
!!! tip "Inhaltsrichtlinie"
    Integration mit Message-Queue-Systemen: RabbitMQ, Redis Pub/Sub, Kafka, SQS.

## Unterstützte Systeme

| System | Status | Einsatz |
|--------|--------|---------|
| Redis Pub/Sub | TODO | Einfache Events |
| RabbitMQ | TODO | Zuverlässige Queues |
| Apache Kafka | TODO | High-Throughput Streaming |
| AWS SQS | TODO | Cloud-native Queues |

## Konfiguration

```bash
MESSAGE_BROKER=redis
REDIS_URL=redis://localhost:6379/0
```

TODO: Konfiguration für jedes unterstützte System

## Queues / Topics

| Queue/Topic | Beschreibung | Consumer |
|------------|-------------|---------|
| TODO | TODO | TODO |

## Nachrichtenformat

TODO: Verweis auf [Event-System](../architecture/event-system.md)

## Monitoring

TODO: Queue-Länge, Consumer-Lag, Dead-Letter-Queue
"""),

    ("integrations/database.md", "Externe Datenbanken", """
!!! tip "Inhaltsrichtlinie"
    Anbindung verschiedener Datenbank-Systeme: PostgreSQL, MySQL, SQLite, MongoDB.

## Unterstützte Datenbanken

| Datenbank | Version | Status | Connection-String |
|----------|---------|--------|------------------|
| PostgreSQL | 12+ | TODO | `postgresql://user:pass@host/db` |
| MySQL | 8.0+ | TODO | `mysql://user:pass@host/db` |
| SQLite | 3.x | TODO | `sqlite:///path/to/db.sqlite` |
| MongoDB | 5.0+ | TODO | `mongodb://host:27017/db` |

## Konfiguration

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
DATABASE_POOL_SIZE=10
DATABASE_POOL_TIMEOUT=30
```

## Connection Pooling

TODO: Pool-Größe, Timeout, Health Checks, Reconnection

## Migrations

TODO: Verweis auf [Migrationsformate](../formats/migration-formats.md)

## Replikation

TODO: Read-Replicas konfigurieren, Routing (Schreiben → Primary, Lesen → Replica)
"""),


    ("integrations/email.md", "E-Mail-Integration", """
!!! tip "Inhaltsrichtlinie"
    E-Mail-Versand: SMTP-Konfiguration, Templates, Transaktions-E-Mails, Newsletter.

## SMTP-Konfiguration

```bash
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=noreply@example.com
SMTP_PASSWORD=secret
SMTP_USE_TLS=true
SMTP_FROM=noreply@example.com
```

## E-Mail-Dienste

| Dienst | Konfiguration | Beschreibung |
|--------|-------------|-------------|
| SMTP direkt | Host/Port/Credentials | Eigener Mailserver |
| SendGrid | API-Key | Cloud-Dienst |
| AWS SES | Access Key | Amazon E-Mail-Service |
| Mailgun | API-Key | Cloud-Dienst |

## Transaktions-E-Mails

| E-Mail | Trigger | Template |
|--------|---------|---------|
| Willkommen | Registrierung | `welcome.html` |
| Passwort-Reset | Anforderung | `password-reset.html` |
| Benachrichtigung | Konfigurierbar | `notification.html` |

TODO: An tatsächliche E-Mails anpassen

## E-Mail-Templates

TODO: Template-Engine, Variablen, Vorschau, Testen

## Rate Limiting

TODO: Max. E-Mails pro Stunde/Tag, Queue
"""),

    ("integrations/search-engine.md", "Suchmaschinen-Integration", """
!!! tip "Inhaltsrichtlinie"
    Integration mit dedizierten Suchmaschinen: Elasticsearch, Meilisearch, Typesense, Solr.

## Unterstützte Engines

| Engine | Version | Status |
|--------|---------|--------|
| Elasticsearch | 8.x | TODO |
| Meilisearch | 1.x | TODO |
| Typesense | 0.25+ | TODO |

## Konfiguration

```bash
SEARCH_ENGINE=elasticsearch
SEARCH_URL=http://localhost:9200
SEARCH_INDEX=app_documents
```

## Indizierung

TODO: Welche Daten werden indiziert? Automatisch oder manuell? Echtzeit oder Batch?

## Mapping / Schema

TODO: Feld-Mapping, Analyser, Synonyme, Stoppwörter

## Neuindizierung

```bash
# TODO: Befehl für vollständige Neuindizierung
```

## Verweis

- [Such-API](../api/search-api.md)
- [Suche & Filter (Manual)](../manual/search.md)
"""),

    ("integrations/cdn.md", "CDN-Integration", """
!!! tip "Inhaltsrichtlinie"
    Content Delivery Network: Konfiguration, Cache-Regeln, Invalidierung, Kosten.

## Unterstützte CDNs

| CDN | Status | Konfiguration |
|-----|--------|-------------|
| CloudFront | TODO | AWS-Integration |
| Cloudflare | TODO | DNS-basiert |
| Bunny CDN | TODO | Pull-Zone |

## Konfiguration

```bash
CDN_ENABLED=true
CDN_URL=https://cdn.example.com
CDN_CACHE_TTL=86400
```

## Cache-Regeln

| Pfad | Cache-Dauer | Beschreibung |
|------|-----------|-------------|
| `/static/*` | 1 Jahr | CSS, JS, Bilder (mit Hash) |
| `/media/*` | 1 Tag | Benutzer-Uploads |
| `/api/*` | Kein Cache | API-Antworten |

## Cache-Invalidierung

TODO: Wie wird der CDN-Cache geleert? (API, CLI, automatisch bei Deploy)

## Kosten

TODO: Kostenfaktoren, Monitoring, Optimierung
"""),

    ("integrations/backup-services.md", "Backup-Dienste", """
!!! tip "Inhaltsrichtlinie"
    Integration mit Backup-Diensten: automatische Backups zu S3, GCS, Restic, Borg.

## Unterstützte Dienste

| Dienst | Typ | Konfiguration |
|--------|-----|-------------|
| AWS S3 | Cloud | Bucket + Credentials |
| Google Cloud Storage | Cloud | Bucket + Service Account |
| Restic | Self-hosted | Repository-Pfad |
| Borg | Self-hosted | Repository-Pfad |

## Konfiguration

```bash
BACKUP_PROVIDER=s3
BACKUP_BUCKET=my-backups
BACKUP_SCHEDULE=0 2 * * *  # Täglich um 2:00
BACKUP_RETENTION_DAYS=30
```

## Automatische Backups

TODO: Scheduler, Benachrichtigung bei Erfolg/Fehler

## Wiederherstellung

TODO: Backup auswählen, Restore-Befehl, Verifizierung

## Verweis

- [Backup & Recovery (Betrieb)](../operations/backup.md)
- [Backup-Formate](../formats/backup-formats.md)
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


    ("development/git-workflow.md", "Git-Workflow", """
!!! tip "Inhaltsrichtlinie"
    Branching-Strategie, Merge-Konventionen, Tagging, Release-Branches, Hotfix-Prozess.

## Branching-Modell

```mermaid
gitGraph
    commit
    branch develop
    checkout develop
    commit
    branch feature/login
    checkout feature/login
    commit
    commit
    checkout develop
    merge feature/login
    branch release/1.0
    checkout release/1.0
    commit
    checkout main
    merge release/1.0 tag:"v1.0"
    checkout develop
    merge release/1.0
```

TODO: An tatsächliches Branching-Modell anpassen (GitFlow, GitHub Flow, Trunk-based)

## Branch-Namenskonventionen

| Typ | Muster | Beispiel |
|-----|--------|---------|
| Feature | `feature/<beschreibung>` | `feature/user-auth` |
| Bugfix | `fix/<beschreibung>` | `fix/login-timeout` |
| Hotfix | `hotfix/<beschreibung>` | `hotfix/security-patch` |
| Release | `release/<version>` | `release/1.2.0` |

## Merge-Strategie

TODO: Merge Commit, Squash & Merge, Rebase & Merge?

## Pull Request Regeln

TODO: Mindestens N Reviewer, CI muss grün sein, keine Force-Pushes auf main

## Tags

TODO: Semantic Versioning Tags, wann wird getaggt?
"""),

    ("development/code-review.md", "Code-Review-Richtlinien", """
!!! tip "Inhaltsrichtlinie"
    Code-Review-Prozess: Checkliste, Feedback-Kultur, automatische Prüfungen, Genehmigungsregeln.

## Review-Checkliste

- [ ] Code ist verständlich und gut strukturiert
- [ ] Tests sind vorhanden und aussagekräftig
- [ ] Keine Sicherheitslücken (Injection, XSS, etc.)
- [ ] Performance ist akzeptabel
- [ ] Dokumentation ist aktualisiert (falls nötig)
- [ ] Breaking Changes sind dokumentiert
- [ ] Error Handling ist korrekt

## Feedback-Richtlinien

- **Konstruktiv**: Vorschläge statt Kritik
- **Spezifisch**: Konkrete Verbesserungsvorschläge
- **Begründet**: Warum ist die Änderung besser?
- **Respektvoll**: Unterscheide Person von Code

## Feedback-Kategorien

| Präfix | Bedeutung | Muss behoben werden? |
|--------|----------|---------------------|
| `blocker:` | Verhindert Merge | Ja |
| `suggestion:` | Verbesserungsvorschlag | Optional |
| `question:` | Verständnisfrage | Antwort nötig |
| `nit:` | Kleinkram (Stil, Formatierung) | Optional |

## Automatische Prüfungen

TODO: Linter, Tests, Coverage, Security-Scan in CI

## Genehmigungsregeln

TODO: Wie viele Approvals? Wer darf genehmigen?
"""),

    ("development/api-design.md", "API-Design-Guidelines", """
!!! tip "Inhaltsrichtlinie"
    Richtlinien für das Design neuer API-Endpunkte: Naming, Versionierung, Error-Handling.

## REST-Konventionen

| Aktion | Methode | Pfad | Response |
|--------|---------|------|---------|
| Liste | GET | `/resources` | 200 + Array |
| Detail | GET | `/resources/:id` | 200 + Objekt |
| Erstellen | POST | `/resources` | 201 + Objekt |
| Aktualisieren | PUT/PATCH | `/resources/:id` | 200 + Objekt |
| Löschen | DELETE | `/resources/:id` | 204 |

## Naming-Konventionen

- Pluralform für Ressourcen: `/users`, nicht `/user`
- Kleinbuchstaben, Bindestriche: `/user-profiles`
- Keine Verben in URLs: `/users`, nicht `/getUsers`
- Unterressourcen: `/users/:id/projects`

## Pagination

TODO: Standard-Pagination-Parameter (`page`, `per_page`, `cursor`)

## Filtering & Sorting

TODO: Query-Parameter-Konventionen

## Error-Response-Format

TODO: Verweis auf [Fehlerbehandlung](../api/errors.md)

## Versionierung

TODO: Verweis auf [API-Versionierung](../api/versioning.md)

## Neuen Endpunkt hinzufügen (Checkliste)

- [ ] REST-Konventionen eingehalten
- [ ] Authentifizierung/Autorisierung
- [ ] Validierung der Eingaben
- [ ] Tests geschrieben
- [ ] Dokumentation aktualisiert
- [ ] Rate-Limiting konfiguriert
"""),

    ("development/security-testing.md", "Sicherheitstests", """
!!! tip "Inhaltsrichtlinie"
    Sicherheitstests: SAST, DAST, Dependency-Scanning, Penetration-Tests, OWASP Top 10.

## Test-Typen

| Typ | Tool | Wann | Was wird geprüft |
|-----|------|------|-----------------|
| SAST | TODO (Bandit, SonarQube) | CI | Quellcode auf Schwachstellen |
| DAST | TODO (OWASP ZAP) | Staging | Laufende Anwendung |
| Dependency Scan | TODO (pip audit, npm audit) | CI | Bekannte CVEs |
| Secret Scan | TODO (trufflehog, gitleaks) | CI | Keine Secrets im Code |

## OWASP Top 10 Checkliste

- [ ] A01 — Broken Access Control
- [ ] A02 — Cryptographic Failures
- [ ] A03 — Injection
- [ ] A04 — Insecure Design
- [ ] A05 — Security Misconfiguration
- [ ] A06 — Vulnerable Components
- [ ] A07 — Authentication Failures
- [ ] A08 — Data Integrity Failures
- [ ] A09 — Logging Failures
- [ ] A10 — SSRF

## Penetration-Tests

TODO: Wie oft? Intern/Extern? Scope? Ergebnisse dokumentieren

## Responsible Disclosure

TODO: Verweis auf [Sicherheitslücke melden](../operations/security.md)
"""),

    ("development/performance-testing.md", "Performance-Tests", """
!!! tip "Inhaltsrichtlinie"
    Lasttests, Stresstests, Benchmarks: Tools, Szenarien, Schwellwerte, CI-Integration.

## Test-Typen

| Typ | Ziel | Dauer |
|-----|------|-------|
| Load Test | Normallast simulieren | 10-30 Min |
| Stress Test | Grenzen finden | Bis Fehler |
| Soak Test | Langzeitstabilität | Stunden |
| Spike Test | Plötzliche Lastspitzen | Minuten |

## Tools

TODO: k6, Locust, JMeter, Apache Bench?

## Beispiel-Szenario (k6)

```javascript
import http from 'k6/http';
export const options = {
  vus: 50,
  duration: '5m',
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};
export default function () {
  http.get('https://app.example.com/api/v1/health');
}
```

## Schwellwerte

| Metrik | Akzeptabel | Grenzwert |
|--------|-----------|----------|
| P95 Latenz | < 500ms | < 2s |
| Fehlerrate | < 0.1% | < 1% |
| Durchsatz | > TODO req/s | > TODO req/s |

## CI-Integration

TODO: Performance-Tests in Pipeline, Regression-Erkennung
"""),


    ("development/error-handling-guide.md", "Fehlerbehandlung (Entwickler-Guide)", """
!!! tip "Inhaltsrichtlinie"
    Best Practices für Fehlerbehandlung im Code: Custom Exceptions, Logging, User-Feedback.
    Architektur-Perspektive in [Fehlerbehandlungsstrategie](../architecture/error-handling.md).

## Custom Exceptions

```python
class AppError(Exception):
    def __init__(self, message: str, code: str, status: int = 500):
        self.message = message
        self.code = code
        self.status = status

class NotFoundError(AppError):
    def __init__(self, resource: str, id: str):
        super().__init__(f"{resource} {id} nicht gefunden", "NOT_FOUND", 404)

class ValidationError(AppError):
    def __init__(self, errors: dict):
        super().__init__("Validierungsfehler", "VALIDATION_ERROR", 422)
        self.errors = errors
```

TODO: An tatsächliche Exception-Klassen anpassen

## Regeln

1. **Spezifische Exceptions** statt generische (`ValueError`, `Exception`)
2. **Keine leeren `except:`** — immer Fehlertyp angeben
3. **Kontext loggen** — was wurde versucht? Mit welchen Parametern?
4. **Benutzerfreundlich** — technische Details nur ins Log, nicht in die UI

## Anti-Patterns

- `except: pass` — Fehler verschlucken
- `raise Exception("...")` — unspezifische Exceptions
- Stack-Traces an Benutzer zeigen
"""),

    ("development/logging-guide.md", "Logging (Entwickler-Guide)", """
!!! tip "Inhaltsrichtlinie"
    Logging-Best-Practices für Entwickler: Wann was loggen, Kontext, Performance.
    Architektur in [Logging-Architektur](../architecture/logging-architecture.md).

## Logger erstellen

```python
import logging
logger = logging.getLogger(__name__)
```

## Wann was loggen

| Level | Wann | Beispiel |
|-------|------|---------|
| DEBUG | Detaillierte Diagnose | `logger.debug("Query: %s, params: %s", sql, params)` |
| INFO | Wichtige Geschäftsereignisse | `logger.info("Benutzer %s angemeldet", user_id)` |
| WARNING | Unerwartetes aber behandeltes | `logger.warning("Retry %d/%d für %s", attempt, max, url)` |
| ERROR | Fehler mit Stacktrace | `logger.error("Import fehlgeschlagen", exc_info=True)` |

## Kontext mitgeben

```python
logger.info("Datei verarbeitet", extra={
    "file_id": file.id,
    "size_bytes": file.size,
    "duration_ms": elapsed,
})
```

## Regeln

1. **Keine PII loggen** (Passwörter, E-Mails, Tokens)
2. **Structured Logging** — Key-Value statt Fließtext
3. **Lazy Formatting** — `logger.debug("x=%s", x)` statt `logger.debug(f"x={x}")`
4. **Korrelation** — Request-ID im Kontext mitführen
"""),

    ("development/database-guide.md", "Datenbank (Entwickler-Guide)", """
!!! tip "Inhaltsrichtlinie"
    Datenbank-Best-Practices für Entwickler: Queries, Migrationen, Transaktionen, Performance.
    Architektur in [Datenbank-Architektur](../architecture/database-architecture.md).

## ORM-Nutzung

TODO: Welches ORM? (SQLAlchemy, Django ORM, Prisma, TypeORM)

## Queries

### Do's

- Parameterisierte Queries (nie String-Concatenation!)
- Nur benötigte Felder selektieren
- Eager Loading bei Beziehungen
- Indizes für häufige WHERE/JOIN-Spalten

### Don'ts

- N+1 Queries (Schleife mit DB-Abfrage)
- `SELECT *` in Produktion
- Queries in Templates / Views
- Transaktionen über HTTP-Requests hinweg

## Migrationen schreiben

```bash
# Neue Migration erstellen
# TODO: Migrations-Befehl

# Migration ausführen
# TODO: Migrate-Befehl
```

### Regeln für Migrationen

1. Immer Up + Down bereitstellen
2. Keine Datenverluste
3. Kleine, atomare Schritte
4. In Staging testen vor Produktion

## Transaktionen

TODO: Wann explizite Transaktionen? Isolation Level?
"""),

    ("development/migration-writing.md", "Migrationen schreiben", """
!!! tip "Inhaltsrichtlinie"
    Anleitung zum Schreiben von Datenbank-Migrationen: Konventionen, Beispiele, Testing.

## Namenskonvention

```
YYYYMMDD_HHMMSS_beschreibung.py
```

Beispiel: `20240115_103000_add_user_email_index.py`

## Beispiel-Migration

```python
# TODO: An tatsächliches Migrations-Framework anpassen

def upgrade():
    op.add_column('users', sa.Column('phone', sa.String(50)))
    op.create_index('idx_users_email', 'users', ['email'])

def downgrade():
    op.drop_index('idx_users_email')
    op.drop_column('users', 'phone')
```

## Checkliste

- [ ] Up-Migration geschrieben und getestet
- [ ] Down-Migration geschrieben und getestet
- [ ] Keine Datenverluste
- [ ] Performance bei großen Tabellen bedacht
- [ ] In Staging getestet
- [ ] Review durch zweiten Entwickler

## Häufige Patterns

### Spalte hinzufügen (ohne Downtime)

1. Spalte als nullable hinzufügen
2. Code deployen der neue Spalte befüllt
3. Backfill für bestehende Daten
4. Spalte als NOT NULL setzen (optional)

### Tabelle umbenennen

TODO: Schritt-für-Schritt mit Abwärtskompatibilität

## Verweis

- [Migrationsformate](../formats/migration-formats.md)
"""),

    ("development/accessibility-guide.md", "Accessibility (Entwickler-Guide)", """
!!! tip "Inhaltsrichtlinie"
    Accessibility-Best-Practices für Entwickler: Semantisches HTML, ARIA, Tests, Checkliste.
    Design-Richtlinien in [Accessibility-Richtlinien](../design/accessibility-guidelines.md).

## Semantisches HTML

```html
<!-- Gut -->
<nav aria-label="Hauptnavigation">
  <ul>
    <li><a href="/">Start</a></li>
  </ul>
</nav>

<main>
  <h1>Seitentitel</h1>
  <section aria-labelledby="section-title">
    <h2 id="section-title">Abschnitt</h2>
  </section>
</main>

<!-- Schlecht -->
<div class="nav">
  <div class="item" onclick="navigate()">Start</div>
</div>
```

## ARIA-Regeln

1. **Kein ARIA ist besser als schlechtes ARIA** — semantisches HTML bevorzugen
2. **Keine `role` auf native Elemente** — `<button>` statt `<div role="button">`
3. **Dynamische Inhalte** — `aria-live` für Updates ohne Seitenneuladen
4. **Labels** — Jedes Formularfeld braucht ein `<label>` oder `aria-label`

## Fokus-Management

TODO: Focus-Trap in Modals, Skip-Links, `tabindex`

## Testen

```bash
# axe-core CLI
npx @axe-core/cli http://localhost:8000

# Lighthouse
npx lighthouse http://localhost:8000 --only-categories=accessibility
```

## Checkliste für jeden PR

- [ ] Bilder haben Alt-Texte
- [ ] Formularfelder haben Labels
- [ ] Interaktive Elemente per Tastatur erreichbar
- [ ] Farbkontrast ≥ 4.5:1
- [ ] `lang`-Attribut gesetzt
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


    ("operations/maintenance.md", "Wartung & Pflege", """
!!! tip "Inhaltsrichtlinie"
    Regelmäßige Wartungsaufgaben: Zeitpläne, Checklisten, Automatisierung, Wartungsfenster.

## Regelmäßige Aufgaben

| Aufgabe | Häufigkeit | Automatisiert | Runbook |
|---------|-----------|-------------|---------|
| Log-Rotation | Täglich | TODO | [Runbook](runbooks.md) |
| Backup-Prüfung | Wöchentlich | TODO | [Backup](backup.md) |
| Dependency-Updates | Monatlich | TODO | - |
| SSL-Zertifikat-Prüfung | Monatlich | TODO | [Runbook](runbooks.md) |
| Datenbank-Vacuum | Wöchentlich | TODO | - |
| Speicherplatz-Prüfung | Täglich | TODO | - |

## Wartungsfenster

TODO: Wann? Wie werden Benutzer informiert? Wie lange?

## Wartungsmodus aktivieren

TODO: Wie wird die Anwendung in den Wartungsmodus versetzt?

## Automatisierung

TODO: Cron-Jobs, Systemd-Timer, Kubernetes CronJobs

## Checkliste nach Wartung

- [ ] Anwendung erreichbar
- [ ] Health Checks grün
- [ ] Logs auf Fehler prüfen
- [ ] Monitoring-Alerts prüfen
- [ ] Wartungsmodus deaktiviert
"""),

    ("operations/capacity-planning.md", "Kapazitätsplanung", """
!!! tip "Inhaltsrichtlinie"
    Ressourcen-Planung: aktuelle Nutzung, Wachstumsprognose, Schwellwerte, Kosten.

## Aktuelle Ressourcen

| Ressource | Kapazität | Auslastung | Trend |
|----------|----------|-----------|-------|
| CPU | TODO Cores | TODO% | TODO |
| RAM | TODO GB | TODO% | TODO |
| Festplatte | TODO GB | TODO% | TODO |
| Netzwerk | TODO Mbit/s | TODO% | TODO |

## Wachstumsprognose

TODO: Erwartetes Wachstum (Benutzer, Daten, Requests) über 6/12/24 Monate

## Schwellwerte für Skalierung

| Metrik | Warnung | Skalierung nötig |
|--------|---------|-----------------|
| CPU | > 70% | > 85% |
| RAM | > 75% | > 90% |
| Disk | > 80% | > 90% |

## Kosten-Übersicht

TODO: Aktuelle Infrastruktur-Kosten, Kosten pro Benutzer, Skalierungskosten

## Empfehlungen

TODO: Nächste geplante Skalierungsschritte
"""),

    ("operations/logging-strategy.md", "Logging-Strategie", """
!!! tip "Inhaltsrichtlinie"
    Logging-Konfiguration: Level, Formate, Aggregation, Aufbewahrung, Datenschutz.

## Logging-Level

| Level | Verwendung | Produktion |
|-------|-----------|-----------|
| DEBUG | Entwicklung, detaillierte Diagnose | Aus |
| INFO | Normaler Betrieb, wichtige Ereignisse | An |
| WARNING | Unerwartete Situationen | An |
| ERROR | Fehler die behandelt wurden | An |
| CRITICAL | Systemkritische Fehler | An |

## Log-Aggregation

TODO: ELK Stack, Loki+Grafana, CloudWatch, Datadog

## Strukturiertes Logging

```python
logger.info("Benutzer angemeldet", extra={
    "user_id": user.id,
    "ip": request.remote_addr,
    "method": "oauth2"
})
```

## Aufbewahrung

| Log-Typ | Aufbewahrung | Komprimierung |
|---------|-------------|--------------|
| Application | TODO Tage | Nach 7 Tagen |
| Access | TODO Tage | Nach 3 Tagen |
| Audit | TODO Monate | Nach 30 Tagen |

## Datenschutz in Logs

TODO: Keine PII loggen, Maskierung von E-Mail/IP, DSGVO-Konformität.
Verweis auf [Datenschutz](../compliance/data-protection.md)

## Verweis

- [Log-Formate](../formats/log-formats.md)
- [Monitoring](monitoring.md)
"""),

    ("operations/network.md", "Netzwerk-Konfiguration", """
!!! tip "Inhaltsrichtlinie"
    Netzwerk-Konfiguration: Ports, Firewall, DNS, TLS, Proxy, VPN.

## Ports

| Port | Protokoll | Dienst | Richtung |
|------|----------|--------|---------|
| 80 | HTTP | Redirect → HTTPS | Eingehend |
| 443 | HTTPS | Web-Anwendung | Eingehend |
| TODO | TCP | Datenbank | Intern |
| TODO | TCP | Cache (Redis) | Intern |

## Firewall-Regeln

TODO: Empfohlene iptables/nftables/Cloud-Firewall-Regeln

## TLS-Konfiguration

TODO: Zertifikat-Setup, Let's Encrypt, Mindest-TLS-Version (1.2+)

## Reverse Proxy

TODO: Nginx/Caddy/Traefik-Konfiguration, Proxy-Headers

## DNS

TODO: A-Records, CNAME, MX, SPF/DKIM/DMARC für E-Mail

## VPN

TODO: VPN-Zugang für Administration, WireGuard/OpenVPN

## Verweis

- [Infrastruktur](infrastructure.md)
- [Sicherheitsarchitektur](../architecture/security-architecture.md)
"""),


    ("operations/monitoring-alerts.md", "Alert-Konfiguration", """
!!! tip "Inhaltsrichtlinie"
    Alert-Regeln: Schwellwerte, Eskalation, Benachrichtigungskanäle, Stummschaltung.

## Alert-Regeln

| Alert | Bedingung | Schwere | Kanal |
|-------|----------|---------|-------|
| CPU hoch | > 85% für 5 Min | Warning | Slack |
| CPU kritisch | > 95% für 2 Min | Critical | PagerDuty |
| RAM hoch | > 90% für 5 Min | Warning | Slack |
| Disk voll | > 90% | Critical | PagerDuty |
| Fehlerrate | > 5% für 2 Min | Critical | PagerDuty |
| Antwortzeit P95 | > 2s für 5 Min | Warning | Slack |
| Service down | Health-Check fehl 3x | Critical | PagerDuty |

TODO: An tatsächliche Schwellwerte anpassen

## Eskalation

| Zeit nach Alert | Aktion |
|----------------|--------|
| 0 Min | Benachrichtigung an On-Call |
| 15 Min | Eskalation an Team-Lead |
| 30 Min | Eskalation an Engineering Manager |

## Stummschaltung (Silence)

TODO: Wartungsfenster, bekannte Probleme temporär stummschalten

## Alert-Fatigue vermeiden

- Nur actionable Alerts
- Schwellwerte regelmäßig anpassen
- Flapping-Detection aktivieren
- Alerts gruppieren

## Verweis

- [Monitoring & Logging](monitoring.md)
- [On-Call](on-call.md)
"""),

    ("operations/cost-optimization.md", "Kostenoptimierung", """
!!! tip "Inhaltsrichtlinie"
    Infrastruktur-Kosten optimieren: Cloud-Kosten, Ressourcen-Rightsizing, Reserved Instances.

## Aktuelle Kosten

| Ressource | Monatliche Kosten | Anteil |
|----------|------------------|--------|
| Compute | TODO | TODO% |
| Datenbank | TODO | TODO% |
| Storage | TODO | TODO% |
| Netzwerk | TODO | TODO% |
| **Gesamt** | **TODO** | **100%** |

## Optimierungsmöglichkeiten

### Compute

TODO: Rightsizing, Spot/Preemptible Instances, Auto-Scaling, Scheduling

### Datenbank

TODO: Richtige Instanzgröße, Reserved Instances, Read Replicas nur wenn nötig

### Storage

TODO: Lifecycle-Policies, Compression, Archivierung (S3 Glacier)

### Netzwerk

TODO: CDN, Komprimierung, Caching

## Monitoring

TODO: Cost-Alerts, Budget-Limits, Tagging für Kostenzuordnung

## Verweis

- [Kapazitätsplanung](capacity-planning.md)
"""),

    ("operations/on-call.md", "On-Call & Bereitschaft", """
!!! tip "Inhaltsrichtlinie"
    Bereitschaftsdienst: Rotation, Verantwortlichkeiten, Werkzeuge, Übergabe, Vergütung.

## On-Call-Rotation

| Woche | Primär | Sekundär |
|-------|--------|---------|
| TODO | TODO | TODO |

## Verantwortlichkeiten

### Primärer On-Call

- Alerts innerhalb von TODO Minuten bestätigen
- Erste Diagnose durchführen
- Eskalieren wenn nötig
- Incident-Dokumentation beginnen

### Sekundärer On-Call

- Unterstützung bei Eskalation
- Übernahme bei Nichterreichbarkeit des Primären

## Werkzeuge

| Werkzeug | Zweck |
|---------|-------|
| PagerDuty / Opsgenie | Alert-Routing, Eskalation |
| Slack #incidents | Kommunikation |
| Runbooks | Schritt-für-Schritt Anleitungen |
| Monitoring-Dashboard | Status-Übersicht |

## Übergabe

TODO: Checkliste für On-Call-Übergabe, offene Incidents, bekannte Probleme

## Runbooks

Verweis auf [Runbooks](runbooks.md) — für jeden Alert ein Runbook.

## Vergütung

TODO: Bereitschaftszulage, Regeln
"""),

    ("operations/change-management.md", "Change Management", """
!!! tip "Inhaltsrichtlinie"
    Änderungsmanagement: Klassifizierung, Genehmigung, Durchführung, Dokumentation.

## Change-Kategorien

| Kategorie | Beschreibung | Genehmigung | Beispiel |
|----------|-------------|-------------|---------|
| Standard | Routiniert, geringes Risiko | Automatisch | Dependency-Update |
| Normal | Geplant, moderates Risiko | Team-Lead | Neues Feature |
| Notfall | Ungeplant, dringend | Post-hoc | Hotfix für Sicherheitslücke |

## Change-Prozess

1. **Antrag**: Change beschreiben (Was, Warum, Wann, Risiko)
2. **Bewertung**: Risiko und Auswirkung einschätzen
3. **Genehmigung**: Je nach Kategorie
4. **Planung**: Zeitfenster, Rollback-Plan, Kommunikation
5. **Durchführung**: Change implementieren
6. **Verifizierung**: Funktioniert alles? Monitoring prüfen
7. **Dokumentation**: Change-Log aktualisieren

## Rollback-Plan

TODO: Jeder Change braucht einen dokumentierten Rollback-Plan

## Change-Log

| Datum | Change | Kategorie | Durchgeführt von | Ergebnis |
|-------|--------|----------|-----------------|---------|
| TODO | TODO | TODO | TODO | Erfolgreich/Rollback |

## Verweis

- [Deployment](deployment.md)
- [Runbooks](runbooks.md)
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


    ("compliance/security-policies.md", "Sicherheitsrichtlinien", """
!!! tip "Inhaltsrichtlinie"
    Interne Sicherheitsrichtlinien: Passwort-Policy, Zugriffskontrolle, Verschlüsselung, Entwicklungs-Sicherheit.

## Passwort-Richtlinie

| Anforderung | Wert |
|------------|------|
| Mindestlänge | TODO Zeichen |
| Großbuchstaben | Mindestens 1 |
| Kleinbuchstaben | Mindestens 1 |
| Ziffern | Mindestens 1 |
| Sonderzeichen | Mindestens 1 |
| Max. Alter | TODO Tage |
| Historie | Letzte TODO Passwörter |

## Zugriffskontrolle

TODO: Principle of Least Privilege, Need-to-Know, Trennung der Pflichten

## Verschlüsselungs-Richtlinie

| Kontext | Algorithmus | Schlüssellänge |
|---------|-----------|---------------|
| Passwort-Hash | bcrypt/argon2 | TODO |
| TLS | TODO | 256 bit |
| Daten at rest | AES-256 | 256 bit |

## Entwicklungs-Sicherheit

TODO: Secure SDLC, Code-Review-Pflicht, SAST/DAST, Dependency-Scanning

## Incident-Management

TODO: Verweis auf [Incident Response](incident-response.md)
"""),

    ("compliance/incident-response.md", "Incident Response", """
!!! tip "Inhaltsrichtlinie"
    Vorgehen bei Sicherheitsvorfällen: Erkennung, Eindämmung, Behebung, Kommunikation, Nachbereitung.

## Incident-Schweregrade

| Schweregrad | Beschreibung | Reaktionszeit |
|------------|-------------|-------------|
| P1 — Kritisch | Datenverlust, Breach | < 15 Minuten |
| P2 — Hoch | Potentieller Breach | < 1 Stunde |
| P3 — Mittel | Verdächtiger Zugriff | < 4 Stunden |
| P4 — Niedrig | Policy-Verstoß | < 24 Stunden |

## Incident-Response-Prozess

1. **Erkennung** → Alert, Meldung, Monitoring
2. **Triage** → Schweregrad bestimmen, Team alarmieren
3. **Eindämmung** → Schaden begrenzen (Zugriff sperren, System isolieren)
4. **Untersuchung** → Root Cause Analysis, Umfang bestimmen
5. **Behebung** → Schwachstelle schließen, Systeme wiederherstellen
6. **Kommunikation** → Betroffene informieren, ggf. Behörden melden
7. **Nachbereitung** → Post-Mortem, Maßnahmen, Lessons Learned

## Kommunikationsplan

TODO: Wer wird wann wie informiert?

## Meldepflichten (DSGVO)

TODO: 72-Stunden-Frist, Meldung an Aufsichtsbehörde, Betroffene informieren

## Verweis

- [Disaster Recovery](../operations/disaster-recovery.md)
"""),

    ("compliance/data-retention.md", "Datenaufbewahrung", """
!!! tip "Inhaltsrichtlinie"
    Aufbewahrungsrichtlinien: Welche Daten, wie lange, wo, Löschprozess, gesetzliche Anforderungen.

## Aufbewahrungsfristen

| Datentyp | Aufbewahrung | Rechtsgrundlage | Löschmethode |
|----------|-------------|----------------|-------------|
| Benutzerdaten | Vertragsdauer + TODO | Art. 6(1)(b) DSGVO | Anonymisierung |
| Audit-Logs | TODO Jahre | Compliance | Automatisch |
| Backups | TODO Monate | Betrieblich | Überschreiben |
| Zugriffslogs | TODO Tage | Art. 6(1)(f) DSGVO | Rotation |
| E-Mails | TODO Monate | TODO | Löschen |

## Löschprozess

TODO: Automatische Löschung, manuelle Prüfung, Bestätigung

## Archivierung

TODO: Welche Daten werden archiviert statt gelöscht?

## Löschnachweis

TODO: Wie wird die Löschung dokumentiert und nachgewiesen?

## Verweis

- [Datenschutz & DSGVO](data-protection.md)
"""),

    ("compliance/third-party-risk.md", "Drittanbieter-Risiken", """
!!! tip "Inhaltsrichtlinie"
    Risikobewertung von Drittanbieter-Diensten: Auftragsverarbeitung, Datenweitergabe, Ausfallrisiko.

## Drittanbieter-Übersicht

| Anbieter | Dienst | Datenverarbeitung | AVV vorhanden | Standort |
|----------|--------|------------------|-------------|----------|
| TODO | Hosting | Ja | TODO | TODO |
| TODO | E-Mail | Ja | TODO | TODO |
| TODO | Monitoring | Nein | - | TODO |

## Risikobewertung

| Risiko | Wahrscheinlichkeit | Auswirkung | Maßnahme |
|--------|-------------------|-----------|----------|
| Anbieter-Ausfall | TODO | TODO | TODO |
| Datenverlust | TODO | TODO | TODO |
| Preiserhöhung | TODO | TODO | TODO |

## Auftragsverarbeitung (AVV)

TODO: Welche Anbieter verarbeiten personenbezogene Daten? AVV-Status?

## Exit-Strategie

TODO: Wie wird ein Anbieterwechsel durchgeführt? Datenexport möglich?

## Regelmäßige Überprüfung

TODO: Wie oft werden Drittanbieter überprüft?
"""),


    ("compliance/accessibility-compliance.md", "Barrierefreiheit-Compliance", """
!!! tip "Inhaltsrichtlinie"
    Gesetzliche Anforderungen zur Barrierefreiheit: WCAG, BITV, EAA, Prüfverfahren, Berichte.

## Relevante Gesetze & Standards

| Standard | Region | Anforderung |
|---------|--------|-------------|
| WCAG 2.1 AA | International | W3C Web Content Accessibility Guidelines |
| BITV 2.0 | Deutschland | Barrierefreie-Informationstechnik-Verordnung |
| EAA | EU | European Accessibility Act (ab 2025) |
| ADA | USA | Americans with Disabilities Act |
| EN 301 549 | EU | Europäische Norm für ICT-Barrierefreiheit |

## Aktueller Status

TODO: Welches Level wird eingehalten? Wann wurde zuletzt geprüft?

## Prüfverfahren

TODO: Automatisiert (axe, Lighthouse) + manuell (Screen-Reader, Tastatur)

## BITV-Test-Ergebnis

TODO: Ergebnis der letzten Prüfung, offene Punkte

## Erklärung zur Barrierefreiheit

TODO: Öffentliche Erklärung gem. BITV/EAA

## Verweis

- [Accessibility-Richtlinien (Design)](../design/accessibility-guidelines.md)
- [Accessibility (Entwickler-Guide)](../development/accessibility-guide.md)
- [Barrierefreiheit (Manual)](../manual/accessibility.md)
"""),

    ("compliance/licensing-compliance.md", "Lizenz-Compliance", """
!!! tip "Inhaltsrichtlinie"
    Open-Source-Lizenzen: Kompatibilität, Pflichten, SBOM, License-Scanning.

## Software Bill of Materials (SBOM)

TODO: Vollständige Liste aller Abhängigkeiten mit Lizenzen

## Lizenz-Kategorien

| Kategorie | Lizenzen | Erlaubt | Pflichten |
|----------|---------|---------|----------|
| Permissive | MIT, BSD, Apache 2.0 | Ja | Copyright-Hinweis |
| Weak Copyleft | LGPL, MPL | Bedingt | Änderungen offenlegen |
| Strong Copyleft | GPL, AGPL | Prüfung nötig | Gesamtcode offenlegen |

## Automatisches Scanning

```bash
# TODO: License-Scanning-Tool und Befehl
# pip-licenses, license-checker, FOSSA, Snyk
```

## Inkompatibilitäten

TODO: Bekannte Lizenz-Inkompatibilitäten und wie sie gelöst wurden

## Verweis

- [Lizenz](../reference/license.md)
- [Abhängigkeiten](../development/dependencies.md)
"""),

    ("compliance/export-control.md", "Exportkontrolle & Kryptographie", """
!!! tip "Inhaltsrichtlinie"
    Exportkontrollvorschriften für Software mit Kryptographie: Regelwerke, Klassifizierung, Meldepflichten.

## Relevanz

TODO: Verwendet die Software Verschlüsselung? Wird sie international vertrieben?

## Verwendete Kryptographie

| Algorithmus | Zweck | Schlüssellänge | Export-Klassifizierung |
|-----------|-------|---------------|----------------------|
| AES-256 | Daten-Verschlüsselung | 256 bit | TODO |
| TLS 1.3 | Transport-Verschlüsselung | - | TODO |
| bcrypt | Passwort-Hashing | - | Ausgenommen |

## Regelwerke

| Regelwerk | Region | Beschreibung |
|----------|--------|-------------|
| EAR | USA | Export Administration Regulations |
| EU Dual-Use | EU | Verordnung (EU) 2021/821 |
| Wassenaar | International | Arrangement on Export Controls |

## Meldepflichten

TODO: Müssen Kryptographie-Exporte gemeldet werden?

## Verweis

- [Sicherheitsarchitektur](../architecture/security-architecture.md)
"""),


    ("project/onboarding.md", "Team-Onboarding", """
!!! tip "Inhaltsrichtlinie"
    Onboarding-Plan für neue Teammitglieder: Checkliste, Zeitplan, Mentor, Ressourcen.

## Erste Woche

### Tag 1

- [ ] Zugänge einrichten (Git, CI/CD, Slack, Jira, Cloud)
- [ ] [Entwicklungsumgebung](../development/setup.md) aufsetzen
- [ ] Repository klonen und bauen
- [ ] Tests lokal ausführen

### Tag 2-3

- [ ] [Architektur-Überblick](../architecture/overview.md) lesen
- [ ] [Grundkonzepte](../getting-started/concepts.md) verstehen
- [ ] Code-Basis erkunden, Module-Struktur verstehen
- [ ] Pair-Programming mit Mentor

### Tag 4-5

- [ ] [Code-Richtlinien](../development/code-style.md) lesen
- [ ] [Git-Workflow](../development/git-workflow.md) verstehen
- [ ] Ersten kleinen Bug fixen (Good-First-Issue)
- [ ] Ersten Pull Request erstellen

## Zweite Woche

- [ ] [Tests](../development/testing.md) verstehen und eigene schreiben
- [ ] [CI/CD-Pipeline](../development/ci-cd.md) verstehen
- [ ] Feature-Arbeit beginnen
- [ ] Am Sprint-Planning teilnehmen

## Mentor

TODO: Wer ist Mentor? Wie oft treffen?

## Hilfreiche Links

TODO: Interne Wikis, Slack-Kanäle, Ansprechpartner
"""),

    ("project/definition-of-done.md", "Definition of Done", """
!!! tip "Inhaltsrichtlinie"
    Definition of Done (DoD): Wann gilt eine Aufgabe/Story als fertig?

## Story / Feature

- [ ] Code implementiert und Code-Review abgeschlossen
- [ ] Unit-Tests geschrieben und bestanden
- [ ] Integrationstests bestanden (falls zutreffend)
- [ ] Keine Regressions in bestehenden Tests
- [ ] Coverage nicht reduziert
- [ ] Dokumentation aktualisiert (falls nutzerrelevant)
- [ ] Accessibility geprüft
- [ ] Security-Checkliste geprüft
- [ ] In Staging deployed und getestet
- [ ] Product Owner hat abgenommen

## Bug-Fix

- [ ] Root Cause identifiziert
- [ ] Fix implementiert und reviewed
- [ ] Regressionstest geschrieben
- [ ] In Staging verifiziert

## Spike / Research

- [ ] Ergebnisse dokumentiert
- [ ] Empfehlung formuliert
- [ ] ADR erstellt (falls Architektur-relevant)
- [ ] Im Team vorgestellt

## Release

- [ ] Alle Stories erfüllen DoD
- [ ] Changelog aktualisiert
- [ ] Release Notes geschrieben
- [ ] Abnahmetests bestanden
- [ ] Tag erstellt und deployed
"""),

    ("project/communication-plan.md", "Kommunikationsplan", """
!!! tip "Inhaltsrichtlinie"
    Wer kommuniziert wann was an wen: Kanäle, Frequenz, Vorlagen, Eskalation.

## Regelmäßige Kommunikation

| Was | Wer | An wen | Frequenz | Kanal |
|-----|-----|--------|---------|-------|
| Daily Standup | Team | Team | Täglich | Slack/Meeting |
| Sprint Review | Team | Stakeholder | 2-wöchentlich | Meeting |
| Status-Report | Tech Lead | Management | Monatlich | E-Mail |
| Release Notes | Team | Alle | Bei Release | Dokumentation |
| Incident Report | On-Call | Team + Management | Bei Incident | Slack + E-Mail |

## Kanäle

| Kanal | Zweck | Response-Zeit |
|-------|-------|-------------|
| Slack #general | Allgemeines | Best-effort |
| Slack #incidents | Vorfälle | < 15 Min |
| E-Mail | Formelles, Externes | < 1 Tag |
| Jira-Kommentare | Task-bezogen | < 1 Tag |
| Meeting | Diskussionen | Geplant |

## Vorlagen

### Status-Report

```
## Status-Report KW XX

### Highlights
- TODO

### Risiken / Blocker
- TODO

### Nächste Schritte
- TODO
```

## Eskalation

TODO: Wann und wie wird eskaliert? Verweis auf [On-Call](../operations/on-call.md)
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


    ("reference/configuration-reference.md", "Konfigurationsreferenz", """
!!! tip "Inhaltsrichtlinie"
    Vollständige Referenz ALLER Konfigurationsoptionen — alphabetisch oder nach Kategorie.
    Diese Seite ist die EINE Anlaufstelle für alle Konfigurationsfragen.

## Konfigurationsdatei

TODO: Vollständiger Pfad, Format (YAML/JSON/TOML)

## Optionen (nach Kategorie)

### Allgemein

| Option | Typ | Standard | Beschreibung |
|--------|-----|---------|-------------|
| `app.name` | string | TODO | Anwendungsname |
| `app.debug` | bool | `false` | Debug-Modus |
| `app.log_level` | enum | `INFO` | Logging-Level |

### Datenbank

| Option | Typ | Standard | Beschreibung |
|--------|-----|---------|-------------|
| `database.url` | string | - | Connection-String |
| `database.pool_size` | int | `10` | Connection-Pool-Größe |

### Server

| Option | Typ | Standard | Beschreibung |
|--------|-----|---------|-------------|
| `server.host` | string | `0.0.0.0` | Bind-Adresse |
| `server.port` | int | `8000` | HTTP-Port |

TODO: Alle Optionen nach diesem Schema dokumentieren

## Verweis

- [Umgebungsvariablen](env-variables.md)
- [Konfigurationsdateien](../formats/config-files.md)
"""),

    ("reference/permissions-matrix.md", "Berechtigungsmatrix", """
!!! tip "Inhaltsrichtlinie"
    Vollständige Matrix: Welche Rolle darf welche Aktion auf welcher Ressource ausführen?

## Matrix

| Ressource | Aktion | Admin | Editor | Viewer | API-Key |
|----------|--------|-------|--------|--------|---------|
| Benutzer | Erstellen | ✓ | ✗ | ✗ | ✗ |
| Benutzer | Lesen | ✓ | ✓ | ✓ | ✓ |
| Benutzer | Bearbeiten | ✓ | ✗ | ✗ | ✗ |
| Benutzer | Löschen | ✓ | ✗ | ✗ | ✗ |
| Daten | Erstellen | ✓ | ✓ | ✗ | ✓ |
| Daten | Lesen | ✓ | ✓ | ✓ | ✓ |
| Daten | Bearbeiten | ✓ | ✓ | ✗ | ✓ |
| Daten | Löschen | ✓ | ✗ | ✗ | ✗ |
| Einstellungen | Lesen | ✓ | ✓ | ✗ | ✗ |
| Einstellungen | Ändern | ✓ | ✗ | ✗ | ✗ |

TODO: An tatsächliche Ressourcen und Rollen anpassen

## Spezialberechtigungen

TODO: Zusätzliche Berechtigungen die nicht in die Matrix passen

## Verweis

- [Berechtigungen & Rollen](../user-guide/permissions.md)
- [API-Authentifizierung](../api/authentication.md)
"""),

    ("reference/supported-platforms.md", "Plattform-Unterstützung", """
!!! tip "Inhaltsrichtlinie"
    Support-Matrix: Betriebssysteme, Browser, Architekturen, Container-Runtimes.

## Betriebssysteme

| OS | Version | Architektur | Status |
|-----|---------|------------|--------|
| Ubuntu | 20.04 LTS | amd64, arm64 | Unterstützt |
| Ubuntu | 22.04 LTS | amd64, arm64 | Unterstützt |
| Debian | 11, 12 | amd64 | Unterstützt |
| RHEL | 8, 9 | amd64 | Unterstützt |
| macOS | 12+ | amd64, arm64 | Unterstützt |
| Windows | 10, 11 | amd64 | Unterstützt |
| Windows Server | 2019+ | amd64 | Unterstützt |

TODO: An tatsächlich getestete Plattformen anpassen

## Browser (falls Web-UI)

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | Letzte 2 Versionen | Unterstützt |
| Firefox | Letzte 2 Versionen | Unterstützt |
| Safari | Letzte 2 Versionen | Unterstützt |
| Edge | Letzte 2 Versionen | Unterstützt |

## Container-Runtimes

| Runtime | Version | Status |
|---------|---------|--------|
| Docker | 20.10+ | Unterstützt |
| Podman | 4.0+ | TODO |
| containerd | 1.6+ | TODO |

## Cloud-Plattformen

TODO: AWS, GCP, Azure — welche Dienste wurden getestet?
"""),

    ("reference/release-notes.md", "Release Notes", """
!!! tip "Inhaltsrichtlinie"
    Detaillierte Release Notes pro Version: Highlights, neue Features, Bugfixes, Breaking Changes, Upgrade-Hinweise.
    Unterschied zum [Changelog](changelog.md): Release Notes sind ausführlicher und benutzerorientiert.

## Version X.Y.Z (Datum)

### Highlights

TODO: Die wichtigsten Änderungen in 2-3 Sätzen

### Neue Features

- TODO

### Verbesserungen

- TODO

### Bugfixes

- TODO

### Breaking Changes

- TODO

### Upgrade-Hinweise

TODO: Was muss bei diesem Upgrade beachtet werden?
Verweis auf [Migrations-Handbuch](migration-guide.md)

### Bekannte Probleme

TODO: Verweis auf [Bekannte Probleme](known-issues.md)
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

    ("reference/tags.md", "Tags", """
Auf dieser Seite werden automatisch alle verwendeten Tags und die zugehörigen Seiten aufgelistet.

[TAGS]
"""),

    # ━━ Asset-Dateien (kein Markdown, aber vom Template referenziert) ━━━━
    ("includes/abbreviations.md", "", """
*[HTML]: Hyper Text Markup Language
*[CSS]: Cascading Style Sheets
*[JS]: JavaScript
*[API]: Application Programming Interface
*[REST]: Representational State Transfer
*[JSON]: JavaScript Object Notation
*[YAML]: YAML Ain't Markup Language
*[CLI]: Command Line Interface
*[GUI]: Graphical User Interface
*[TUI]: Text User Interface
*[CI]: Continuous Integration
*[CD]: Continuous Deployment
*[DSGVO]: Datenschutz-Grundverordnung
*[GDPR]: General Data Protection Regulation
*[SSO]: Single Sign-On
*[JWT]: JSON Web Token
*[OAuth]: Open Authorization
*[SDK]: Software Development Kit
*[SLA]: Service Level Agreement
*[URL]: Uniform Resource Locator
*[SQL]: Structured Query Language
*[ORM]: Object-Relational Mapping
*[TLS]: Transport Layer Security
*[SSL]: Secure Sockets Layer
*[DNS]: Domain Name System
*[CDN]: Content Delivery Network
*[RBAC]: Role-Based Access Control
*[MFA]: Multi-Factor Authentication
*[TOTP]: Time-based One-Time Password
*[CRUD]: Create, Read, Update, Delete
*[EOF]: End of File
*[i18n]: Internationalization
*[l10n]: Localization
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
        if title:
            content = f"# {title}\n{body}"
        else:
            content = body
        file_path.write_text(content.strip() + "\n", encoding="utf-8")
        created.append(file_path)

    # Create stylesheets/extra.css (asset file, not in DEFAULT_SKELETON)
    css_file = docs_dir / "stylesheets" / "extra.css"
    if not css_file.exists():
        css_file.parent.mkdir(parents=True, exist_ok=True)
        css_file.write_text(
            "/* Custom styles for MkDocs Material */\n\n"
            "/* Admonition tweaks */\n"
            ".md-typeset .admonition,\n"
            ".md-typeset details {\n"
            "  border-radius: 4px;\n"
            "}\n\n"
            "/* Table improvements */\n"
            ".md-typeset table:not([class]) th {\n"
            "  min-width: 6rem;\n"
            "}\n",
            encoding="utf-8",
        )
        created.append(css_file)

    # Create javascripts/mathjax.js (for MathJax support)
    mathjax_file = docs_dir / "javascripts" / "mathjax.js"
    if not mathjax_file.exists():
        mathjax_file.parent.mkdir(parents=True, exist_ok=True)
        mathjax_file.write_text(
            "window.MathJax = {\n"
            "  tex: {\n"
            '    inlineMath: [["$", "$"], ["\\\\(", "\\\\)"]],\n'
            '    displayMath: [["$$", "$$"], ["\\\\[", "\\\\]"]],\n'
            "    processEscapes: true,\n"
            "    processEnvironments: true\n"
            "  },\n"
            "  options: {\n"
            '    ignoreHtmlClass: ".*|",\n'
            '    processHtmlClass: "arithmatex"\n'
            "  }\n"
            "};\n",
            encoding="utf-8",
        )
        created.append(mathjax_file)

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


def _walk_tree(base: Path, current: Path, tree: list[tuple[str, int]
    # ━━ Design-System ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ("design/overview.md", "Design-System — Überblick", """
!!! tip "Inhaltsrichtlinie"
    Überblick über das Design-System: Prinzipien, Farben, Typographie, Abstände, Icons.

## Design-Prinzipien

- **Konsistenz**: Gleiche Muster für gleiche Aktionen
- **Einfachheit**: So wenig UI-Elemente wie nötig
- **Barrierefreiheit**: WCAG 2.1 AA als Mindeststandard
- **Responsivität**: Funktioniert auf allen Bildschirmgrößen

## Farben

| Name | Hex | Verwendung |
|------|-----|-----------|
| Primary | TODO | Hauptaktionen, Links |
| Secondary | TODO | Sekundäre Aktionen |
| Success | TODO | Erfolgsmeldungen |
| Warning | TODO | Warnungen |
| Error | TODO | Fehlermeldungen |
| Background | TODO | Hintergrund |
| Text | TODO | Fließtext |

## Typographie

| Stil | Schrift | Größe | Verwendung |
|------|--------|-------|-----------|
| H1 | TODO | 2rem | Seitentitel |
| H2 | TODO | 1.5rem | Abschnitte |
| Body | TODO | 1rem | Fließtext |
| Small | TODO | 0.875rem | Hinweise |
| Code | Monospace | 0.875rem | Code-Blöcke |

## Abstände

TODO: Spacing-System (4px, 8px, 16px, 24px, 32px, 48px, 64px)

## Icons

TODO: Welches Icon-Set? (Material Icons, Heroicons, Lucide, etc.)
"""),

    ("design/components.md", "UI-Komponenten", """
!!! tip "Inhaltsrichtlinie"
    Komponentenbibliothek: Alle wiederverwendbaren UI-Komponenten mit Varianten, Props, Beispielen.

## Buttons

| Variante | Verwendung | Beispiel |
|----------|-----------|---------|
| Primary | Hauptaktion | Speichern, Erstellen |
| Secondary | Nebenaktionen | Abbrechen, Zurück |
| Danger | Destruktive Aktionen | Löschen |
| Ghost | Subtile Aktionen | Links, Icons |

## Formulare

TODO: Input, Select, Checkbox, Radio, Textarea, DatePicker, FilePicker

## Navigation

TODO: Navbar, Sidebar, Breadcrumbs, Tabs, Pagination

## Feedback

TODO: Alert, Toast, Modal, Tooltip, Loading-Spinner, Progress-Bar

## Daten-Darstellung

TODO: Table, Card, List, Badge, Tag, Avatar

## Layout

TODO: Grid, Container, Divider, Spacer

## Komponentenstatus

| Komponente | Status | Dokumentiert | Getestet |
|-----------|--------|-------------|---------|
| Button | Stabil | ✓ | ✓ |
| TODO | TODO | TODO | TODO |
"""),

    ("design/tokens.md", "Design Tokens", """
!!! tip "Inhaltsrichtlinie"
    Design Tokens: Farben, Abstände, Schriften, Schatten, Radien als wiederverwendbare Variablen.

## Was sind Design Tokens?

Design Tokens sind die kleinsten Bausteine des Design-Systems — Werte für
Farben, Abstände, Schriften etc. als Variablen definiert.

## Farb-Tokens

```css
--color-primary: #3b82f6;
--color-primary-hover: #2563eb;
--color-primary-active: #1d4ed8;
--color-text: #1f2937;
--color-text-secondary: #6b7280;
--color-background: #ffffff;
--color-surface: #f9fafb;
--color-border: #e5e7eb;
```

TODO: An tatsächliche Farben anpassen

## Spacing-Tokens

```css
--space-1: 0.25rem;  /* 4px */
--space-2: 0.5rem;   /* 8px */
--space-3: 0.75rem;  /* 12px */
--space-4: 1rem;     /* 16px */
--space-6: 1.5rem;   /* 24px */
--space-8: 2rem;     /* 32px */
```

## Typography-Tokens

TODO: Font-Family, Font-Size, Line-Height, Font-Weight

## Shadow-Tokens

TODO: Box-Shadow-Stufen (sm, md, lg, xl)

## Border-Tokens

TODO: Border-Radius, Border-Width, Border-Color

## Dark-Mode-Tokens

TODO: Overrides für Dark Mode
"""),

    ("design/style-guide.md", "Style Guide", """
!!! tip "Inhaltsrichtlinie"
    Visueller Style Guide: Sprache & Ton, Do's und Don'ts, Textkonventionen, Bildrichtlinien.

## Sprache & Ton

- **Klar**: Fachbegriffe erklären, Abkürzungen vermeiden
- **Freundlich**: Positive Formulierungen bevorzugen
- **Prägnant**: So kurz wie möglich, so lang wie nötig
- **Aktiv**: Aktiv statt Passiv ("Klicken Sie" statt "Es wird geklickt")

## Textkonventionen

| Element | Konvention | Beispiel |
|---------|-----------|---------|
| Button-Texte | Imperativ, kurz | "Speichern", "Löschen" |
| Überschriften | Title Case (DE: Normal) | "Neue Datei erstellen" |
| Fehlermeldungen | Ursache + Lösung | "Datei nicht gefunden. Prüfen Sie den Pfad." |
| Platzhalter | Beispielwert | "max@example.com" |
| Tooltips | Kurze Erklärung | "Datei als PDF exportieren" |

## Do's und Don'ts

### Do's
- Konsistente Terminologie verwenden
- Benutzer mit "Sie" ansprechen
- Fehler verständlich erklären

### Don'ts
- Technischen Jargon in der UI
- Doppelte Verneinungen
- Mehrdeutige Icons ohne Label

## Bilder & Screenshots

TODO: Dateiformate (WebP/PNG), max. Breite, Beschriftung, Alt-Texte

## Animationen

TODO: Dauer (150-300ms), Easing, wann animieren?
"""),

    ("design/accessibility-guidelines.md", "Accessibility-Richtlinien", """
!!! tip "Inhaltsrichtlinie"
    WCAG-Konformität: Farbkontraste, Tastatur-Navigation, ARIA, Screen-Reader, automatische Tests.

## WCAG 2.1 Level AA Anforderungen

### Wahrnehmbar

- **Farbkontrast**: Min. 4.5:1 für Text, 3:1 für große Schrift
- **Nicht nur Farbe**: Information nicht ausschließlich über Farbe vermitteln
- **Alt-Texte**: Alle Bilder mit beschreibendem Alt-Text
- **Untertitel**: Videos mit Untertiteln (falls zutreffend)

### Bedienbar

- **Tastatur**: Alle Funktionen per Tastatur erreichbar
- **Tab-Reihenfolge**: Logische Navigation mit Tab
- **Focus-Indicator**: Sichtbarer Fokus-Ring
- **Skip-Links**: "Zum Inhalt springen"-Link

### Verständlich

- **Sprache**: `lang`-Attribut gesetzt
- **Konsistenz**: Gleiche Navigation auf allen Seiten
- **Fehlervermeidung**: Validierung vor Absenden

### Robust

- **Semantisches HTML**: Korrekte Überschriften-Hierarchie, Landmarks
- **ARIA**: ARIA-Labels wo nötig, `role`-Attribute

## ARIA-Verwendung

| Widget | ARIA-Attribute | Beispiel |
|--------|---------------|---------|
| Modal | `role="dialog"`, `aria-modal="true"` | Bestätigungsdialog |
| Tab | `role="tablist"`, `role="tab"` | Tab-Navigation |
| Alert | `role="alert"` | Fehlermeldung |

## Automatische Tests

TODO: axe-core, Lighthouse Accessibility, pa11y

## Manuelle Tests

TODO: Screen-Reader-Test, Tastatur-Test, Zoom-Test (200%)
"""),

    ("design/responsive.md", "Responsive Design", """
!!! tip "Inhaltsrichtlinie"
    Responsives Layout: Breakpoints, Mobile-First, Grid-System, Touch-Targets.

## Breakpoints

| Name | Breite | Gerätetyp |
|------|--------|----------|
| xs | < 576px | Smartphone (Portrait) |
| sm | ≥ 576px | Smartphone (Landscape) |
| md | ≥ 768px | Tablet |
| lg | ≥ 992px | Desktop |
| xl | ≥ 1200px | Großer Desktop |
| xxl | ≥ 1400px | Ultrawide |

## Mobile-First-Prinzip

TODO: Basis-Layout für Mobile, erweitert per Media Query

## Grid-System

TODO: CSS Grid / Flexbox, Spalten, Abstände

## Touch-Targets

- Mindestgröße: 44x44px (Apple) / 48x48px (Material Design)
- Mindestabstand zwischen Targets: 8px

## Navigation auf verschiedenen Geräten

| Gerät | Navigation |
|-------|-----------|
| Desktop | Sidebar + Top-Bar |
| Tablet | Einklappbare Sidebar |
| Mobile | Hamburger-Menü / Bottom-Navigation |

## Bilder & Medien

TODO: Responsive Images (`srcset`, `picture`), Lazy Loading

## Testing

TODO: Wie auf verschiedenen Geräten testen? (DevTools, reale Geräte)
"""),


    ("design/animations.md", "Animationen & Übergänge", """
!!! tip "Inhaltsrichtlinie"
    Animations-Richtlinien: Dauer, Easing, Zweck, Performance, Reduced Motion.

## Grundprinzipien

- **Funktional**: Animationen verdeutlichen Übergänge, keine reine Dekoration
- **Schnell**: Maximal 300ms für UI-Feedback
- **Konsistent**: Gleiche Aktionen → gleiche Animationen

## Standard-Timings

| Aktion | Dauer | Easing |
|--------|-------|--------|
| Hover-Feedback | 150ms | ease-out |
| Modal öffnen | 200ms | ease-out |
| Modal schließen | 150ms | ease-in |
| Seitenwechsel | 250ms | ease-in-out |
| Toast erscheinen | 200ms | ease-out |
| Toast verschwinden | 300ms | ease-in |

## Easing-Funktionen

```css
--ease-in: cubic-bezier(0.4, 0, 1, 0.7);
--ease-out: cubic-bezier(0, 0.3, 0.6, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
```

## Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Performance

TODO: CSS-Transitions bevorzugen, `transform` und `opacity` animieren, `will-change` sparsam
"""),

    ("design/iconography.md", "Icons & Symbole", """
!!! tip "Inhaltsrichtlinie"
    Icon-System: Bibliothek, Größen, Farben, Konventionen, eigene Icons.

## Icon-Bibliothek

TODO: Material Icons, Heroicons, Lucide, Phosphor, etc.

## Größen

| Größe | Pixel | Verwendung |
|-------|-------|-----------|
| xs | 12px | Inline-Hinweise |
| sm | 16px | Buttons, Inputs |
| md | 20px | Navigation, Listen |
| lg | 24px | Überschriften |
| xl | 32px | Feature-Icons |
| 2xl | 48px | Illustrationen |

## Farben

- **Primär**: Interaktive Icons (Buttons, Links)
- **Sekundär**: Dekorative Icons (Labels, Badges)
- **Muted**: Weniger wichtige Icons
- **Danger**: Destruktive Aktionen
- **Keine Farbe allein**: Icons nie als einziges Unterscheidungsmerkmal

## Konventionen

| Aktion | Icon | Beschreibung |
|--------|------|-------------|
| Erstellen | + (Plus) | Neuen Eintrag erstellen |
| Bearbeiten | Stift | Eintrag bearbeiten |
| Löschen | Mülleimer | Eintrag löschen |
| Suchen | Lupe | Suche öffnen |
| Einstellungen | Zahnrad | Einstellungen öffnen |
| Schließen | X | Dialog/Panel schließen |

## Accessibility

- Dekorative Icons: `aria-hidden="true"`
- Funktionale Icons: `aria-label="Beschreibung"`
"""),

    ("design/dark-mode.md", "Dark Mode", """
!!! tip "Inhaltsrichtlinie"
    Dark-Mode-Design: Farbpalette, Kontraste, Bilder, Umschaltung, System-Präferenz.

## Farbpalette Dark Mode

| Token | Light | Dark |
|-------|-------|------|
| Background | #ffffff | #1a1a2e |
| Surface | #f9fafb | #16213e |
| Text Primary | #1f2937 | #e2e8f0 |
| Text Secondary | #6b7280 | #94a3b8 |
| Border | #e5e7eb | #334155 |
| Primary | #3b82f6 | #60a5fa |

TODO: An tatsächliche Farben anpassen

## Kontraste

- Text auf Background: mindestens 4.5:1 (auch im Dark Mode!)
- Alle Farben mit Contrast-Checker verifizieren

## Bilder im Dark Mode

TODO: Dunklere Bilder, reduzierte Helligkeit, Schatten statt Ränder

## Umschaltung

| Modus | Beschreibung |
|-------|-------------|
| System | Folgt der Betriebssystem-Einstellung |
| Hell | Immer Light Mode |
| Dunkel | Immer Dark Mode |

```css
@media (prefers-color-scheme: dark) {
  :root { /* Dark-Mode-Tokens */ }
}
```

## Verweis

- [Design Tokens](tokens.md)
"""),

    ("design/forms.md", "Formular-Design", """
!!! tip "Inhaltsrichtlinie"
    Formular-Patterns: Layout, Validierung, Fehlermeldungen, Barrierefreiheit, Multi-Step.

## Layout

- **Einspaltiges Layout** bevorzugen (bessere Lesbarkeit)
- **Labels über dem Feld** (nicht daneben)
- **Logische Gruppierung** zusammengehöriger Felder
- **Pflichtfelder** markieren (Stern * oder "Pflicht"-Label)

## Validierung

### Wann validieren?

| Zeitpunkt | Verwendung |
|-----------|-----------|
| On Submit | Standard — alle Fehler auf einmal |
| On Blur | Für komplexe Felder (E-Mail, Passwort) |
| On Input | Nur für Echtzeit-Feedback (Passwort-Stärke) |

### Fehlermeldungen

```
✗ Bitte geben Sie eine gültige E-Mail-Adresse ein.
✗ Das Passwort muss mindestens 8 Zeichen lang sein.
```

**Regeln:**
- Unter dem betroffenen Feld anzeigen
- Rot markieren (+ Icon, nicht nur Farbe)
- Sagen was falsch ist UND was erwartet wird
- `aria-describedby` für Screen-Reader

## Multi-Step-Formulare

TODO: Wizard-Pattern, Fortschrittsanzeige, Vor/Zurück, Zwischenspeichern

## Verweis

- [UI-Komponenten](components.md)
- [Accessibility-Richtlinien](accessibility-guidelines.md)
"""),

    # ━━ Testdokumentation ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ("testing/overview.md", "Testdokumentation — Überblick", """
!!! tip "Inhaltsrichtlinie"
    Überblick über die Test-Strategie: Welche Tests existieren, wie werden sie ausgeführt, wo liegen sie.

## Test-Übersicht

| Typ | Anzahl | Coverage | Dauer | Frequenz |
|-----|--------|---------|-------|---------|
| Unit | TODO | TODO% | TODO | Jeder Commit |
| Integration | TODO | - | TODO | Jeder PR |
| E2E | TODO | - | TODO | Nightly |
| Performance | TODO | - | TODO | Wöchentlich |
| Security | TODO | - | TODO | Wöchentlich |

## Tests ausführen

```bash
# Alle Tests
pytest

# Nur Unit-Tests
pytest tests/unit/

# Mit Coverage
pytest --cov=src --cov-report=html
```

## Verzeichnisstruktur

```
tests/
  unit/           ← Schnelle, isolierte Tests
  integration/    ← Komponentenübergreifende Tests
  e2e/            ← End-to-End Workflow-Tests
  fixtures/       ← Gemeinsame Testdaten
  conftest.py     ← Shared Fixtures
```

## Verweis

- [Test-Architektur](../architecture/testing-architecture.md)
- [CI/CD-Pipeline](../development/ci-cd.md)
"""),

    ("testing/test-plan.md", "Testplan", """
!!! tip "Inhaltsrichtlinie"
    Formaler Testplan: Testziele, Scope, Risiken, Umgebung, Zeitplan, Kriterien.

## Testziele

TODO: Was soll durch Tests sichergestellt werden?

## Scope

### In Scope

TODO: Welche Funktionen werden getestet?

### Out of Scope

TODO: Was wird NICHT getestet? (z.B. externe Abhängigkeiten)

## Test-Umgebung

| Umgebung | Zweck | Datenbank | URL |
|----------|-------|----------|-----|
| Lokal | Entwicklung | SQLite | localhost |
| CI | Automatisiert | PostgreSQL | - |
| Staging | Manuell | PostgreSQL | TODO |

## Risiken

| Risiko | Wahrscheinlichkeit | Gegenmaßnahme |
|--------|-------------------|--------------|
| Instabile Tests | TODO | TODO |
| Langsame Pipeline | TODO | TODO |

## Abnahmekriterien

- [ ] Alle Tests bestehen
- [ ] Coverage ≥ TODO%
- [ ] Keine kritischen Sicherheitslücken
- [ ] Performance-Schwellwerte eingehalten
"""),

    ("testing/test-cases.md", "Testfälle", """
!!! tip "Inhaltsrichtlinie"
    Katalog wichtiger Testfälle: ID, Beschreibung, Vorbedingung, Schritte, erwartetes Ergebnis.

## Testfall-Format

| Feld | Beschreibung |
|------|-------------|
| **ID** | Eindeutige Kennung (TC-XXX) |
| **Titel** | Kurzbeschreibung |
| **Vorbedingung** | Was muss gegeben sein? |
| **Schritte** | Durchzuführende Aktionen |
| **Erwartetes Ergebnis** | Was soll passieren? |
| **Priorität** | Hoch / Mittel / Niedrig |

## Authentifizierung

### TC-001: Erfolgreicher Login

- **Vorbedingung**: Gültiger Benutzer existiert
- **Schritte**: 1. Login-Seite öffnen, 2. Credentials eingeben, 3. Absenden
- **Erwartet**: Dashboard wird angezeigt, Session erstellt
- **Priorität**: Hoch

### TC-002: Login mit falschen Credentials

- **Vorbedingung**: -
- **Schritte**: 1. Login-Seite, 2. Falsche Credentials, 3. Absenden
- **Erwartet**: Fehlermeldung, kein Zugang
- **Priorität**: Hoch

TODO: Weitere Testfälle nach diesem Schema

## CRUD-Operationen

TODO: Testfälle für Erstellen, Lesen, Aktualisieren, Löschen

## Edge Cases

TODO: Grenzwerte, leere Eingaben, Sonderzeichen, große Datenmengen
"""),

    ("testing/test-automation.md", "Testautomatisierung", """
!!! tip "Inhaltsrichtlinie"
    Automatisierte Tests: Framework, Konfiguration, Fixtures, Mocking, CI-Integration.

## Framework

TODO: pytest, Jest, JUnit — Version, Konfiguration

## Konfiguration

```ini
# pytest.ini / pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"
markers = [
    "slow: Langsame Tests",
    "integration: Integrationstests",
    "e2e: End-to-End Tests",
]
```

## Fixtures

TODO: Gemeinsame Fixtures, Factory-Pattern, Datenbank-Fixtures

## Mocking

TODO: Mocking-Bibliothek, Mocking-Strategien, Wann mocken?

## Test-Daten

TODO: Faker, Factories, Seed-Daten, Snapshots

## Parallelisierung

TODO: Tests parallel ausführen (pytest-xdist, jest --workers)

## CI-Integration

TODO: Tests in Pipeline, Coverage-Upload, Artefakte
"""),

    ("testing/performance-tests.md", "Performance-Testberichte", """
!!! tip "Inhaltsrichtlinie"
    Ergebnisse von Performance-Tests: Baseline, aktuelle Werte, Trends, Optimierungsvorschläge.

## Baseline

| Endpunkt | P50 | P95 | P99 | RPS |
|----------|-----|-----|-----|-----|
| GET /api/v1/health | TODO | TODO | TODO | TODO |
| GET /api/v1/resources | TODO | TODO | TODO | TODO |
| POST /api/v1/resources | TODO | TODO | TODO | TODO |

## Aktuelle Messung

TODO: Datum, Umgebung, Last-Profil, Ergebnisse

## Trends

TODO: Diagramm oder Tabelle — Performance über letzte N Releases

## Identifizierte Engpässe

TODO: Langsame Queries, Speicherverbrauch, CPU-Spitzen

## Verweis

- [Performance-Tests (Entwicklung)](../development/performance-testing.md)
- [Performance-Tuning (Betrieb)](../operations/performance.md)
"""),

    ("testing/security-tests.md", "Sicherheitstest-Berichte", """
!!! tip "Inhaltsrichtlinie"
    Ergebnisse von Sicherheitstests: SAST/DAST-Ergebnisse, offene Findings, Risikobewertung.

## Letzter Scan

- **Datum**: TODO
- **Tool**: TODO (Bandit, SonarQube, OWASP ZAP)
- **Scope**: TODO

## Ergebnisse

| Schweregrad | Anzahl | Behoben | Offen |
|------------|--------|---------|-------|
| Kritisch | TODO | TODO | TODO |
| Hoch | TODO | TODO | TODO |
| Mittel | TODO | TODO | TODO |
| Niedrig | TODO | TODO | TODO |

## Offene Findings

TODO: Liste der offenen Sicherheitsbefunde mit Risikobewertung

## Dependency-Scan

TODO: Bekannte CVEs in Abhängigkeiten

## Verweis

- [Sicherheitstests (Entwicklung)](../development/security-testing.md)
- [Sicherheitsrichtlinien](../compliance/security-policies.md)
"""),

    ("testing/acceptance-tests.md", "Abnahmetests", """
!!! tip "Inhaltsrichtlinie"
    Abnahmetests für Releases: Kriterien, Checkliste, Ergebnisse, Freigabe.

## Abnahmekriterien

| Kriterium | Schwellwert | Status |
|----------|-----------|--------|
| Alle Unit-Tests bestehen | 100% | TODO |
| Integration-Tests bestehen | 100% | TODO |
| Coverage | ≥ TODO% | TODO |
| Keine kritischen Bugs | 0 | TODO |
| Performance P95 | < TODO ms | TODO |
| Security Scan | Keine kritischen Findings | TODO |

## Manuelle Prüfungen

- [ ] Alle Hauptfunktionen in Staging getestet
- [ ] Cross-Browser-Test durchgeführt
- [ ] Mobile-Test durchgeführt
- [ ] Accessibility-Test durchgeführt
- [ ] Dokumentation aktualisiert

## Freigabe

- **Getestet von**: TODO
- **Datum**: TODO
- **Version**: TODO
- **Ergebnis**: Freigegeben / Nicht freigegeben

## Verweis

- [Release-Prozess](../development/release.md)
- [Testplan](test-plan.md)
"""),


    ("testing/regression-tests.md", "Regressionstests", """
!!! tip "Inhaltsrichtlinie"
    Regressionstests: Strategie, Testauswahl, Automatisierung, Triage von Regressionen.

## Strategie

TODO: Wann werden Regressionstests ausgeführt? (Nightly, vor Release, nach Merge)

## Test-Suite

| Suite | Anzahl Tests | Dauer | Scope |
|-------|-------------|-------|-------|
| Smoke | TODO | < 5 Min | Kritische Pfade |
| Regression (klein) | TODO | < 30 Min | Letzte 3 Releases |
| Regression (voll) | TODO | < 2 Std | Alle Features |

## Triage bei Regression

1. Test fehlgeschlagen — Bug oder Testfehler?
2. Seit welchem Commit? (`git bisect`)
3. Kritikalität bewerten
4. Fix oder Revert

## Testauswahl

TODO: Risiko-basierte Auswahl, Changed-Code-basiert, Impact Analysis

## Verweis

- [CI/CD-Pipeline](../development/ci-cd.md)
- [Testplan](test-plan.md)
"""),

    ("testing/compatibility-tests.md", "Kompatibilitätstests", """
!!! tip "Inhaltsrichtlinie"
    Browser-, Plattform-, Versions-Kompatibilität: Testmatrix, Tools, Automatisierung.

## Browser-Testmatrix

| Browser | Version | Desktop | Mobile | Status |
|---------|---------|---------|--------|--------|
| Chrome | Letzte 2 | TODO | TODO | TODO |
| Firefox | Letzte 2 | TODO | TODO | TODO |
| Safari | Letzte 2 | TODO | TODO | TODO |
| Edge | Letzte 2 | TODO | TODO | TODO |

## Plattform-Testmatrix

| OS | Version | Status |
|-----|---------|--------|
| Ubuntu | 22.04 | TODO |
| macOS | 14 | TODO |
| Windows | 11 | TODO |

## Automatisierung

TODO: Selenium Grid, BrowserStack, Sauce Labs, Playwright

## Testfälle

TODO: Welche Funktionen werden browser-/plattform-übergreifend getestet?

## Verweis

- [Plattform-Unterstützung](../reference/supported-platforms.md)
"""),

    ("testing/accessibility-tests.md", "Accessibility-Tests", """
!!! tip "Inhaltsrichtlinie"
    Accessibility-Tests: Automatisierte Tools, manuelle Prüfung, Screen-Reader-Tests.

## Automatisierte Tests

### axe-core (CI)

```bash
npx @axe-core/cli http://localhost:8000
```

### Lighthouse (CI)

```bash
npx lighthouse http://localhost:8000 --only-categories=accessibility --output=json
```

### pa11y (CI)

```bash
npx pa11y http://localhost:8000
```

## Manuelle Tests

### Tastatur-Test

- [ ] Alle interaktiven Elemente erreichbar mit Tab
- [ ] Fokus-Reihenfolge logisch
- [ ] Focus-Indicator sichtbar
- [ ] Dialoge per Escape schließbar

### Screen-Reader-Test

| Screen-Reader | Browser | Status |
|-------------|---------|--------|
| NVDA | Firefox | TODO |
| VoiceOver | Safari | TODO |
| JAWS | Chrome | TODO |

### Zoom-Test

- [ ] 200% Zoom — Layout bricht nicht
- [ ] 400% Zoom — Inhalte weiterhin nutzbar

## Ergebnisse

TODO: Verweis auf letzte Testergebnisse

## Verweis

- [Accessibility-Richtlinien (Design)](../design/accessibility-guidelines.md)
- [Barrierefreiheit-Compliance](../compliance/accessibility-compliance.md)
"""),

    ("testing/test-data.md", "Testdaten-Management", """
!!! tip "Inhaltsrichtlinie"
    Testdaten erstellen, verwalten, anonymisieren: Factories, Fixtures, Faker, Snapshots.

## Testdaten-Strategien

| Strategie | Beschreibung | Einsatz |
|----------|-------------|---------|
| Fixtures | Statische Testdaten | Einfache, vorhersagbare Tests |
| Factories | Dynamisch generierte Daten | Flexible, variantenreiche Tests |
| Faker | Realistische Zufallsdaten | Massentests, Edge Cases |
| Snapshots | Kopie von Produktionsdaten | Integrations-/E2E-Tests |

## Factory-Pattern

```python
# TODO: An tatsächliches Framework anpassen
class UserFactory:
    @staticmethod
    def create(**kwargs):
        defaults = {
            "name": faker.name(),
            "email": faker.email(),
            "role": "viewer",
        }
        defaults.update(kwargs)
        return User.create(**defaults)
```

## Anonymisierung von Produktionsdaten

TODO: PII entfernen, E-Mails/Namen ersetzen, IDs beibehalten, Relationen intakt halten

## Seed-Daten

```bash
# TODO: Befehl zum Laden von Seed-Daten
```

## Regeln

1. **Keine echten Daten** in Tests oder Repositories
2. **Deterministische Tests** — gleiche Eingabe → gleiches Ergebnis
3. **Aufräumen** — Testdaten nach dem Test löschen
"""),

    # ━━ Projektmanagement ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ("project/overview.md", "Projektmanagement — Überblick", """
!!! tip "Inhaltsrichtlinie"
    Projektorganisation: Methodik, Team, Kommunikation, Tools, Zeitplanung.

## Projektmethodik

TODO: Scrum, Kanban, SAFe, Wasserfall?

## Team

| Rolle | Verantwortung | Person |
|-------|-------------|--------|
| Product Owner | Anforderungen, Priorisierung | TODO |
| Tech Lead | Architektur, Code-Qualität | TODO |
| Entwickler | Implementierung | TODO |
| QA | Testing, Qualitätssicherung | TODO |
| DevOps | Infrastruktur, CI/CD | TODO |

## Kommunikation

| Kanal | Zweck | Frequenz |
|-------|-------|---------|
| Daily Standup | Status, Blocker | Täglich |
| Sprint Planning | Sprintplanung | Alle 2 Wochen |
| Retro | Verbesserung | Alle 2 Wochen |
| Slack/Teams | Schnelle Fragen | Laufend |

## Tools

TODO: Jira, GitHub Projects, Linear, Notion?

## Verweis

- [Roadmap](roadmap.md)
- [Stakeholder](stakeholders.md)
"""),

    ("project/roadmap.md", "Roadmap", """
!!! tip "Inhaltsrichtlinie"
    Produkt-Roadmap: Geplante Features, Meilensteine, Zeitplanung, Prioritäten.

## Aktuelle Phase

TODO: In welcher Phase befindet sich das Projekt?

## Meilensteine

| Meilenstein | Zieldatum | Status | Beschreibung |
|------------|----------|--------|-------------|
| MVP | TODO | TODO | Minimales lauffähiges Produkt |
| v1.0 | TODO | TODO | Erster stabiler Release |
| v2.0 | TODO | TODO | Nächstes Major-Release |

## Q1 TODO

- [ ] Feature A
- [ ] Feature B
- [ ] Verbesserung C

## Q2 TODO

- [ ] Feature D
- [ ] Feature E

## Backlog (ungeplant)

TODO: Features die gewünscht aber nicht terminiert sind

## Entscheidungslog

TODO: Verweis auf [ADR](../architecture/decisions.md)
"""),

    ("project/stakeholders.md", "Stakeholder", """
!!! tip "Inhaltsrichtlinie"
    Stakeholder-Übersicht: Wer hat Interesse am Projekt? Erwartungen, Kommunikation.

## Stakeholder-Matrix

| Stakeholder | Typ | Interesse | Einfluss | Kommunikation |
|------------|-----|----------|---------|--------------|
| Endanwender | Nutzer | Hoch | Mittel | Release Notes, Docs |
| Management | Sponsor | Mittel | Hoch | Status-Reports |
| Entwickler | Team | Hoch | Hoch | Daily, Slack |
| Support | Intern | Hoch | Niedrig | Ticket-System |
| Partner | Extern | Mittel | Niedrig | Newsletter |

## Erwartungen

### Endanwender
TODO: Was erwarten die Benutzer?

### Management
TODO: KPIs, Budget, Timeline

### Entwickler
TODO: Technische Qualität, DX

## Feedback-Kanäle

TODO: Wie können Stakeholder Feedback geben?
"""),

    ("project/risks.md", "Risiken & Maßnahmen", """
!!! tip "Inhaltsrichtlinie"
    Risikoregister: Identifizierte Risiken, Bewertung, Gegenmaßnahmen, Verantwortliche.

## Risikoregister

| # | Risiko | Wahrscheinl. | Auswirkung | Risikostufe | Maßnahme | Verantwortlich |
|---|--------|-------------|-----------|------------|----------|---------------|
| R1 | Personalausfall | Mittel | Hoch | Hoch | Cross-Training, Dokumentation | TODO |
| R2 | Technische Schuld | Hoch | Mittel | Hoch | Refactoring-Sprints | TODO |
| R3 | Scope Creep | Hoch | Mittel | Hoch | Klare Anforderungen, Sprint Goals | TODO |
| R4 | Sicherheitsvorfall | Niedrig | Hoch | Mittel | Security-Tests, Audits | TODO |
| R5 | Abhängigkeit von Drittanbieter | Mittel | Mittel | Mittel | Abstraktion, Exit-Strategie | TODO |

TODO: An tatsächliche Projektrisiken anpassen

## Risikobewertung

| | Niedrige Auswirkung | Mittlere Auswirkung | Hohe Auswirkung |
|---|---|---|---|
| **Hoch** | Mittel | Hoch | Kritisch |
| **Mittel** | Niedrig | Mittel | Hoch |
| **Niedrig** | Niedrig | Niedrig | Mittel |

## Überprüfung

TODO: Wie oft wird das Risikoregister überprüft?
"""),

    ("project/meetings.md", "Meeting-Protokolle & Vorlagen", """
!!! tip "Inhaltsrichtlinie"
    Vorlagen für wiederkehrende Meetings: Agenda, Protokoll-Format, Aktionspunkte.

## Daily Standup

| Frage | Antwort |
|-------|---------|
| Was habe ich gestern gemacht? | TODO |
| Was mache ich heute? | TODO |
| Gibt es Blocker? | TODO |

Dauer: 15 Minuten, täglich

## Sprint Planning

### Agenda

1. Review der Sprint-Ziele
2. Backlog-Refinement
3. Kapazitätsplanung
4. Task-Zuordnung

### Protokoll-Vorlage

- **Sprint**: #TODO
- **Zeitraum**: TODO – TODO
- **Kapazität**: TODO Story Points
- **Sprint-Ziel**: TODO
- **Ausgewählte Stories**: TODO

## Retrospektive

### Format

1. **Was lief gut?** (Keep)
2. **Was lief schlecht?** (Stop)
3. **Was können wir verbessern?** (Start)

### Aktionspunkte

| Aktion | Verantwortlich | Frist |
|--------|---------------|-------|
| TODO | TODO | TODO |

## Architektur-Review

### Agenda

1. Architektur-Entscheidungen besprechen
2. Technische Schuld bewerten
3. ADRs erstellen/aktualisieren

TODO: Verweis auf [Entscheidungslog](../architecture/decisions.md)
"""),

], depth: int) -> None:
    """Recursively walk directory and build tree display."""
    entries = sorted(current.iterdir(), key=lambda p: (not p.is_dir(), p.name))
    for entry in entries:
        if entry.is_dir():
            tree.append((f"{entry.name}/", depth))
            _walk_tree(base, entry, tree, depth + 1)
        elif entry.suffix == ".md":
            tree.append((entry.name, depth))
