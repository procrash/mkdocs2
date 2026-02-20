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
    **Zielgruppe:** Erstnutzer, die das Produkt zum ersten Mal installieren wollen; Admins, die es in bestehende Infrastruktur einbetten.

    **Pflicht-Abschnitte:**

    - Voraussetzungen (Verweis auf requirements.md für Details)
    - Installation per Paketmanager (pip, apt, brew, choco — je ein Tab)
    - Installation per Docker (docker run / docker-compose Minimalbeispiel)
    - Installation aus Quellcode (git clone + pip install -e .)
    - Verifikation der Installation (Kommando + erwartete Ausgabe)
    - Häufige Installationsprobleme und Lösungen (Tabelle)
    - Nächste Schritte (Link → quickstart.md)

    **Inhaltliche Tiefe:** Schritt-für-Schritt mit exakten Kommandos in Code-Blöcken. Jede Plattform (Linux, macOS, Windows) als eigener Tab. Versionsnummern als Platzhalter `X.Y.Z`.

    **Abgrenzung:** Keine Konfigurationsdetails (→ user-guide/configuration.md). Kein Upgrade bestehender Installationen (→ getting-started/upgrade.md).

    **Beispiel-Inhalte:** `pip install projektname`, `docker run -d -p 8080:8080 projektname:latest`, Ausgabe von `projektname --version`.

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
    **Zielgruppe:** Ungeduldige Nutzer, die in unter 5 Minuten ein laufendes System sehen wollen.

    **Pflicht-Abschnitte:**

    - TL;DR-Box (3–5 Kommandos, die sofort funktionieren)
    - Schritt 1: Installieren (Einzeiler, Verweis → installation.md)
    - Schritt 2: Projekt initialisieren
    - Schritt 3: Konfiguration anpassen (nur das Nötigste)
    - Schritt 4: Starten und Ergebnis prüfen
    - Was kommt als Nächstes? (Links zu hello-world.md, user-guide/basic-usage.md)

    **Inhaltliche Tiefe:** Maximal eine DIN-A4-Seite. Jeder Schritt hat genau einen Code-Block und einen Satz Erklärung. Keine Optionen, keine Varianten — nur der glückliche Pfad.

    **Abgrenzung:** Keine Erklärung von Konzepten (→ concepts.md). Keine alternativen Installationswege (→ installation.md). Keine fortgeschrittenen Optionen.

    **Beispiel-Inhalte:** `projektname init mein-projekt && cd mein-projekt && projektname serve` — Screenshot oder ASCII-Ausgabe des laufenden Systems.

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
    **Zielgruppe:** Admins und Entwickler, die vor der Installation prüfen müssen, ob ihre Umgebung kompatibel ist.

    **Pflicht-Abschnitte:**

    - Unterstützte Betriebssysteme (Tabelle: OS, Version, Architektur, Support-Status)
    - Hardware-Mindestanforderungen (CPU, RAM, Festplatte — Minimum vs. Empfohlen)
    - Software-Abhängigkeiten (Python-Version, Node.js, Docker, etc.)
    - Netzwerk-Anforderungen (Ports, Firewall-Regeln, DNS)
    - Optionale Abhängigkeiten (für bestimmte Features)
    - Kompatibilitätsmatrix (Version × OS × Architektur)

    **Inhaltliche Tiefe:** Tabellarisch, präzise Versionsnummern. Unterscheidung Minimum / Empfohlen / Optimal. Automatischer Check-Befehl, falls vorhanden.

    **Abgrenzung:** Keine Installationsanleitung (→ installation.md). Keine Konfiguration (→ user-guide/configuration.md).

    **Beispiel-Inhalte:** Tabelle mit Spalten OS | Min. Version | Python | RAM | Disk. Kommando `projektname doctor` zur Prüfung.

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
    **Zielgruppe:** Bestandsnutzer, die von Version N auf N+1 aktualisieren.

    **Pflicht-Abschnitte:**

    - Vor dem Upgrade: Backup erstellen (Verweis → user-guide/backup-restore.md)
    - Upgrade-Pfad-Matrix (von Version → zu Version, direkt oder stufenweise)
    - Upgrade per Paketmanager (pip install --upgrade, etc.)
    - Upgrade per Docker (Image-Tag ändern, Container neu starten)
    - Datenbank-Migrationen (falls nötig, automatisch vs. manuell)
    - Nach dem Upgrade: Verifikation und Rollback-Anleitung
    - Breaking Changes Checkliste (je Major-Version)

    **Inhaltliche Tiefe:** Konkrete Kommandos für jeden Upgrade-Pfad. Warnboxen (admonitions) für Breaking Changes. Rollback-Schritte explizit dokumentieren.

    **Abgrenzung:** Keine Neuinstallation (→ installation.md). Keine Migration von Fremdprodukten (→ migration.md).

    **Beispiel-Inhalte:** `pip install --upgrade projektname==X.Y.Z`, `docker pull projektname:X.Y.Z`, Migrationsskript `projektname migrate`.

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
    **Zielgruppe:** Nutzer, die von einem Konkurrenzprodukt oder einer älteren Architektur umsteigen.

    **Pflicht-Abschnitte:**

    - Unterstützte Quellsysteme (Tabelle: Produkt, Version, Migrationsgrad)
    - Vorbereitungen (Daten-Export aus Altsystem)
    - Automatische Migration (Import-Tool, Kommandos, erwartete Laufzeit)
    - Manuelle Nacharbeiten (was nicht automatisch migriert wird)
    - Datenvalidierung nach Migration
    - Parallelbetrieb und schrittweise Umstellung
    - Bekannte Einschränkungen

    **Inhaltliche Tiefe:** Pro Quellsystem ein eigener Unterabschnitt. Mapping-Tabellen (Altes Konzept → Neues Konzept). Geschätzte Zeitangaben.

    **Abgrenzung:** Kein Versions-Upgrade innerhalb des eigenen Produkts (→ upgrade.md). Keine Neuinstallation (→ installation.md).

    **Beispiel-Inhalte:** `projektname migrate --from=altprodukt --source=/pfad/zum/export`, Mapping-Tabelle Felder alt → neu.

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
    **Zielgruppe:** Alle neuen Nutzer, die das mentale Modell des Produkts verstehen wollen, bevor sie loslegen.

    **Pflicht-Abschnitte:**

    - Architektur-Überblick (vereinfachtes Diagramm, max. 6 Komponenten)
    - Kernbegriffe-Glossar (Tabelle: Begriff, Definition, Analogie)
    - Datenmodell (Entitäten und ihre Beziehungen, ER-Diagramm)
    - Lebenszyklus eines typischen Objekts (Erstellen → Bearbeiten → Archivieren)
    - Berechtigungsmodell (Kurzüberblick, Verweis → user-guide/permissions.md)
    - Erweiterbarkeit (Plugins, Templates, API — nur Überblick)

    **Inhaltliche Tiefe:** Erklärend, nicht prozedural. Analogien zur realen Welt. Diagramme als Mermaid-Code. Maximal 1 Absatz pro Begriff.

    **Abgrenzung:** Keine Schritt-für-Schritt-Anleitungen (→ quickstart.md, tutorials/). Keine vollständige API-Referenz (→ developer-guide/).

    **Beispiel-Inhalte:** Mermaid-Diagramm der Architektur, Glossar-Tabelle mit 10–15 Kernbegriffen, Lebenszyklus-Diagramm.

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
    **Zielgruppe:** Absolute Anfänger, die das kleinstmögliche funktionsfähige Beispiel sehen wollen.

    **Pflicht-Abschnitte:**

    - Ziel des Beispiels (1 Satz: was wird gebaut)
    - Voraussetzungen (installiertes Produkt, sonst nichts)
    - Der komplette Code / die komplette Konfiguration (ein einziger Block)
    - Zeile-für-Zeile-Erklärung
    - Ausführen und Ergebnis betrachten (Kommando + erwartete Ausgabe)
    - Variationen zum Experimentieren (2–3 kleine Änderungen)

    **Inhaltliche Tiefe:** So kurz wie möglich — idealerweise unter 20 Zeilen Code/Konfiguration. Jede Zeile wird erklärt. Kein externes Setup nötig.

    **Abgrenzung:** Keine Produktionsreife (→ tutorials/expert-production.md). Keine Erklärung der Architektur (→ concepts.md).

    **Beispiel-Inhalte:** Minimale Konfigurationsdatei, ein `projektname run` Kommando, erwartete Konsolenausgabe.

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
    **Zielgruppe:** Einsteiger mit typischen Anfängerfragen und Stolpersteinen.

    **Pflicht-Abschnitte:**

    - Installation & Setup (5–8 Fragen)
    - Erste Schritte (5–8 Fragen)
    - Häufige Fehlermeldungen (Tabelle: Fehler → Ursache → Lösung)
    - Begriffe und Konzepte (3–5 Fragen, Verweis → concepts.md)
    - Wo finde ich Hilfe? (Community, Doku-Verweise, Support)

    **Inhaltliche Tiefe:** Jede Frage als H3-Überschrift, Antwort max. 3–5 Sätze. Code-Beispiele nur wenn nötig. Querverweise auf ausführlichere Seiten.

    **Abgrenzung:** Keine fortgeschrittenen Fragen (→ separates FAQ oder user-guide/). Keine vollständige Fehlerbehebung (→ operations/troubleshooting.md).

    **Beispiel-Inhalte:** „Warum startet der Server nicht?" → Port belegt, Lösung: `--port 8081`. „Was ist ein Projekt?" → Verweis auf concepts.md.

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
    **Zielgruppe:** Nutzer, die nach der Ersteinrichtung das Handbuch als Nachschlagewerk nutzen.

    **Pflicht-Abschnitte:**

    - Zweck des User Guide (1 Absatz)
    - Kapitelübersicht (Tabelle: Kapitel, Beschreibung, Schwierigkeitsgrad)
    - Empfohlene Lesereihenfolge für verschiedene Rollen (Admin, Endnutzer, Power-User)
    - Schnellnavigation (Icon-Karten oder Link-Grid zu allen Unterseiten)
    - Konventionen in dieser Dokumentation (Admonition-Typen, Code-Konventionen)

    **Inhaltliche Tiefe:** Rein navigatorisch, kein fachlicher Inhalt. Maximal 1–2 Sätze pro verlinktem Kapitel. Visuell ansprechend (Grid-Cards empfohlen).

    **Abgrenzung:** Keine eigenen Anleitungen (→ jeweilige Unterseite). Keine Tutorials (→ tutorials/).

    **Beispiel-Inhalte:** Tabelle mit 14 Zeilen (je eine pro User-Guide-Seite), Rollen-Matrix: Admin liest X, Y, Z zuerst.

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
    **Zielgruppe:** Alle Nutzer, die das System an ihre Bedürfnisse anpassen wollen.

    **Pflicht-Abschnitte:**

    - Konfigurationsdatei-Formate (YAML, TOML, ENV — Prioritätsreihenfolge)
    - Vollständige Optionsreferenz (Tabelle: Schlüssel, Typ, Default, Beschreibung)
    - Umgebungsvariablen (Mapping: YAML-Schlüssel → ENV-Variable)
    - Konfigurationsbeispiele nach Anwendungsfall (Entwicklung, Test, Produktion)
    - Validierung der Konfiguration (Kommando + häufige Fehler)
    - Konfiguration zur Laufzeit ändern (Hot-Reload, falls unterstützt)

    **Inhaltliche Tiefe:** Jede Option einzeln dokumentiert mit Typ, Default, Wertebereich und Beispiel. Zusammengehörige Optionen gruppiert. YAML-Codeblöcke mit Kommentaren.

    **Abgrenzung:** Keine Plugin-spezifische Konfiguration (→ plugins.md). Keine Deployment-Konfiguration (→ operations/deployment.md).

    **Beispiel-Inhalte:** Kommentierte `config.yaml` mit allen Abschnitten, ENV-Mapping-Tabelle, `projektname config validate` Ausgabe.

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
    **Zielgruppe:** Nutzer direkt nach der Installation, die die ersten produktiven Aufgaben erledigen wollen.

    **Pflicht-Abschnitte:**

    - Erstes Projekt erstellen
    - Daten hinzufügen (manuell und Import)
    - Grundlegende Operationen (Anzeigen, Bearbeiten, Löschen)
    - Suchen und Filtern
    - Ergebnisse exportieren
    - Typischer Tagesablauf-Workflow (Zusammenfassung)

    **Inhaltliche Tiefe:** Aufgabenorientiert: „Ich will X tun → So geht's". Jede Aufgabe mit CLI-Kommando UND UI-Weg (falls beides existiert). Screenshots/Ausgaben zeigen.

    **Abgrenzung:** Keine fortgeschrittenen Features (→ advanced-features.md). Keine Installation (→ getting-started/installation.md).

    **Beispiel-Inhalte:** `projektname create --name "Mein Projekt"`, `projektname add datei.csv`, Filterbeispiel `projektname list --filter "status=aktiv"`.

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
    **Zielgruppe:** Erfahrene Nutzer, die über die Grundfunktionen hinausgehen wollen.

    **Pflicht-Abschnitte:**

    - Feature-Übersicht (Tabelle: Feature, Kurzbeschreibung, Voraussetzung)
    - Erweiterte Suche (Regex, Volltextsuche, gespeicherte Abfragen)
    - Batch-Operationen (Massenverarbeitung, Bulk-Import/Export)
    - Workflows und Pipelines (mehrstufige Verarbeitungsketten)
    - Benutzerdefinierte Felder und Metadaten
    - Scheduling und zeitgesteuerte Aktionen
    - Integration mit Drittanbietern (Überblick, Verweis → Integrationsseiten)

    **Inhaltliche Tiefe:** Pro Feature: Was es tut, wann man es braucht, Minimalbeispiel. Tiefergehende Tutorials verlinken (→ tutorials/).

    **Abgrenzung:** Keine Grundfunktionen (→ basic-usage.md). Keine API-Programmierung (→ developer-guide/).

    **Beispiel-Inhalte:** Regex-Suchbeispiel, Batch-Import-Kommando `projektname batch import *.csv`, Workflow-YAML-Definition.

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
    **Zielgruppe:** Administratoren, die Benutzer verwalten und Zugriffsrechte konfigurieren.

    **Pflicht-Abschnitte:**

    - Berechtigungsmodell (Überblick: Rollen, Gruppen, Rechte)
    - Vordefinierte Rollen (Tabelle: Rolle, Rechte, typischer Einsatz)
    - Benutzer anlegen, bearbeiten, deaktivieren
    - Gruppen verwalten
    - Benutzerdefinierte Rollen erstellen
    - Ressourcen-basierte Berechtigungen (Zugriff auf Projekt-/Objektebene)
    - LDAP/SSO-Integration (Überblick, Verweis → operations/authentication.md)
    - Audit-Log für Berechtigungsänderungen

    **Inhaltliche Tiefe:** Detaillierte Rechte-Matrix (Rolle × Aktion). Schritt-für-Schritt für jede Verwaltungsaufgabe. Sicherheitshinweise als Warnboxen.

    **Abgrenzung:** Keine technische SSO-Konfiguration (→ operations/authentication.md). Keine API-Token-Verwaltung (→ developer-guide/api-reference.md).

    **Beispiel-Inhalte:** Rollen-Matrix mit Leser/Bearbeiter/Admin, Kommando `projektname user create --role editor`, Gruppenbeispiel.

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
    **Zielgruppe:** Nutzer, die das System durch Plugins erweitern wollen, und Admins, die Plugins verwalten.

    **Pflicht-Abschnitte:**

    - Plugin-Architektur (vereinfachtes Diagramm: Hooks, Events, API)
    - Plugin-Verzeichnis durchsuchen und installieren
    - Plugin aktivieren, deaktivieren, konfigurieren
    - Empfohlene Plugins (Top 5–10 mit Kurzbeschreibung)
    - Plugin-Kompatibilität prüfen
    - Eigene Plugins entwickeln (Überblick, Verweis → developer-guide/plugin-development.md)
    - Fehlerbehebung bei Plugin-Problemen

    **Inhaltliche Tiefe:** Installationskommandos für jedes Beispiel-Plugin. Konfigurationsausschnitte. Kompatibilitäts-Hinweise pro Plugin.

    **Abgrenzung:** Keine Plugin-Entwicklung im Detail (→ developer-guide/plugin-development.md). Keine Kern-Konfiguration (→ configuration.md).

    **Beispiel-Inhalte:** `projektname plugin install mein-plugin`, Plugin-Konfiguration in `config.yaml`, `projektname plugin list` Ausgabe.

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
    **Zielgruppe:** Alle Nutzer, die das Produkt über die Kommandozeile bedienen.

    **Pflicht-Abschnitte:**

    - Globale Optionen (--verbose, --config, --output-format, etc.)
    - Befehlsübersicht (Tabelle: Befehl, Kurzbeschreibung)
    - Detailreferenz pro Befehl (Syntax, Optionen, Beispiele, Exit-Codes)
    - Ausgabeformate (text, json, yaml, csv)
    - Shell-Completion einrichten (bash, zsh, fish)
    - Umgebungsvariablen für CLI-Defaults
    - Häufige CLI-Patterns und Einzeiler

    **Inhaltliche Tiefe:** Vollständige Referenz — jede Option, jeder Schalter dokumentiert. Pro Befehl mindestens ein Beispiel. Maschinenlesbare Ausgabe hervorheben.

    **Abgrenzung:** Keine konzeptionellen Erklärungen (→ concepts.md). Keine Tutorials (→ tutorials/).

    **Beispiel-Inhalte:** `projektname [global-optionen] <befehl> [befehl-optionen]`, Exit-Code-Tabelle (0=OK, 1=Fehler, 2=Konfiguration).

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
    **Zielgruppe:** Nutzer, die konkrete Rezepte und Kopiervorlagen für typische Aufgaben suchen.

    **Pflicht-Abschnitte:**

    - Beispiel-Index (Tabelle: Name, Schwierigkeit, Thema)
    - Grundlegende Beispiele (5–8 Alltagsaufgaben)
    - Fortgeschrittene Beispiele (5–8 komplexere Szenarien)
    - Integrations-Beispiele (Zusammenspiel mit externen Tools)
    - Komplette Projekt-Beispiele (2–3 End-to-End-Szenarien)
    - Tipps und Best Practices pro Beispiel

    **Inhaltliche Tiefe:** Jedes Beispiel: Ziel (1 Satz), vollständiger Code/Konfiguration, erwartetes Ergebnis. Copy-paste-fähig. Keine langen Erklärungen.

    **Abgrenzung:** Keine Schritt-für-Schritt-Tutorials (→ tutorials/). Keine API-Referenz (→ developer-guide/api-reference.md).

    **Beispiel-Inhalte:** Rezept „Täglicher Export als CSV": Kommando + Cron-Eintrag. Rezept „Daten filtern und per Webhook senden".

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
    **Zielgruppe:** Nutzer, die Daten erstellen, importieren, bearbeiten, archivieren und löschen.

    **Pflicht-Abschnitte:**

    - Unterstützte Datenformate (Tabelle: Format, Import, Export, Einschränkungen)
    - Daten erstellen (manuell, per Import, per API)
    - Daten bearbeiten (Einzeln, Batch-Bearbeitung)
    - Daten suchen und filtern (Abfragesyntax)
    - Daten exportieren (Formate, Filter, Zeiträume)
    - Archivierung und Aufbewahrungsrichtlinien
    - Daten endgültig löschen (Soft-Delete vs. Hard-Delete, DSGVO)
    - Datenintegrität und Validierung

    **Inhaltliche Tiefe:** Pro Operation: CLI-Weg und UI-Weg. Import-Beispiel mit Beispieldatei. Abfragesyntax vollständig dokumentiert.

    **Abgrenzung:** Keine Datenbank-Administration (→ operations/database.md). Keine Backup-Strategie (→ backup-restore.md).

    **Beispiel-Inhalte:** CSV-Importbeispiel, Filterabfrage `status:aktiv AND erstellt:>2024-01`, Exportkommando `projektname export --format=json`.

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
    **Zielgruppe:** Nutzer und Admins, die das System in mehreren Sprachen betreiben oder lokalisieren.

    **Pflicht-Abschnitte:**

    - Unterstützte Sprachen (Tabelle: Sprache, Code, Übersetzungsgrad)
    - Systemsprache ändern (global und pro Benutzer)
    - Datumsformate, Zahlenformate, Zeitzonen konfigurieren
    - Eigene Übersetzungen hinzufügen oder korrigieren
    - Mehrsprachige Inhalte verwalten
    - RTL-Unterstützung (falls vorhanden)
    - Übersetzungs-Workflow für Mitwirkende

    **Inhaltliche Tiefe:** Konfigurationsbeispiele für jede Einstellung. Dateistruktur der Sprachdateien erklären. Hinweis auf Fallback-Verhalten.

    **Abgrenzung:** Keine Zeichenkodierungsprobleme auf Systemebene (→ operations/). Keine Plugin-Lokalisierung (→ developer-guide/).

    **Beispiel-Inhalte:** `locale: de-DE` in config.yaml, Sprachdatei-Struktur `locales/de/messages.yaml`, Datumsformat-Optionen.

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
    **Zielgruppe:** Nutzer und Admins, die ihre Daten sichern und im Notfall wiederherstellen wollen.

    **Pflicht-Abschnitte:**

    - Was wird gesichert? (Daten, Konfiguration, Uploads, Datenbank)
    - Manuelles Backup erstellen (Kommando + Erklärung)
    - Automatische Backups konfigurieren (Zeitplan, Speicherort, Rotation)
    - Backup verifizieren (Integritätsprüfung)
    - Wiederherstellung aus Backup (Schritt-für-Schritt)
    - Teilweise Wiederherstellung (nur bestimmte Daten)
    - Backup-Speicherorte (lokal, S3, NFS)
    - Disaster-Recovery-Szenario (kompletter Datenverlust)

    **Inhaltliche Tiefe:** Exakte Kommandos für jede Aktion. Zeitschätzungen für typische Datenmengen. Checkliste für regelmäßige Backup-Tests.

    **Abgrenzung:** Keine Infrastruktur-Backups (→ operations/backup-strategy.md). Keine Hochverfügbarkeit (→ tutorials/expert-high-availability.md).

    **Beispiel-Inhalte:** `projektname backup create --output /backups/`, Cron-Job für tägliches Backup, `projektname restore --from /backups/2024-01-15.tar.gz`.

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
    **Zielgruppe:** Power-User, die wiederkehrende Aufgaben automatisieren wollen.

    **Pflicht-Abschnitte:**

    - Automations-Konzept (Trigger → Bedingung → Aktion)
    - Verfügbare Trigger (Tabelle: Trigger, Beschreibung, Parameter)
    - Verfügbare Aktionen (Tabelle: Aktion, Beschreibung, Parameter)
    - Bedingungen und Filter (Syntax, Operatoren, Verschachtelung)
    - Regel erstellen (Schritt-für-Schritt mit Beispiel)
    - Regelausführung überwachen (Logs, Fehlerbehandlung)
    - Praxisbeispiele (5–8 typische Automationsrezepte)
    - Grenzen und Performance-Hinweise

    **Inhaltliche Tiefe:** Vollständige Trigger- und Aktions-Referenz. Jedes Praxisbeispiel mit komplettem YAML/JSON. Fehlerbehandlungs-Strategien erklären.

    **Abgrenzung:** Keine externen Workflow-Engines (→ integrations/). Kein Scripting/API (→ developer-guide/).

    **Beispiel-Inhalte:** Regel „Bei neuem Eintrag → E-Mail senden", YAML-Definition, Log-Ausgabe einer ausgeführten Regel.

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
    **Zielgruppe:** Nutzer, die wiederverwendbare Vorlagen für Projekte, Dokumente oder Berichte erstellen und nutzen.

    **Pflicht-Abschnitte:**

    - Template-Typen (Projekt-Templates, Dokumentvorlagen, Berichtsvorlagen)
    - Mitgelieferte Templates (Übersicht mit Beschreibung)
    - Template verwenden (Auswahl, Anpassung, Anwendung)
    - Eigenes Template erstellen (Schritt-für-Schritt)
    - Template-Variablen und Platzhalter (Syntax, verfügbare Variablen)
    - Templates teilen und importieren
    - Template-Vererbung und Komposition

    **Inhaltliche Tiefe:** Vollständige Variable-Referenz. Mindestens 2 komplette Template-Beispiele. Jinja2/Mustache-Syntax erklären (je nach Engine).

    **Abgrenzung:** Keine Code-Templates für Entwickler (→ developer-guide/). Keine E-Mail-Templates (→ operations/notifications.md).

    **Beispiel-Inhalte:** Template-Datei mit Platzhaltern `{{ projekt.name }}`, Kommando `projektname create --template=standard`, Template-Verzeichnisstruktur.

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
    **Zielgruppe:** Alle Nutzer, die Inhalte organisieren, gruppieren und wiederfinden wollen.

    **Pflicht-Abschnitte:**

    - Konzept: Tags vs. Kategorien (Unterschiede, wann was nutzen)
    - Kategorien verwalten (erstellen, bearbeiten, verschachteln, löschen)
    - Tags vergeben und entfernen (einzeln und per Batch)
    - Hierarchische Kategorien (Baumstruktur, Vererbung)
    - Filtern und Suchen nach Tags/Kategorien
    - Automatisches Tagging (Regeln, KI-basiert falls vorhanden)
    - Tag-Cloud und Statistiken
    - Best Practices für Taxonomie-Design

    **Inhaltliche Tiefe:** Schritt-für-Schritt für jede Verwaltungsaufgabe. Empfehlungen für Namenskonventionen. Performance-Hinweise bei vielen Tags.

    **Abgrenzung:** Keine Volltextsuche (→ data-management.md). Keine Automationsregeln basierend auf Tags (→ automation-rules.md).

    **Beispiel-Inhalte:** Kategorie-Baum Beispiel, `projektname tag add --name "wichtig" --item 42`, Filterbeispiel `projektname list --tag "dringend"`.

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
    **Zielgruppe:** Alle Nutzer, die ein passendes Tutorial nach Schwierigkeitsgrad und Thema suchen.

    **Pflicht-Abschnitte:**

    - Wie nutze ich die Tutorials? (Lesehinweise, Voraussetzungen)
    - Anfänger-Tutorials (Karten-Grid: Titel, Dauer, Lernziel)
    - Fortgeschrittene Tutorials (Karten-Grid: Titel, Dauer, Lernziel)
    - Experten-Tutorials (Karten-Grid: Titel, Dauer, Lernziel)
    - Empfohlene Lernpfade (nach Rolle: Endnutzer, Admin, Entwickler)
    - Voraussetzungen-Matrix (Tutorial × benötigte Vorkenntnisse)

    **Inhaltliche Tiefe:** Rein navigatorisch. Pro Tutorial: Titel, geschätzte Dauer, 1 Satz Beschreibung, Schwierigkeits-Badge. Keine eigenen Inhalte.

    **Abgrenzung:** Keine eigenen Anleitungen (→ jeweiliges Tutorial). Keine Referenz-Dokumentation (→ user-guide/).

    **Beispiel-Inhalte:** Grid mit 14 Tutorial-Karten, Lernpfad-Diagramm als Mermaid-Flowchart, Zeitschätzungen (30 Min, 1h, 2h).

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
    **Zielgruppe:** Absolute Anfänger, die ihr erstes Projekt von Grund auf erstellen wollen.

    **Pflicht-Abschnitte:**

    - Lernziele (was man nach dem Tutorial kann)
    - Voraussetzungen (installiertes Produkt, Verweis → installation.md)
    - Schritt 1: Projekt erstellen und benennen
    - Schritt 2: Grundstruktur einrichten
    - Schritt 3: Erste Daten hinzufügen
    - Schritt 4: Daten anzeigen und navigieren
    - Schritt 5: Projekt konfigurieren und anpassen
    - Schritt 6: Ergebnisse exportieren
    - Zusammenfassung und nächste Schritte

    **Inhaltliche Tiefe:** Jeder Schritt mit Kommando/UI-Anleitung, erwarteter Ausgabe und Erklärung. Screenshots oder ASCII-Art für UI-Schritte. Fehlerboxen für häufige Probleme.

    **Abgrenzung:** Keine fortgeschrittenen Features (→ tutorials/advanced-*). Keine Konfigurationsdetails (→ user-guide/configuration.md).

    **Beispiel-Inhalte:** `projektname init "Mein erstes Projekt"`, Dateistruktur des erstellten Projekts, Export als PDF.

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
    **Zielgruppe:** Anfänger, die die wichtigsten Konfigurationsoptionen kennenlernen wollen.

    **Pflicht-Abschnitte:**

    - Lernziele (Konfigurationsdatei verstehen und sicher bearbeiten)
    - Voraussetzungen (laufendes Projekt aus beginner-first-project)
    - Schritt 1: Konfigurationsdatei finden und öffnen
    - Schritt 2: Grundeinstellungen ändern (Name, Sprache, Theme)
    - Schritt 3: Änderungen anwenden und prüfen
    - Schritt 4: Umgebungsvariablen nutzen
    - Schritt 5: Konfiguration validieren
    - Häufige Konfigurationsfehler und Lösungen
    - Zusammenfassung

    **Inhaltliche Tiefe:** Kommentierte Konfigurationsausschnitte (nicht die ganze Datei). Vorher/Nachher zeigen. Validierungs-Output erklären.

    **Abgrenzung:** Keine vollständige Optionsreferenz (→ user-guide/configuration.md). Keine Produktionskonfiguration (→ tutorials/expert-production.md).

    **Beispiel-Inhalte:** Ausschnitt config.yaml vorher/nachher, `projektname config validate` Ausgabe, Umgebungsvariable `PROJEKT_PORT=9090`.

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
    **Zielgruppe:** Fortgeschrittene Nutzer, die wiederkehrende Abläufe automatisieren wollen.

    **Pflicht-Abschnitte:**

    - Lernziele (3 Automationsregeln erstellen und testen)
    - Voraussetzungen (laufendes Projekt mit Daten)
    - Schritt 1: Einfache Regel erstellen (Trigger → Aktion)
    - Schritt 2: Bedingungen hinzufügen (Filter, Logik)
    - Schritt 3: Mehrere Aktionen verketten
    - Schritt 4: Zeitgesteuerte Automation einrichten
    - Schritt 5: Regel testen und debuggen
    - Schritt 6: Produktivschaltung und Monitoring
    - Fehlerbehebung bei Automationsproblemen

    **Inhaltliche Tiefe:** 3 vollständige Automationsbeispiele (einfach → mittel → komplex). YAML/JSON für jede Regel. Log-Ausgaben zeigen.

    **Abgrenzung:** Keine Referenz aller Trigger/Aktionen (→ user-guide/automation-rules.md). Keine externe Orchestrierung (→ integrations/).

    **Beispiel-Inhalte:** Regel „Neue Einträge automatisch taggen", Regel „Täglicher Report per E-Mail", Regel „Eskalation bei überfälligen Aufgaben".

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
    **Zielgruppe:** Fortgeschrittene Nutzer, die Plugins und Erweiterungen installieren, konfigurieren und kombinieren.

    **Pflicht-Abschnitte:**

    - Lernziele (Plugin finden, installieren, konfigurieren, kombinieren)
    - Voraussetzungen (laufendes Projekt)
    - Schritt 1: Plugin-Verzeichnis durchsuchen
    - Schritt 2: Plugin installieren und aktivieren
    - Schritt 3: Plugin konfigurieren
    - Schritt 4: Mehrere Plugins kombinieren (Reihenfolge, Konflikte)
    - Schritt 5: Plugin-Updates verwalten
    - Schritt 6: Plugin deaktivieren und deinstallieren
    - Eigenes Mini-Plugin erstellen (Bonus-Abschnitt)

    **Inhaltliche Tiefe:** Konkret mit 2–3 echten oder Beispiel-Plugins durchgespielt. Konfigurationsausschnitte. Konfliktlösung demonstrieren.

    **Abgrenzung:** Keine vollständige Plugin-Entwicklung (→ developer-guide/plugin-development.md). Keine Plugin-Referenz (→ user-guide/plugins.md).

    **Beispiel-Inhalte:** Installation von „analytics-plugin" und „export-plugin", Konfiguration, Zusammenspiel der beiden, Deinstallation.

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
    **Zielgruppe:** Experten und Admins, die das System für hohe Last und große Datenmengen optimieren.

    **Pflicht-Abschnitte:**

    - Lernziele (Engpässe identifizieren und beheben)
    - Voraussetzungen (laufendes Produktivsystem, Monitoring-Zugang)
    - Schritt 1: Baseline-Metriken erfassen (Benchmarking-Tool)
    - Schritt 2: Engpässe identifizieren (Profiling, Logs)
    - Schritt 3: Datenbank-Optimierung (Indizes, Abfragen, Pooling)
    - Schritt 4: Caching konfigurieren (Redis, In-Memory, CDN)
    - Schritt 5: Ressourcen-Limits setzen (Worker, Threads, Memory)
    - Schritt 6: Ergebnisse messen und vergleichen
    - Performance-Checkliste für Produktion

    **Inhaltliche Tiefe:** Konkrete Messwerte und Befehle. Vorher/Nachher-Vergleiche mit Zahlen. Konfigurationsänderungen mit Erklärung der Auswirkung.

    **Abgrenzung:** Keine Infrastruktur-Skalierung (→ tutorials/expert-high-availability.md). Keine Code-Optimierung (→ developer-guide/).

    **Beispiel-Inhalte:** Benchmark-Befehl, Datenbank-Index-Erstellung, Caching-Konfiguration in config.yaml, Vergleichstabelle vorher/nachher.

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
    **Zielgruppe:** Admins und DevOps, die das System produktionsreif machen wollen.

    **Pflicht-Abschnitte:**

    - Lernziele (System absichern, härten, überwachen)
    - Voraussetzungen (laufendes System, Grundkenntnisse Linux/Docker)
    - Schritt 1: Sicherheits-Checkliste abarbeiten (→ security-hardening.md Kurzform)
    - Schritt 2: HTTPS/TLS konfigurieren
    - Schritt 3: Produktions-Datenbank einrichten (PostgreSQL statt SQLite)
    - Schritt 4: Reverse-Proxy konfigurieren (nginx/Caddy)
    - Schritt 5: Logging und Monitoring einrichten
    - Schritt 6: Backup-Automation konfigurieren
    - Schritt 7: Healthcheck und Alerting
    - Go-Live-Checkliste

    **Inhaltliche Tiefe:** Vollständige Konfigurationsdateien (nginx, systemd, docker-compose). Jeder Schritt mit Verifikationskommando. Sicherheitshinweise als Warnboxen.

    **Abgrenzung:** Keine Hochverfügbarkeit (→ expert-high-availability.md). Keine Performance-Tuning-Details (→ expert-performance.md).

    **Beispiel-Inhalte:** nginx-Konfiguration, systemd-Unit-File, docker-compose.prod.yaml, `projektname healthcheck` Ausgabe.

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
    **Zielgruppe:** Anfänger, die bestehende Daten aus Dateien oder anderen Quellen importieren wollen.

    **Pflicht-Abschnitte:**

    - Lernziele (CSV, JSON und Excel importieren können)
    - Voraussetzungen (laufendes Projekt, Beispieldateien)
    - Schritt 1: Importformate verstehen (CSV, JSON, XLSX — Anforderungen)
    - Schritt 2: Beispieldaten herunterladen oder erstellen
    - Schritt 3: CSV-Import durchführen (Mapping, Encoding, Trennzeichen)
    - Schritt 4: JSON-Import durchführen
    - Schritt 5: Import validieren und Fehler beheben
    - Schritt 6: Daten nach Import prüfen und bereinigen
    - Häufige Import-Probleme (Encoding, Datumsformate, Duplikate)

    **Inhaltliche Tiefe:** Beispieldateien als Codeblöcke eingebettet. Jedes Format Schritt für Schritt. Fehlerausgaben und deren Lösung zeigen.

    **Abgrenzung:** Keine API-basierte Datenintegration (→ tutorials/advanced-api-usage.md). Keine Batch-Verarbeitung (→ user-guide/advanced-features.md).

    **Beispiel-Inhalte:** 5-Zeilen-CSV-Beispiel, `projektname import --format=csv daten.csv`, Fehlermeldung bei falschem Encoding und Lösung.

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
    **Zielgruppe:** Fortgeschrittene Nutzer und Entwickler, die das System per API programmatisch nutzen wollen.

    **Pflicht-Abschnitte:**

    - Lernziele (API-Authentifizierung, CRUD-Operationen, Pagination)
    - Voraussetzungen (laufendes System, API-Key, curl oder httpie installiert)
    - Schritt 1: API-Key erstellen und testen
    - Schritt 2: Daten per API lesen (GET, Filter, Pagination)
    - Schritt 3: Daten erstellen und aktualisieren (POST, PUT/PATCH)
    - Schritt 4: Daten löschen (DELETE, Soft-Delete)
    - Schritt 5: Fehlerbehandlung (HTTP-Codes, Fehlerformat)
    - Schritt 6: Python/JavaScript-Client-Bibliothek nutzen
    - Rate-Limiting und Best Practices

    **Inhaltliche Tiefe:** Jeder API-Call als curl-Beispiel UND als Python-Snippet. Response-Bodies vollständig zeigen. Pagination-Logik komplett erklären.

    **Abgrenzung:** Keine API-Referenz (→ developer-guide/api-reference.md). Keine Webhooks (→ tutorials/advanced-webhooks.md).

    **Beispiel-Inhalte:** `curl -H "Authorization: Bearer TOKEN" https://localhost/api/v1/items`, Python requests-Beispiel, Paginierungs-Schleife.

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
    **Zielgruppe:** Fortgeschrittene Nutzer, die eigene Berichte und Dashboards erstellen wollen.

    **Pflicht-Abschnitte:**

    - Lernziele (3 verschiedene Berichtstypen erstellen)
    - Voraussetzungen (laufendes Projekt mit Daten)
    - Schritt 1: Eingebaute Berichte verstehen und anpassen
    - Schritt 2: Einfachen tabellarischen Bericht erstellen
    - Schritt 3: Bericht mit Diagrammen und Visualisierungen
    - Schritt 4: Zeitgesteuerten Bericht einrichten (E-Mail, PDF-Export)
    - Schritt 5: Dashboard mit mehreren Widgets zusammenstellen
    - Schritt 6: Berichtsvorlage speichern und teilen
    - Datenquellen und Aggregationsfunktionen

    **Inhaltliche Tiefe:** Vollständige Berichtsdefinitionen als YAML/JSON. Screenshots oder Beschreibung der Ausgabe. Aggregationsfunktionen mit Beispielen.

    **Abgrenzung:** Keine BI-Tool-Integration (→ integrations/). Keine Rohdaten-Abfragen (→ developer-guide/).

    **Beispiel-Inhalte:** Berichtsdefinition YAML, Diagramm-Konfiguration, Cron-Job für wöchentlichen PDF-Versand.

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
    **Zielgruppe:** Experten und Infrastruktur-Admins, die Ausfallsicherheit und Skalierung konfigurieren.

    **Pflicht-Abschnitte:**

    - Lernziele (redundantes Setup mit Failover aufbauen)
    - Voraussetzungen (2+ Server, Load Balancer, gemeinsamer Speicher)
    - Schritt 1: Architektur planen (Diagramm: LB → App-Nodes → DB)
    - Schritt 2: Datenbank-Replikation einrichten (Primary/Replica)
    - Schritt 3: Mehrere App-Instanzen konfigurieren (Shared Session, Shared Storage)
    - Schritt 4: Load Balancer konfigurieren (Health Checks, Sticky Sessions)
    - Schritt 5: Failover testen (Node abschalten, Verhalten beobachten)
    - Schritt 6: Monitoring und Alerting für den Cluster
    - Skalierungs-Strategien (horizontal vs. vertikal)

    **Inhaltliche Tiefe:** Vollständige Konfigurationsdateien für jeden Schritt. Architektur-Diagramm als Mermaid. Failover-Testskript. Metriken und Schwellwerte.

    **Abgrenzung:** Keine Einzelserver-Performance (→ expert-performance.md). Keine Kubernetes-Orchestrierung (→ operations/kubernetes.md).

    **Beispiel-Inhalte:** docker-compose mit 2 App-Containern + 1 DB-Container + nginx-LB, Failover-Testskript, HAProxy-Konfiguration.

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
    **Zielgruppe:** Anfänger, die die Benutzeroberfläche Schritt für Schritt kennenlernen wollen.

    **Pflicht-Abschnitte:**

    - Lernziele (UI navigieren, Hauptfunktionen finden und nutzen)
    - Voraussetzungen (laufendes System, Browser, Zugangsdaten)
    - Schritt 1: Anmelden und Dashboard erkunden
    - Schritt 2: Navigation und Menüstruktur verstehen
    - Schritt 3: Hauptbereiche durchgehen (Projekte, Daten, Einstellungen)
    - Schritt 4: Eintrag erstellen, bearbeiten, löschen über die UI
    - Schritt 5: Suche und Filter nutzen
    - Schritt 6: Persönliche Einstellungen anpassen (Theme, Sprache, Benachrichtigungen)
    - Tastenkürzel und Produktivitätstipps

    **Inhaltliche Tiefe:** Beschreibender Text mit Hinweisen wo welche Elemente zu finden sind (da keine echten Screenshots möglich). Jeder Schritt: was klicken, was erwarten.

    **Abgrenzung:** Keine CLI-Nutzung (→ user-guide/cli-reference.md). Keine Admin-Oberfläche (→ user-guide/permissions.md).

    **Beispiel-Inhalte:** Beschreibung des Dashboard-Layouts, Navigationsmenü-Struktur, Tastenkürzel-Tabelle (Ctrl+K=Suche, etc.).

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
    **Zielgruppe:** Fortgeschrittene Nutzer, die das System per Webhooks mit externen Diensten verbinden wollen.

    **Pflicht-Abschnitte:**

    - Lernziele (Webhook einrichten, testen, absichern)
    - Voraussetzungen (laufendes System, externer Endpunkt oder RequestBin zum Testen)
    - Schritt 1: Webhook-Konzept verstehen (Event → HTTP POST → Empfänger)
    - Schritt 2: Ersten Webhook registrieren (URL, Events, Format)
    - Schritt 3: Webhook testen (manueller Trigger, Payload inspizieren)
    - Schritt 4: Webhook absichern (HMAC-Signatur, Secret, HTTPS)
    - Schritt 5: Fehlerbehandlung (Retry-Logik, Dead-Letter-Queue)
    - Schritt 6: Praxisbeispiel — Slack/Teams-Benachrichtigung
    - Webhook-Payload-Referenz (alle Event-Typen)

    **Inhaltliche Tiefe:** Vollständige Payload-Beispiele als JSON. HMAC-Verifizierungscode in Python. Retry-Verhalten dokumentiert.

    **Abgrenzung:** Keine API-Nutzung (→ tutorials/advanced-api-usage.md). Keine Automationsregeln (→ user-guide/automation-rules.md).

    **Beispiel-Inhalte:** Webhook-Registration per CLI/UI, JSON-Payload eines „item.created" Events, Python-Skript zur HMAC-Verifikation.

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
    **Zielgruppe:** Fortgeschrittene Nutzer und Admins, die eine vollständige Backup-Strategie implementieren wollen.

    **Pflicht-Abschnitte:**

    - Lernziele (vollständige Backup-Strategie aufbauen und testen)
    - Voraussetzungen (laufendes Produktivsystem mit Daten)
    - Schritt 1: Backup-Strategie planen (RPO, RTO, 3-2-1-Regel)
    - Schritt 2: Vollbackup erstellen und verifizieren
    - Schritt 3: Inkrementelle Backups konfigurieren
    - Schritt 4: Automatische Backup-Rotation einrichten
    - Schritt 5: Remote-Backup konfigurieren (S3, NFS, rsync)
    - Schritt 6: Disaster-Recovery-Test durchführen (komplette Wiederherstellung)
    - Schritt 7: Monitoring und Alerting für Backup-Jobs
    - Backup-Strategie-Dokumentation (Template)

    **Inhaltliche Tiefe:** Vollständige Skripte und Cron-Jobs. Zeitschätzungen für verschiedene Datenmengen. DR-Test als Checkliste. RPO/RTO-Berechnung erklären.

    **Abgrenzung:** Keine Grundlagen (→ user-guide/backup-restore.md). Keine HA-Konfiguration (→ tutorials/expert-high-availability.md).

    **Beispiel-Inhalte:** Backup-Skript mit Rotation, S3-Upload-Kommando, DR-Test-Checkliste, Monitoring-Skript das bei Fehler alarmiert.

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
    **Zielgruppe:** Security-bewusste Admins, die das System gegen Angriffe absichern wollen.

    **Pflicht-Abschnitte:**

    - Lernziele (System nach CIS-Benchmark-Vorbild härten)
    - Voraussetzungen (laufendes Produktivsystem, Root/Admin-Zugang)
    - Schritt 1: Sicherheits-Audit durchführen (eingebauter Security-Check)
    - Schritt 2: Authentifizierung härten (Passwortrichtlinien, 2FA, Session-Timeout)
    - Schritt 3: Netzwerk absichern (Firewall, TLS-Konfiguration, Header)
    - Schritt 4: Dateisystem-Berechtigungen einschränken
    - Schritt 5: Logging und Audit-Trail konfigurieren
    - Schritt 6: Dependency-Scanning und Updates
    - Schritt 7: Penetrationstest-Grundlagen (OWASP Top 10 prüfen)
    - Security-Hardening-Checkliste (zum Abhaken)

    **Inhaltliche Tiefe:** Konkrete Konfigurationsänderungen mit Vorher/Nachher. TLS-Cipher-Suites auflisten. Security-Header komplett. Checkliste als Tabelle mit Status-Spalte.

    **Abgrenzung:** Keine Benutzerrechteverwaltung (→ user-guide/permissions.md). Keine Netzwerk-Infrastruktur (→ operations/networking.md).

    **Beispiel-Inhalte:** nginx Security-Header-Konfiguration, TLS 1.3 Config, `projektname security audit` Ausgabe, OWASP-Checkliste.

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
    **Zielgruppe:** Endanwender ohne technische Vorkenntnisse, die das Produkt erstmals nutzen

    **Pflicht-Abschnitte:**

    - Was ist dieses Produkt? (2-3 Sätze Elevator-Pitch)
    - Kernfunktionen im Überblick (Bullet-Liste, max. 8 Punkte)
    - Schnellstart: Vom Login bis zur ersten Aktion in 5 Schritten
    - Systemvoraussetzungen (Browser, Betriebssystem, Bildschirmauflösung)
    - Wo finde ich Hilfe? (Support-Kanäle, FAQ-Link)

    **Inhaltliche Tiefe:** Nur Oberfläche — keine technischen Details, keine Admin-Themen. Verwende Screenshots mit nummerierten Callouts. Jeder Schritt maximal 2 Sätze.

    **Abgrenzung:** Keine Installationsanleitung (→ getting-started/installation.md), keine API-Dokumentation (→ api/), keine Admin-Funktionen (→ manual/admin-panel.md)

    **Beispiel-Inhalte:** Screenshot der Startseite mit Callouts auf Hauptnavigation, Suchfeld und Benutzerprofil; Tabelle «Funktion → Kurzbeschreibung → Seite»


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
    **Zielgruppe:** Alle Endanwender, die sich im Interface orientieren wollen

    **Pflicht-Abschnitte:**

    - Aufbau des Hauptbildschirms (Header, Sidebar, Content-Bereich, Footer)
    - Hauptnavigation und Menüstruktur (Hierarchie-Diagramm)
    - Kontextmenüs und Rechtsklick-Aktionen
    - Breadcrumb-Navigation und Seitenhistorie
    - Responsive Verhalten bei verschiedenen Bildschirmgrößen

    **Inhaltliche Tiefe:** Annotierte Screenshots für jeden Bildschirmbereich. Beschreibe jedes UI-Element mit Name, Position und Funktion. Nutze eine nummerierte Legende.

    **Abgrenzung:** Keine Workflow-Beschreibungen (→ manual/workflows.md), keine mobilen Layouts (→ manual/mobile.md), keine Admin-UI (→ manual/admin-panel.md)

    **Beispiel-Inhalte:** Annotierter Screenshot mit «1 = Hauptmenü, 2 = Suchleiste, 3 = Benachrichtigungsglocke»; Tabelle aller Menüpunkte mit Icon, Label und Zielseite


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
    **Zielgruppe:** Endanwender, die konkrete Aufgaben erledigen wollen

    **Pflicht-Abschnitte:**

    - Übersicht der häufigsten Workflows (Tabelle: Workflow → Komplexität → Zeitbedarf)
    - Schritt-für-Schritt-Anleitung pro Workflow (nummerierte Liste mit Screenshots)
    - Entscheidungspunkte und Verzweigungen (Flussdiagramme)
    - Häufige Fehler und deren Behebung pro Workflow
    - Tipps zur Effizienzsteigerung

    **Inhaltliche Tiefe:** Jeder Workflow als eigenständiger Abschnitt mit Vorbedingungen, Schritten und erwartetem Ergebnis. Maximal 10 Schritte pro Workflow. Verwende Admonitions (tip, warning) für Sonderfälle.

    **Abgrenzung:** Keine UI-Erklärung (→ manual/ui-overview.md), keine Massen-Workflows (→ manual/bulk-operations.md), keine Admin-Workflows (→ manual/admin-panel.md)

    **Beispiel-Inhalte:** Workflow «Neuen Datensatz anlegen»: 1. Klick auf ‹+Neu› 2. Formular ausfüllen 3. Speichern; Flussdiagramm mit Ja/Nein-Verzweigung bei Validierungsfehlern


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
    **Zielgruppe:** Alle Endanwender, die Daten schnell finden müssen

    **Pflicht-Abschnitte:**

    - Einfache Suche vs. erweiterte Suche (Vergleichstabelle)
    - Suchsyntax und Operatoren (AND, OR, NOT, Wildcards, Phrasensuche)
    - Filter setzen, kombinieren und speichern
    - Sortieroptionen und deren Wirkung
    - Gespeicherte Suchen und Suchvorlagen
    - Suchergebnisse interpretieren (Relevanz, Hervorhebung)

    **Inhaltliche Tiefe:** Jeder Operator mit Syntax-Beispiel und Ergebnis-Screenshot. Filterkombinationen als Entscheidungstabelle darstellen.

    **Abgrenzung:** Keine Volltextindex-Konfiguration (→ architecture/caching.md), keine API-Suchendpunkte (→ formats/api-formats.md)

    **Beispiel-Inhalte:** Tabelle «Operator → Beispiel → Ergebnis»: z.B. `name:"Müller" AND status:aktiv`; Screenshot der Filter-Sidebar mit drei aktiven Filtern


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
    **Zielgruppe:** Endanwender, die über Ereignisse informiert bleiben wollen

    **Pflicht-Abschnitte:**

    - Arten von Benachrichtigungen (In-App, E-Mail, Push, SMS)
    - Benachrichtigungszentrale: Aufbau und Bedienung
    - Benachrichtigungen konfigurieren (Kanäle, Häufigkeit, Stummschaltung)
    - Abonnements verwalten (Themen, Objekte, Personen)
    - Benachrichtigungshistorie und Archiv

    **Inhaltliche Tiefe:** Pro Benachrichtigungstyp: Auslöser, Inhalt, Kanal, Beispiel. Konfigurationsoptionen als Tabelle mit Standardwerten.

    **Abgrenzung:** Keine Systembenachrichtigungen für Admins (→ manual/admin-panel.md), kein Event-System-Internals (→ architecture/event-system.md)

    **Beispiel-Inhalte:** Screenshot der Benachrichtigungsglocke mit Badge-Zähler; Tabelle «Ereignis → Standard-Kanal → Anpassbar?»: z.B. «Neuer Kommentar → In-App + E-Mail → Ja»


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
    **Zielgruppe:** Power-User, die effizient mit Tastatur arbeiten wollen

    **Pflicht-Abschnitte:**

    - Globale Tastenkürzel (Navigation, Suche öffnen, Hilfe)
    - Kontextbezogene Kürzel (Editor, Tabelle, Formular)
    - Tastenkürzel anpassen und eigene erstellen
    - Übersicht als druckbare Referenzkarte
    - Konflikte mit Browser-/Betriebssystem-Kürzeln

    **Inhaltliche Tiefe:** Vollständige Referenztabelle mit Spalten: Aktion, Windows/Linux, macOS. Gruppiert nach Kontext. Maximal 50 Kürzel.

    **Abgrenzung:** Keine Workflow-Beschreibungen (→ manual/workflows.md), keine Accessibility-Tastatursteuerung (→ manual/accessibility.md)

    **Beispiel-Inhalte:** Tabelle: «Strg+K → Suche öffnen | Cmd+K»; «Strg+S → Speichern | Cmd+S»; druckbare PDF-Karte als Download-Link


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
    **Zielgruppe:** Endanwender, die Daten zwischen Systemen bewegen

    **Pflicht-Abschnitte:**

    - Unterstützte Import-Formate (CSV, Excel, JSON, XML — Vergleichstabelle)
    - Schritt-für-Schritt-Anleitung Import (Datei wählen, Mapping, Validierung, Ausführung)
    - Unterstützte Export-Formate und Optionen
    - Schritt-für-Schritt-Anleitung Export
    - Fehlerbehandlung bei Import (Validierungsfehler, Duplikate, fehlende Pflichtfelder)
    - Zeitgesteuerte Importe/Exporte einrichten

    **Inhaltliche Tiefe:** Je Format eine Beispieldatei (3-5 Zeilen) zeigen. Mapping-Tabelle: Quellspalte → Zielspalte. Fehlermeldungen mit Lösung auflisten.

    **Abgrenzung:** Keine Format-Spezifikationen (→ formats/input-formats.md, formats/output-formats.md), keine API-basierte Integration (→ formats/api-formats.md), keine Datenmigration (→ formats/migration-formats.md)

    **Beispiel-Inhalte:** CSV-Beispiel mit Kopfzeile und 3 Datenzeilen; Screenshot des Mapping-Dialogs; Fehlermeldung «Zeile 42: Pflichtfeld ‹E-Mail› fehlt»


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
    **Zielgruppe:** Endanwender und Teamleiter, die Berichte erstellen und teilen

    **Pflicht-Abschnitte:**

    - Verfügbare Berichtstypen (Tabelle: Name → Datenquelle → Aktualisierung)
    - Bericht erstellen: Parameter, Filter, Zeitraum wählen
    - Bericht anpassen: Spalten, Gruppierung, Diagrammtyp
    - Export als PDF, Excel, CSV
    - Berichte zeitgesteuert versenden (Scheduling)
    - Berichte teilen und Berechtigungen

    **Inhaltliche Tiefe:** Jeden Berichtstyp mit Screenshot des fertigen Berichts zeigen. Export-Optionen als Vergleichstabelle (Format → Vor-/Nachteile).

    **Abgrenzung:** Keine Berichts-Dateiformate (→ formats/report-formats.md), keine Dashboard-Widgets (→ manual/dashboard.md), keine API-Endpunkte (→ formats/api-formats.md)

    **Beispiel-Inhalte:** Screenshot eines Monatsberichts mit Balkendiagramm; Tabelle «Berichtstyp → Verfügbare Filter → Standard-Zeitraum»


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
    **Zielgruppe:** Endanwender, die ihr persönliches Nutzungserlebnis anpassen möchten

    **Pflicht-Abschnitte:**

    - Profil bearbeiten (Name, Avatar, Kontaktdaten)
    - Sicherheitseinstellungen (Passwort ändern, 2FA einrichten)
    - Darstellung (Sprache, Theme, Schriftgröße, Datumsformat)
    - Benachrichtigungseinstellungen (Kurzlink zu manual/notifications.md)
    - Datenschutz-Einstellungen (Sichtbarkeit, Tracking)
    - Einstellungen exportieren und zurücksetzen

    **Inhaltliche Tiefe:** Jede Einstellung mit Pfad im Menü, Standardwert und Screenshot. Sicherheitsrelevante Optionen mit Admonition ‹warning› hervorheben.

    **Abgrenzung:** Keine systemweiten Einstellungen (→ manual/admin-panel.md), keine Konfigurationsdateien (→ formats/config-files.md)

    **Beispiel-Inhalte:** Pfad «Einstellungen → Darstellung → Theme → Dunkel»; Screenshot der 2FA-Einrichtung mit QR-Code (Platzhalter); Tabelle aller Einstellungen mit Standardwerten


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
    **Zielgruppe:** Teams, die gemeinsam auf dem System arbeiten

    **Pflicht-Abschnitte:**

    - Benutzerrollen und Berechtigungsstufen (Tabelle: Rolle → Rechte)
    - Benutzer einladen und verwalten
    - Gruppen und Teams anlegen
    - Gemeinsame Ressourcen teilen (Ordner, Berichte, Vorlagen)
    - Aktivitätenprotokoll und Audit-Trail

    **Inhaltliche Tiefe:** Rollen-Rechte-Matrix als vollständige Tabelle. Einladungs-Workflow Schritt für Schritt. Teilen-Dialog mit Screenshot.

    **Abgrenzung:** Keine Echtzeit-Zusammenarbeit (→ manual/collaboration.md), keine Admin-Benutzerverwaltung (→ manual/admin-panel.md), keine Sicherheitsarchitektur (→ architecture/security-architecture.md)

    **Beispiel-Inhalte:** Tabelle «Betrachter: lesen=Ja, bearbeiten=Nein, löschen=Nein | Bearbeiter: lesen=Ja, bearbeiten=Ja, löschen=Nein»; Screenshot der Einladungs-E-Mail


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
    **Zielgruppe:** Nutzer mit Einschränkungen, Barrierefreiheits-Beauftragte

    **Pflicht-Abschnitte:**

    - Unterstützte Screenreader und Kompatibilität
    - Tastaturnavigation (vollständige Tab-Reihenfolge)
    - Kontrast-Modi und Schriftgrößenanpassung
    - ARIA-Landmarks und Seitenstruktur
    - Bekannte Einschränkungen und Workarounds
    - Konformität (WCAG-Level, BITV)

    **Inhaltliche Tiefe:** Konformitätstabelle nach WCAG 2.1 AA-Kriterien. Pro Screenreader (NVDA, JAWS, VoiceOver) getestete Funktionen auflisten.

    **Abgrenzung:** Keine allgemeinen Tastenkürzel (→ manual/shortcuts.md), keine mobilen Gesten (→ manual/mobile.md)

    **Beispiel-Inhalte:** Tabelle «WCAG-Kriterium → Status → Anmerkung»; Anleitung zur Nutzung mit NVDA: «Tab → Hauptnavigation → Pfeil-unten → Menüpunkt wählen»


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
    **Zielgruppe:** Endanwender, die ihren Arbeitsbereich personalisieren möchten

    **Pflicht-Abschnitte:**

    - Dashboard-Aufbau und Standard-Widgets
    - Widgets hinzufügen, entfernen und anordnen (Drag & Drop)
    - Widget-Konfiguration (Datenquelle, Zeitraum, Darstellungstyp)
    - Dashboard-Layouts speichern und teilen
    - Datenaktualisierung und Auto-Refresh

    **Inhaltliche Tiefe:** Pro Standard-Widget: Name, Screenshot, konfigurierbare Parameter. Layout-Raster erklären (Spalten, Zeilen). Aktualisierungsintervalle als Tabelle.

    **Abgrenzung:** Keine Berichterstellung (→ manual/reports.md), keine Datenansichten außerhalb des Dashboards (→ manual/data-views.md)

    **Beispiel-Inhalte:** Screenshot Standard-Dashboard mit 4 Widgets; Widget «Letzte Aktivitäten»: zeigt die letzten 10 Aktionen mit Zeitstempel und Benutzer


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
    **Zielgruppe:** Endanwender, die Daten in verschiedenen Formaten betrachten wollen

    **Pflicht-Abschnitte:**

    - Tabellenansicht: Spalten konfigurieren, sortieren, filtern
    - Kartenansicht (Kanban): Spalten definieren, Karten verschieben
    - Listenansicht: kompakte Darstellung
    - Kalenderansicht: Termine und Fristen
    - Ansichten wechseln, speichern und teilen

    **Inhaltliche Tiefe:** Pro Ansicht: Screenshot, Konfigurationsoptionen, Vor-/Nachteile. Vergleichstabelle aller Ansichten (Ansicht → Stärke → Einsatzzweck).

    **Abgrenzung:** Keine Dashboard-Widgets (→ manual/dashboard.md), keine Berichtsansichten (→ manual/reports.md), keine Such-/Filtermechanik (→ manual/search.md)

    **Beispiel-Inhalte:** Tabellenansicht mit sortierbaren Spalten «Name, Status, Datum»; Kanban-Board mit Spalten «Offen → In Bearbeitung → Erledigt»


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
    **Zielgruppe:** Teams, die gleichzeitig an Inhalten arbeiten

    **Pflicht-Abschnitte:**

    - Echtzeit-Bearbeitung: Cursor anderer Benutzer, Änderungsindikatoren
    - Kommentare und Diskussionen (inline, am Objekt)
    - @-Erwähnungen und Zuweisung
    - Konflikterkennung und -lösung bei gleichzeitiger Bearbeitung
    - Präsenz-Anzeige (wer ist gerade online/aktiv)

    **Inhaltliche Tiefe:** Konfliktszenarien mit Vorher/Nachher-Screenshots. Kommentar-Workflow als Flussdiagramm (Erstellen → Antworten → Lösen → Archivieren).

    **Abgrenzung:** Keine Benutzerverwaltung (→ manual/multi-user.md), keine Versionierung (→ manual/history-versioning.md), keine Benachrichtigungen (→ manual/notifications.md)

    **Beispiel-Inhalte:** Screenshot mit zwei Benutzern im gleichen Dokument (farbige Cursor); Beispiel-Kommentar: «@Max bitte den Absatz prüfen» mit Antwort und Erledigt-Haken


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
    **Zielgruppe:** Nutzer, die ohne stabile Internetverbindung arbeiten müssen

    **Pflicht-Abschnitte:**

    - Welche Funktionen offline verfügbar sind (Ja/Nein-Tabelle)
    - Offline-Modus aktivieren und Daten vorab synchronisieren
    - Arbeiten im Offline-Modus (Einschränkungen, Hinweise)
    - Synchronisation beim Wiederherstellen der Verbindung
    - Konfliktauflösung nach Offline-Bearbeitung

    **Inhaltliche Tiefe:** Vollständige Funktions-Tabelle mit Offline-Status. Sync-Prozess als Sequenzdiagramm. Speicherplatzbedarf für Offline-Daten angeben.

    **Abgrenzung:** Keine mobile-spezifische Offline-Funktion (→ manual/mobile.md), keine Backup-Strategien (→ formats/backup-formats.md), keine Architektur der Sync-Engine (→ architecture/data-flow.md)

    **Beispiel-Inhalte:** Tabelle «Datensätze anzeigen → offline: Ja | Neuen Datensatz anlegen → offline: Ja (wird bei Sync übertragen) | Berichte generieren → offline: Nein»


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
    **Zielgruppe:** Nutzer, die auf Smartphone oder Tablet arbeiten

    **Pflicht-Abschnitte:**

    - Unterstützte Plattformen (iOS ab Version X, Android ab Version Y)
    - App installieren und einrichten
    - Unterschiede zur Desktop-Version (Feature-Matrix)
    - Gesten und Touch-Bedienung
    - Push-Benachrichtigungen konfigurieren
    - Offline-Modus auf mobilen Geräten

    **Inhaltliche Tiefe:** Feature-Vergleichstabelle Desktop vs. Mobile. Gesten-Referenz (Swipe, Pinch, Long-Press) mit Beschreibung. Screenshots vom mobilen UI.

    **Abgrenzung:** Keine Desktop-UI-Beschreibung (→ manual/ui-overview.md), keine allgemeine Offline-Funktion (→ manual/offline-mode.md)

    **Beispiel-Inhalte:** Screenshot der mobilen Listenansicht; Gesten-Tabelle: «Swipe links → Löschen | Swipe rechts → Archivieren | Long-Press → Kontextmenü»


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
    **Zielgruppe:** Endanwender, die Dateien hochladen, organisieren und teilen

    **Pflicht-Abschnitte:**

    - Dateien hochladen (Einzel, Mehrfach, Drag & Drop)
    - Ordnerstruktur anlegen und verwalten
    - Dateien verschieben, kopieren, umbenennen
    - Dateivorschau und unterstützte Formate
    - Freigabe und Zugriffsrechte pro Datei/Ordner
    - Speicherplatz und Kontingente

    **Inhaltliche Tiefe:** Upload-Limits (Dateigröße, Dateitypen) als Tabelle. Vorschau-Kompatibilität pro Format. Freigabe-Dialog mit Screenshot.

    **Abgrenzung:** Keine Backup-Formate (→ formats/backup-formats.md), keine Medienformat-Details (→ formats/image-formats.md), keine Versionierung (→ manual/history-versioning.md)

    **Beispiel-Inhalte:** Tabelle «Format → Max. Größe → Vorschau verfügbar»: «PDF → 50 MB → Ja | MP4 → 500 MB → Ja (Streaming) | ZIP → 200 MB → Nein»


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
    **Zielgruppe:** Endanwender, die wiederkehrende Strukturen effizient nutzen wollen

    **Pflicht-Abschnitte:**

    - Verfügbare Vorlagen durchsuchen und vorschauen
    - Vorlage auf neuen Datensatz anwenden
    - Eigene Vorlagen erstellen und speichern
    - Vorlagen teilen und als Standard festlegen
    - Platzhalter und dynamische Felder in Vorlagen

    **Inhaltliche Tiefe:** Platzhalter-Syntax mit Beispielen (z.B. `{{datum}}`, `{{benutzer}}`). Vorlagen-Galerie als Screenshot. Erstellungs-Workflow Schritt für Schritt.

    **Abgrenzung:** Keine Template-Dateiformate (→ formats/template-formats.md), keine Berichtsvorlagen (→ manual/reports.md)

    **Beispiel-Inhalte:** Vorlage «Wochenbericht»: Platzhalter {{kw}}, {{autor}}, {{zusammenfassung}}; Screenshot des Vorlagen-Auswahldialogs mit Kategoriefilter


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
    **Zielgruppe:** Endanwender, die Änderungen nachverfolgen und rückgängig machen wollen

    **Pflicht-Abschnitte:**

    - Änderungsverlauf anzeigen (Timeline, Diff-Ansicht)
    - Versionen vergleichen (Side-by-Side, Inline-Diff)
    - Frühere Version wiederherstellen
    - Automatische vs. manuelle Versionierung
    - Aufbewahrungsfristen und Speicherlimits

    **Inhaltliche Tiefe:** Diff-Darstellung mit farblicher Markierung (grün = hinzugefügt, rot = entfernt) als Screenshot. Wiederherstellungsprozess in 3 Schritten.

    **Abgrenzung:** Keine Echtzeit-Zusammenarbeit (→ manual/collaboration.md), keine Audit-Logs (→ manual/multi-user.md), keine Datenbank-Migrationen (→ formats/migration-formats.md)

    **Beispiel-Inhalte:** Screenshot der Versionsliste: «v3 — Max, 14:30 — ‹Absatz 2 geändert› | v2 — Lisa, 10:15 — ‹Tabelle hinzugefügt›»; Diff-Ansicht mit Hervorhebungen


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
    **Zielgruppe:** Power-User, die viele Datensätze gleichzeitig bearbeiten

    **Pflicht-Abschnitte:**

    - Mehrfachauswahl (Checkboxen, Bereich-Auswahl, Alle auswählen)
    - Verfügbare Massenaktionen (Bearbeiten, Löschen, Verschieben, Exportieren, Status ändern)
    - Massenbearbeitung: Felder für alle gewählten Datensätze ändern
    - Fortschrittsanzeige und Abbruchmöglichkeit
    - Fehlerprotokoll nach Massenoperation

    **Inhaltliche Tiefe:** Jede Massenaktion mit maximal zulässiger Anzahl, geschätzter Dauer und Rückgängig-Option. Fehlerprotokoll-Format erklären.

    **Abgrenzung:** Keine Einzel-Workflows (→ manual/workflows.md), keine Import-/Export-Massendaten (→ manual/import-export.md)

    **Beispiel-Inhalte:** Screenshot: 25 ausgewählte Datensätze, Aktionsleiste «Status ändern → Erledigt»; Fehlerprotokoll: «3 von 25 fehlgeschlagen — Zeile 7: gesperrt, Zeile 12: Berechtigung fehlt»


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
    **Zielgruppe:** System-Administratoren und Team-Leads mit Admin-Rechten

    **Pflicht-Abschnitte:**

    - Admin-Panel aufrufen und Übersicht
    - Benutzerverwaltung (Anlegen, Sperren, Rollen zuweisen)
    - Systemeinstellungen (E-Mail, Speicher, Sicherheit)
    - Audit-Log und Aktivitätsprotokoll
    - Systemstatus und Monitoring (Health-Check, Speicherverbrauch)
    - Wartung (Cache leeren, Indizes neu aufbauen, Backups)

    **Inhaltliche Tiefe:** Jede Admin-Funktion mit Menüpfad, erforderlicher Rolle und Screenshot. Kritische Aktionen (Benutzer löschen, System zurücksetzen) mit ‹danger›-Admonition markieren.

    **Abgrenzung:** Keine Endanwender-Einstellungen (→ manual/settings.md), keine Architektur-Details (→ architecture/overview.md), keine Deployment-Konfiguration (→ architecture/deployment-architecture.md)

    **Beispiel-Inhalte:** Screenshot Admin-Dashboard mit KPIs (aktive Nutzer, Speicherverbrauch, offene Tickets); Tabelle «Systemeinstellung → Standardwert → Empfehlung»


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
    **Zielgruppe:** Entwickler und Integratoren, die wissen müssen, welche Formate das System verarbeitet

    **Pflicht-Abschnitte:**

    - Gesamtübersicht aller Dateiformate (Tabelle: Format → Zweck → Richtung → Seite)
    - Kategorisierung: Eingabe, Ausgabe, Konfiguration, Austausch
    - Gemeinsame Konventionen (Zeichencodierung, Zeilenenden, Mime-Types)
    - Versionierung von Formaten (Kompatibilitätsmatrix)

    **Inhaltliche Tiefe:** Navigations-Tabelle als zentrales Element. Jedes Format in einer Zeile mit Link zur Detailseite. Konventionen (UTF-8, LF) einmalig hier definieren und in Unterseiten referenzieren.

    **Abgrenzung:** Keine Detail-Spezifikationen (→ jeweilige Unterseiten), keine API-Dokumentation (→ formats/api-formats.md)

    **Beispiel-Inhalte:** Tabelle: «CSV → Datenimport → Eingabe → formats/input-formats.md | JSON → API-Response → Ausgabe → formats/api-formats.md»


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
    **Zielgruppe:** Entwickler und Datenlieferanten, die Daten ins System einspeisen

    **Pflicht-Abschnitte:**

    - CSV-Format: Trennzeichen, Quoting, Header-Zeile, Encoding
    - Excel-Format: unterstützte Versionen (.xlsx, .xls), Blattauswahl, Datentypen
    - JSON-Format: Schema, verschachtelte Strukturen, Arrays
    - XML-Format: Schema/DTD, Namespaces
    - Validierungsregeln pro Format
    - Fehlercodes bei ungültigem Input

    **Inhaltliche Tiefe:** Pro Format: vollständiges Minimalbeispiel (5-10 Zeilen), JSON-Schema oder DTD, Validierungsregeln als Tabelle. Fehlercodes mit Bedeutung und Lösung.

    **Abgrenzung:** Keine Benutzer-Anleitung zum Import (→ manual/import-export.md), keine Ausgabeformate (→ formats/output-formats.md)

    **Beispiel-Inhalte:** CSV: `name;email;rolle\n"Müller";"m@x.de";"admin"`; JSON-Schema-Auszug mit required-Feldern; Fehler E1001: «Ungültiges Datumsformat in Spalte 3»


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
    **Zielgruppe:** Entwickler und nachgelagerte Systeme, die exportierte Daten weiterverarbeiten

    **Pflicht-Abschnitte:**

    - CSV-Export: Spaltenreihenfolge, Trennzeichen, Kopfzeile
    - JSON-Export: Struktur, Paginierung, Metadaten
    - Excel-Export: Formatierungen, Blattstruktur
    - PDF-Export: Layout, Schriftarten, Wasserzeichen
    - Konfigurierbare Ausgabeoptionen (Felder, Filter, Sortierung)

    **Inhaltliche Tiefe:** Pro Format: vollständiges Beispiel der Ausgabe. JSON-Export mit Metadaten-Envelope (`{meta: {}, data: []}`). PDF-Optionen als Konfigurationstabelle.

    **Abgrenzung:** Keine Benutzer-Anleitung zum Export (→ manual/import-export.md), keine Eingabeformate (→ formats/input-formats.md), keine Berichtsformate (→ formats/report-formats.md)

    **Beispiel-Inhalte:** JSON-Ausgabe: `{"meta": {"total": 42, "page": 1}, "data": [{...}]}`; CSV-Header: `id;name;erstellt_am;status`


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
    **Zielgruppe:** Admins und DevOps-Ingenieure, die das System konfigurieren

    **Pflicht-Abschnitte:**

    - Konfigurationsdatei-Hierarchie (System → Umgebung → Benutzer)
    - YAML-Konfigurationsdatei: Struktur, Schlüssel, Datentypen
    - Umgebungsvariablen: Namenskonventionen, Priorität gegenüber Dateien
    - .env-Dateien: Format und Ladereihenfolge
    - Geheimnis-Management (Secrets, Tokens — nicht im Klartext)
    - Vollständige Referenztabelle aller Konfigurationsschlüssel

    **Inhaltliche Tiefe:** Jeder Schlüssel mit Typ, Standardwert, Beschreibung und Beispiel. Hierarchie als Diagramm. Umgebungsvariablen-Mapping-Tabelle.

    **Abgrenzung:** Keine Benutzer-Einstellungen (→ manual/settings.md), keine Deployment-Topologie (→ architecture/deployment-architecture.md)

    **Beispiel-Inhalte:** YAML: `database:\n  host: localhost\n  port: 5432\n  name: app_db`; Env-Mapping: `DATABASE_HOST=localhost` überschreibt `database.host`


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
    **Zielgruppe:** Backend-Entwickler und Datenbankadministratoren

    **Pflicht-Abschnitte:**

    - ER-Diagramm (Entity-Relationship) als Mermaid-Diagramm
    - Tabellenliste mit Beschreibung und Kardinalitäten
    - Spaltendefinitionen pro Tabelle (Name, Typ, Nullable, Default, Beschreibung)
    - Indizes und Constraints (Primary Key, Foreign Key, Unique)
    - Datenmigrations-Konventionen

    **Inhaltliche Tiefe:** Jede Tabelle vollständig dokumentiert. ER-Diagramm als Mermaid-Code eingebettet. Beziehungen mit Kardinalität (1:n, m:n).

    **Abgrenzung:** Keine Migrationsskripte (→ formats/migration-formats.md), keine DB-Architektur-Entscheidungen (→ architecture/database-architecture.md)

    **Beispiel-Inhalte:** Mermaid-ER-Diagramm mit 3 Tabellen; Tabelle `users`: `id SERIAL PK | email VARCHAR(255) UNIQUE NOT NULL | created_at TIMESTAMP DEFAULT NOW()`


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
    **Zielgruppe:** Entwickler, die Datenbank-Migrationen erstellen und ausführen

    **Pflicht-Abschnitte:**

    - Migrations-Framework (Alembic/Flyway/eigenes) und Konventionen
    - Dateinamens-Konvention (z.B. `V001__beschreibung.sql`)
    - Up- und Down-Migration: Struktur und Pflichtinhalte
    - Daten-Migrationen vs. Schema-Migrationen
    - Rollback-Strategien und Sicherheitshinweise

    **Inhaltliche Tiefe:** Vollständiges Beispiel einer Up/Down-Migration. Checkliste vor dem Einspielen einer Migration. Namensschema als Regex.

    **Abgrenzung:** Keine Schema-Dokumentation (→ formats/database-schema.md), keine Deployment-Pipeline (→ architecture/deployment-architecture.md)

    **Beispiel-Inhalte:** Up: `ALTER TABLE users ADD COLUMN phone VARCHAR(20);` Down: `ALTER TABLE users DROP COLUMN phone;` Dateiname: `V003__add_phone_to_users.sql`


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
    **Zielgruppe:** DevOps-Ingenieure und Entwickler, die Logs auswerten

    **Pflicht-Abschnitte:**

    - Strukturiertes Log-Format (JSON-Lines, Feldnamen, Datentypen)
    - Log-Level-Definitionen (DEBUG, INFO, WARN, ERROR, FATAL — wann welches?)
    - Pflichtfelder pro Log-Eintrag (Timestamp, Level, Message, Correlation-ID)
    - Kontextfelder (User-ID, Request-ID, Service-Name)
    - Rotation und Retention

    **Inhaltliche Tiefe:** Vollständiger JSON-Lines-Beispieleintrag. Log-Level-Entscheidungsbaum als Tabelle. Felder mit Typ und Beispielwert.

    **Abgrenzung:** Keine Logging-Architektur (→ architecture/logging-architecture.md), keine Monitoring-Dashboards (→ architecture/deployment-architecture.md)

    **Beispiel-Inhalte:** `{"ts":"2025-01-15T10:30:00Z","level":"ERROR","msg":"DB timeout","correlation_id":"abc-123","service":"api","duration_ms":5000}`


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
    **Zielgruppe:** Frontend- und Backend-Entwickler, die API-Integrationen bauen

    **Pflicht-Abschnitte:**

    - Request-Format: HTTP-Methoden, Header, Body-Struktur
    - Response-Format: Envelope-Struktur, Statusfelder, Paginierung
    - Fehler-Response: Fehlercode-Schema, Fehlerobjekt-Struktur
    - Authentifizierung: Token-Format, Header-Name
    - Versionierung der API (URL-Pfad, Header)
    - Rate-Limiting-Header und Retry-Logik

    **Inhaltliche Tiefe:** Vollständige Beispiele für Request und Response pro Endpunkt-Typ (CRUD). Fehlercode-Tabelle mit HTTP-Status, Code und Beschreibung.

    **Abgrenzung:** Keine Endpunkt-Liste (→ separate API-Referenz), keine Benutzer-Importanleitung (→ manual/import-export.md)

    **Beispiel-Inhalte:** Request: `POST /api/v1/items` mit JSON-Body; Response: `{"status":"ok","data":{...},"meta":{"request_id":"xyz"}}`; Fehler: `{"status":"error","code":"VALIDATION_FAILED","details":[...]}`


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
    **Zielgruppe:** Entwickler und Template-Designer, die Vorlagen erstellen

    **Pflicht-Abschnitte:**

    - Template-Engine und Syntax (z.B. Jinja2, Mustache)
    - Verfügbare Variablen und Kontextobjekte
    - Kontrollstrukturen (Schleifen, Bedingungen, Filter)
    - Template-Vererbung und Includes
    - Dateistruktur und Namenskonvention für Templates

    **Inhaltliche Tiefe:** Syntax-Referenz mit Beispielen für jeden Konstrukt-Typ. Variablen-Tabelle (Name → Typ → Beschreibung → Beispielwert). Vererbungs-Diagramm für Template-Hierarchie.

    **Abgrenzung:** Keine Endanwender-Vorlagen (→ manual/templates-usage.md), keine Berichtsvorlagen (→ formats/report-formats.md)

    **Beispiel-Inhalte:** `{% extends "base.html" %}{% block content %}{{ titel }}{% endblock %}`; Variable: `benutzer.name` (String) → «Max Mustermann»


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
    **Zielgruppe:** Plugin-Entwickler, die Erweiterungen für das System bauen

    **Pflicht-Abschnitte:**

    - Plugin-Manifest-Datei: Struktur, Pflichtfelder, Versionierung
    - Verzeichnisstruktur eines Plugins
    - Hook-Definitionen und Event-Bindings
    - Abhängigkeits-Deklaration
    - Paketierung und Verteilung (ZIP, Registry)

    **Inhaltliche Tiefe:** Vollständiges Manifest-Beispiel (JSON/YAML). Verzeichnisbaum als ASCII-Diagramm. Hook-Tabelle (Name → Parameter → Rückgabe → Zeitpunkt).

    **Abgrenzung:** Keine Plugin-Architektur (→ architecture/plugin-architecture.md), keine API-Formate (→ formats/api-formats.md)

    **Beispiel-Inhalte:** Manifest: `{"name":"my-plugin","version":"1.0.0","hooks":["before_save","after_delete"],"min_app_version":"3.0"}`; Verzeichnis: `my-plugin/├── manifest.json├── src/└── tests/`


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
    **Zielgruppe:** Admins und DevOps, die Backups erstellen und wiederherstellen

    **Pflicht-Abschnitte:**

    - Backup-Dateiformat: Struktur des Archivs (TAR/ZIP + Metadaten)
    - Enthaltene Daten: Datenbank-Dump, Dateien, Konfiguration
    - Metadaten-Datei im Backup (Version, Zeitstempel, Prüfsumme)
    - Inkrementelle vs. vollständige Backups
    - Wiederherstellungs-Prozess und Kompatibilitätsprüfung

    **Inhaltliche Tiefe:** Archivstruktur als Verzeichnisbaum. Metadaten-JSON vollständig dokumentiert. Kompatibilitätsmatrix (Backup-Version → App-Version).

    **Abgrenzung:** Keine Backup-Strategie (→ architecture/deployment-architecture.md), keine Datenmigration (→ formats/migration-formats.md)

    **Beispiel-Inhalte:** Archiv: `backup-2025-01-15.tar.gz` enthält `meta.json, db_dump.sql, files/, config/`; meta.json: `{"version":"2.1","created":"2025-01-15T02:00:00Z","checksum":"sha256:abc..."}`


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
    **Zielgruppe:** Integratoren und Entwickler, die Daten mit Drittsystemen austauschen

    **Pflicht-Abschnitte:**

    - Unterstützte Austauschformate (JSON, XML, CSV, Parquet, protobuf)
    - Daten-Envelope: Kopfdaten, Nutzdaten, Signaturen
    - Zeichencodierung, Escape-Regeln, Sonderzeichen
    - Schema-Validierung (JSON Schema, XSD)
    - Versionierung und Abwärtskompatibilität

    **Inhaltliche Tiefe:** Pro Format: vollständiges Austauschbeispiel mit Envelope. Schema-Dateien als Referenz verlinkt. Kompatibilitätsregeln als Checkliste.

    **Abgrenzung:** Keine API-Kommunikation (→ formats/api-formats.md), keine Import-Anleitung (→ manual/import-export.md)

    **Beispiel-Inhalte:** JSON-Envelope: `{"header":{"version":"1.0","sender":"erp","timestamp":"..."}, "payload":[...]}`; XSD-Auszug für Validierung


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
    **Zielgruppe:** Entwickler und Content-Manager, die Medien verarbeiten

    **Pflicht-Abschnitte:**

    - Unterstützte Bildformate (JPEG, PNG, WebP, SVG, GIF)
    - Maximale Abmessungen und Dateigrößen
    - Thumbnail-Generierung: Größen, Qualitätsstufen, Namenskonvention
    - Metadaten-Behandlung (EXIF, IPTC — Beibehaltung vs. Entfernung)
    - Video- und Audio-Formate (sofern unterstützt)

    **Inhaltliche Tiefe:** Format-Vergleichstabelle (Format → Transparenz → Animation → Kompression → Einsatzzweck). Thumbnail-Größen als Konfigurationstabelle.

    **Abgrenzung:** Keine Dateiverwaltung (→ manual/file-management.md), keine Ausgabeformat-Spezifikation (→ formats/output-formats.md)

    **Beispiel-Inhalte:** Tabelle: «JPEG → Nein → Nein → Verlustbehaftet → Fotos | PNG → Ja → Nein → Verlustfrei → Screenshots | SVG → Ja → Ja (SMIL) → Vektor → Icons»


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
    **Zielgruppe:** Entwickler und Report-Designer, die Berichtsvorlagen erstellen

    **Pflicht-Abschnitte:**

    - Berichts-Definitionsdatei: Struktur und Felder
    - Datenquellen-Konfiguration (Abfrage, Parameter, Filter)
    - Layout-Definition: Kopfzeile, Tabellen, Diagramme, Fußzeile
    - Ausgabeformate pro Bericht (PDF, Excel, HTML)
    - Platzhalter und Berechnungsfelder

    **Inhaltliche Tiefe:** Vollständige Berichts-Definitionsdatei als Beispiel. Platzhalter-Syntax und verfügbare Aggregationsfunktionen (SUM, AVG, COUNT).

    **Abgrenzung:** Keine Berichterstellung durch Endanwender (→ manual/reports.md), keine Template-Engine-Syntax (→ formats/template-formats.md)

    **Beispiel-Inhalte:** Definition: `{"title":"Monatsbericht","query":"SELECT ... WHERE monat={{param.monat}}","columns":[{"field":"name","label":"Name"},{"field":"summe","label":"Umsatz","format":"currency"}]}`


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
    **Zielgruppe:** Entwickler und Übersetzer, die Lokalisierung pflegen

    **Pflicht-Abschnitte:**

    - Übersetzungsdatei-Format (JSON, PO/POT, XLIFF)
    - Schlüssel-Namenskonvention (hierarchisch, z.B. `module.component.label`)
    - Pluralisierung und Geschlechterformen
    - Interpolation und Variablen in Übersetzungen
    - Fallback-Kette (z.B. de-AT → de → en)
    - Workflow: Neue Strings hinzufügen, übersetzen, prüfen

    **Inhaltliche Tiefe:** Pro Format: Beispieldatei mit 5 Einträgen inkl. Pluralisierung. Konventionen als strenge Regeln formulieren. Fallback-Kette als Diagramm.

    **Abgrenzung:** Keine UI-Spracheinstellungen (→ manual/settings.md), keine Template-Syntax (→ formats/template-formats.md)

    **Beispiel-Inhalte:** JSON: `{"user.greeting":"Hallo {{name}}","item.count_one":"{{count}} Element","item.count_other":"{{count}} Elemente"}`; PO: `msgid "Save" msgstr "Speichern"`


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
    **Zielgruppe:** Neue Entwickler, Architekten, technische Entscheider

    **Pflicht-Abschnitte:**

    - High-Level-Architekturdiagramm (C4 Level 1: System-Kontext)
    - Architekturstil (Monolith, Microservices, Modular Monolith)
    - Zentrale Designprinzipien (max. 5)
    - Externe Systeme und Abhängigkeiten
    - Querschnittsthemen (Sicherheit, Logging, Fehlerbehandlung — mit Verweisen)

    **Inhaltliche Tiefe:** Mermaid-Diagramm auf C4-Level 1. Jedes Designprinzip mit Begründung und Konsequenz. Externe Systeme als Tabelle (System → Schnittstelle → Datenrichtung).

    **Abgrenzung:** Keine Komponenten-Details (→ architecture/components.md), keine Technologie-Entscheidungen (→ architecture/tech-stack.md, architecture/decisions.md)

    **Beispiel-Inhalte:** C4-Kontextdiagramm mit Benutzer, System, E-Mail-Server, Dritt-API; Prinzip: «Separation of Concerns — Jede Schicht hat genau eine Verantwortung»


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
    **Zielgruppe:** Entwickler, die die Systemstruktur verstehen müssen

    **Pflicht-Abschnitte:**

    - Komponentendiagramm (C4 Level 2: Container-Diagramm)
    - Komponentenliste (Name → Verantwortung → Technologie → Repository/Pfad)
    - Abhängigkeiten zwischen Komponenten (Dependency-Graph)
    - Schnittstellen der Komponenten (bereitgestellte und benötigte)
    - Eigentumsmodell (welches Team besitzt welche Komponente)

    **Inhaltliche Tiefe:** Mermaid-Diagramm auf C4-Level 2. Pro Komponente: 2-3 Sätze Beschreibung, Technologie-Stack, Schnittstellen. Abhängigkeitsmatrix als Tabelle.

    **Abgrenzung:** Kein High-Level-Überblick (→ architecture/overview.md), keine Code-Level-Details, keine Deployment-Sicht (→ architecture/deployment-architecture.md)

    **Beispiel-Inhalte:** Container-Diagramm: Web-App → API-Gateway → Backend-Service → Datenbank; Tabelle: «Auth-Service → Authentifizierung und Autorisierung → Go → /services/auth»


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
    **Zielgruppe:** Entwickler und Architekten, die den Datenfluss nachvollziehen müssen

    **Pflicht-Abschnitte:**

    - Datenflussdiagramm (Sequenz- oder Flussdiagramm)
    - Haupt-Datenströme: Benutzer-Request, Batch-Verarbeitung, Event-Verarbeitung
    - Datentransformation an jeder Station (Eingabe → Verarbeitung → Ausgabe)
    - Datenvalidierung und -anreicherung
    - Datensenken und -quellen (extern und intern)

    **Inhaltliche Tiefe:** Mindestens 3 Hauptflüsse als Sequenzdiagramme (Mermaid). Pro Fluss: beteiligte Komponenten, Datenformat an jeder Schnittstelle, Fehlerfluss.

    **Abgrenzung:** Keine Komponentenbeschreibung (→ architecture/components.md), keine DB-Schema-Details (→ formats/database-schema.md), keine Caching-Details (→ architecture/caching.md)

    **Beispiel-Inhalte:** Sequenzdiagramm: Browser → API-Gateway → Auth → Service → DB → Response; Annotation: «Validierung in Service-Layer, Enrichment mit User-Kontext»


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
    **Zielgruppe:** Architekten und Tech-Leads, die Entscheidungen nachvollziehen wollen

    **Pflicht-Abschnitte:**

    - ADR-Format-Erklärung (Architecture Decision Records)
    - ADR-Index (Tabelle: Nummer → Titel → Status → Datum)
    - Pro ADR: Kontext, Entscheidung, Konsequenzen, Status
    - Abgelöste/veraltete Entscheidungen kennzeichnen

    **Inhaltliche Tiefe:** ADR-Template mit allen Feldern. Mindestens 3 Beispiel-ADRs (z.B. Datenbankwahl, API-Stil, Auth-Strategie). Status-Werte: Vorgeschlagen, Akzeptiert, Veraltet, Abgelöst.

    **Abgrenzung:** Keine Implementierungsdetails (→ architecture/components.md), keine Tech-Stack-Auflistung (→ architecture/tech-stack.md)

    **Beispiel-Inhalte:** ADR-001: «PostgreSQL als primäre Datenbank — Kontext: Bedarf an JSONB-Unterstützung und starke Konsistenz — Entscheidung: PostgreSQL 15 — Konsequenz: Kein nativer Volltext-Suchindex → ElasticSearch ergänzen»


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
    **Zielgruppe:** Neue Entwickler, Architekten, Management

    **Pflicht-Abschnitte:**

    - Technologie-Stack-Übersicht als Schichtdiagramm (Frontend → Backend → Datenbank → Infrastruktur)
    - Pro Technologie: Name, Version, Einsatzzweck, Lizenz
    - Programmiersprachen und Frameworks
    - Externe Services und SaaS-Abhängigkeiten
    - Entwicklungs-Tooling (IDE, Linter, Formatter, CI/CD)

    **Inhaltliche Tiefe:** Vollständige Tabelle aller Technologien mit Versionspinning. Begründung für jede Haupttechnologie (Kurzform, Verweis auf ADR für Details).

    **Abgrenzung:** Keine Architekturbegründungen (→ architecture/decisions.md), keine Deployment-Konfiguration (→ architecture/deployment-architecture.md)

    **Beispiel-Inhalte:** Tabelle: «Python 3.11 → Backend-Logik → MIT | React 18 → Frontend-UI → MIT | PostgreSQL 15 → Datenbank → PostgreSQL License»; Schichtdiagramm als Mermaid-Block


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
    **Zielgruppe:** Security-Engineers, Architekten, Auditoren

    **Pflicht-Abschnitte:**

    - Sicherheitsmodell im Überblick (Defense in Depth, Zero Trust)
    - Authentifizierung: Verfahren, Token-Handling, Session-Management
    - Autorisierung: RBAC/ABAC-Modell, Berechtigungsregeln
    - Datenverschlüsselung: at rest, in transit, Schlüsselmanagement
    - Eingabevalidierung und Output-Encoding (XSS, SQLi, CSRF)
    - Sicherheitsrelevante Header und CORS-Konfiguration
    - Schwachstellen-Management und Dependency-Scanning

    **Inhaltliche Tiefe:** RBAC-Matrix vollständig abbilden. Verschlüsselungsalgorithmen mit Schlüssellänge angeben. OWASP Top 10 als Checkliste mit Maßnahmen.

    **Abgrenzung:** Keine Benutzerrollen-Verwaltung (→ manual/multi-user.md), keine Config-Secrets (→ formats/config-files.md)

    **Beispiel-Inhalte:** Auth-Flow als Sequenzdiagramm (Login → Token → Refresh); RBAC-Matrix: «Rolle admin → /api/users: CRUD | Rolle viewer → /api/users: R»; Encryption: AES-256-GCM at rest, TLS 1.3 in transit


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
    **Zielgruppe:** Architekten, DevOps-Ingenieure, technische Entscheider

    **Pflicht-Abschnitte:**

    - Skalierungsstrategie (horizontal vs. vertikal)
    - Stateless-Design und Session-Management
    - Datenbank-Skalierung (Read-Replicas, Sharding, Connection-Pooling)
    - Lastverteilung (Load Balancer, Health Checks)
    - Performance-Kennzahlen und SLOs (Latenz, Throughput)
    - Bottleneck-Analyse und Kapazitätsplanung

    **Inhaltliche Tiefe:** Skalierungsdiagramm für 10x/100x Last. SLO-Tabelle (Metrik → Zielwert → Messmethode). Bottleneck-Analyse als Flowchart.

    **Abgrenzung:** Keine Caching-Details (→ architecture/caching.md), keine Queue-Architektur (→ architecture/queue-architecture.md), keine Deployment-Topologie (→ architecture/deployment-architecture.md)

    **Beispiel-Inhalte:** Diagramm: 1 Server → 3 Server + LB → DB-Replikat; SLO: «P95 Latenz < 200ms bei 1000 req/s»; Bottleneck: «DB-Verbindungslimit bei >500 concurrent»


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
    **Zielgruppe:** Backend-Entwickler, die einheitliche Fehlerbehandlung implementieren

    **Pflicht-Abschnitte:**

    - Fehlerbehandlungs-Strategie und Grundsätze
    - Fehler-Hierarchie (Exception-Klassen, Fehlertypen)
    - Fehler-Propagation durch die Schichten (Service → Controller → Client)
    - Fehler-Response-Format (→ Verweis auf formats/api-formats.md)
    - Retry-Strategien und Circuit-Breaker
    - Fehler-Logging und -Monitoring (Korrelation mit Request-ID)

    **Inhaltliche Tiefe:** Exception-Hierarchie als Baumdiagramm. Pro Fehlertyp: HTTP-Status, interner Code, Logging-Level, Benutzer-Nachricht. Retry-Konfiguration als Tabelle (Fehlertyp → Max-Retries → Backoff).

    **Abgrenzung:** Keine Log-Formate (→ formats/log-formats.md), keine API-Fehlerresponse-Spezifikation (→ formats/api-formats.md)

    **Beispiel-Inhalte:** Hierarchie: `AppError → ValidationError, NotFoundError, AuthError`; Mapping: `NotFoundError → 404 → ERR_NOT_FOUND → ERROR-Level → ‹Ressource nicht gefunden›`


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
    **Zielgruppe:** Backend-Entwickler und Performance-Engineers

    **Pflicht-Abschnitte:**

    - Caching-Strategie: Welche Daten werden gecacht (und welche nicht)
    - Cache-Schichten (Browser-Cache, CDN, Application-Cache, DB-Cache)
    - Cache-Invalidierung: Strategien (TTL, Event-basiert, manuell)
    - Cache-Schlüssel-Design und Namenskonventionen
    - Technologie (Redis, Memcached, In-Memory) und Konfiguration
    - Monitoring: Cache-Hit-Rate, Speicherverbrauch

    **Inhaltliche Tiefe:** Cache-Schichten als Diagramm. Entscheidungstabelle: Datentyp → Cachebar? → TTL → Invalidierungs-Trigger. Schlüssel-Beispiele: `user:{id}:profile`, `query:{hash}`.

    **Abgrenzung:** Keine Performance-Skalierung (→ architecture/scalability.md), keine Datenfluss-Details (→ architecture/data-flow.md)

    **Beispiel-Inhalte:** Schichten: Browser (Cache-Control) → CDN (Varnish) → Redis → PostgreSQL; Entscheidung: «Benutzerprofil → Ja → TTL 5min → Invalidierung bei PUT /users/{id}»


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
    **Zielgruppe:** Backend-Entwickler, die Events publizieren oder konsumieren

    **Pflicht-Abschnitte:**

    - Event-Driven-Architektur: Grundprinzipien und Einsatzzweck
    - Event-Typen und Namenskonventionen (Domain-Events, Integration-Events)
    - Event-Schema: Pflichtfelder (event_type, timestamp, source, payload)
    - Event-Bus/Broker: Technologie und Konfiguration
    - Event-Handler: Registrierung, Reihenfolge, Fehlerbehandlung
    - Idempotenz und Exactly-Once-Semantik

    **Inhaltliche Tiefe:** Event-Katalog als Tabelle (Event → Auslöser → Payload-Felder → Konsumenten). Vollständiges Event-JSON-Beispiel. Idempotenz-Strategien erklären.

    **Abgrenzung:** Keine Queue-Infrastruktur (→ architecture/queue-architecture.md), keine Benachrichtigungen (→ manual/notifications.md)

    **Beispiel-Inhalte:** Event: `{"type":"user.created","ts":"...","source":"auth-service","payload":{"user_id":123,"email":"..."}}`; Katalog: «user.created → Registrierung → E-Mail-Service, Analytics-Service»


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
    **Zielgruppe:** DevOps-Ingenieure und Systemadministratoren

    **Pflicht-Abschnitte:**

    - Deployment-Topologie (Diagramm: Server, Container, Netzwerk-Zonen)
    - Umgebungen: Entwicklung, Staging, Produktion (Vergleichstabelle)
    - Container-Orchestrierung (Docker Compose, Kubernetes)
    - CI/CD-Pipeline: Stufen, Gates, Rollback
    - Netzwerk-Architektur (VPC, Subnetze, Firewalls, Reverse-Proxy)
    - Monitoring und Alerting (Prometheus, Grafana, PagerDuty)

    **Inhaltliche Tiefe:** Deployment-Diagramm als Mermaid. CI/CD-Pipeline als Stufendiagramm (Build → Test → Deploy → Smoke-Test). Umgebungs-Matrix (Umgebung → Server → Replicas → Ressourcen).

    **Abgrenzung:** Keine Anwendungs-Architektur (→ architecture/overview.md), keine Konfigurationsdateien (→ formats/config-files.md)

    **Beispiel-Inhalte:** Topologie: Internet → Load Balancer → 3x App-Container → DB-Primary + Read-Replica; Pipeline: «GitHub Push → Lint → Unit-Tests → Build Image → Deploy Staging → Integration-Tests → Deploy Prod»


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
    **Zielgruppe:** Entwickler und QA-Engineers, die Tests schreiben und pflegen

    **Pflicht-Abschnitte:**

    - Teststrategie und Testpyramide (Unit → Integration → E2E)
    - Test-Frameworks und -Tools pro Schicht
    - Testdaten-Management (Fixtures, Factories, Faker)
    - Mocking-Strategie (externe Services, Datenbank)
    - Code-Coverage-Ziele und -Messung
    - CI-Integration: Wann welche Tests laufen

    **Inhaltliche Tiefe:** Testpyramide als Diagramm mit prozentualer Verteilung. Pro Test-Schicht: Framework, Ausführungszeit, Beispiel. Coverage-Tabelle (Modul → Ist → Soll).

    **Abgrenzung:** Keine Deployment-Pipeline (→ architecture/deployment-architecture.md), keine Fehlerbehandlungs-Tests (→ architecture/error-handling.md)

    **Beispiel-Inhalte:** Pyramide: «Unit 70% (pytest, <1s) | Integration 20% (testcontainers, <30s) | E2E 10% (Playwright, <2min)»; Fixture: `@pytest.fixture def sample_user(): return User(name="Test")`


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
    **Zielgruppe:** Entwickler und DevOps, die das Logging-System implementieren oder nutzen

    **Pflicht-Abschnitte:**

    - Logging-Architektur: Übersicht (Applikation → Aggregator → Speicher → Dashboard)
    - Strukturiertes Logging: Warum und wie
    - Correlation-ID-Propagation über Service-Grenzen
    - Log-Aggregation (ELK, Loki, CloudWatch)
    - Log-Retention und -Rotation
    - Sensitive Daten in Logs vermeiden (PII-Filterung)

    **Inhaltliche Tiefe:** Architektur-Diagramm der Log-Pipeline. Correlation-ID-Propagation als Sequenzdiagramm. PII-Filter-Regeln als Tabelle.

    **Abgrenzung:** Keine Log-Format-Spezifikation (→ formats/log-formats.md), keine Monitoring-Infrastruktur (→ architecture/deployment-architecture.md)

    **Beispiel-Inhalte:** Pipeline: App → Filebeat → Elasticsearch → Kibana; Correlation: «Request-Header X-Correlation-ID → in jedem Log-Eintrag → bis zum DB-Query»; PII-Filter: «Feld ‹email› → maskiert als ‹m***@x.de›»


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
    **Zielgruppe:** Plugin-Entwickler und Core-Architekten

    **Pflicht-Abschnitte:**

    - Plugin-System-Architektur: Host-App, Plugin-API, Sandbox
    - Lifecycle: Laden, Initialisieren, Aktivieren, Deaktivieren, Entfernen
    - Extension Points: Wo können Plugins einhaken (Hook-Katalog)
    - Sicherheitsmodell: Berechtigungen, Sandbox-Grenzen
    - Versioning und Kompatibilität (SemVer, Min/Max-App-Version)
    - Plugin-Registry und Verteilung

    **Inhaltliche Tiefe:** Lifecycle als Zustandsdiagramm (Mermaid). Hook-Katalog als vollständige Tabelle. Sandbox-Regeln als Checkliste.

    **Abgrenzung:** Keine Plugin-Manifest-Formate (→ formats/plugin-formats.md), keine Event-Architektur (→ architecture/event-system.md)

    **Beispiel-Inhalte:** Lifecycle: `Discovered → Loaded → Initialized → Active → Disabled → Unloaded`; Hook: «before_save(entity) → kann Validierung hinzufügen oder abbrechen»; Sandbox: «Kein Zugriff auf Dateisystem, nur zugewiesene API-Endpunkte»


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
    **Zielgruppe:** Backend-Entwickler, die asynchrone Verarbeitung implementieren

    **Pflicht-Abschnitte:**

    - Einsatzzweck asynchroner Verarbeitung (Wann Queue statt synchron?)
    - Queue-Technologie (RabbitMQ, Redis Streams, Celery, SQS)
    - Queue-Topologie: Exchanges, Queues, Routing-Keys
    - Worker-Architektur: Concurrency, Prefetch, Acknowledge
    - Dead-Letter-Queue und Fehlerbehandlung
    - Monitoring: Queue-Länge, Consumer-Lag, Verarbeitungszeit

    **Inhaltliche Tiefe:** Topologie-Diagramm (Mermaid). Pro Queue: Name, Routing-Key, Consumer, Retry-Policy, DLQ. Worker-Konfiguration als Code-Beispiel.

    **Abgrenzung:** Keine Event-Architektur (→ architecture/event-system.md), keine Skalierung (→ architecture/scalability.md)

    **Beispiel-Inhalte:** Topologie: Producer → Exchange (topic) → Queue «email-send» → Worker; DLQ: «Nach 3 Retries mit exponentiellem Backoff → dead-letter-email-send»; Worker: `@celery.task(max_retries=3, default_retry_delay=60)`


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
    **Zielgruppe:** Backend-Entwickler und Datenbankadministratoren

    **Pflicht-Abschnitte:**

    - Datenbank-Technologien im Einsatz (relational, NoSQL, Suchindex)
    - Datenbank-Topologie (Primary, Replicas, Shards)
    - Connection-Management (Pooling, Connection-Limits)
    - ORM/Query-Builder-Strategie und Konventionen
    - Backup- und Recovery-Strategie
    - Performance-Optimierung (Indizes, Query-Analyse, EXPLAIN)

    **Inhaltliche Tiefe:** Topologie-Diagramm (Primary → Replicas → Failover). Connection-Pool-Konfiguration als Tabelle. Index-Strategie: Wann welcher Index-Typ (B-Tree, GIN, GiST).

    **Abgrenzung:** Kein DB-Schema (→ formats/database-schema.md), keine Migrationen (→ formats/migration-formats.md), keine Skalierung (→ architecture/scalability.md)

    **Beispiel-Inhalte:** Topologie: «PostgreSQL Primary (Write) → 2 Read-Replicas (async) → Redis (Session-Cache) → Elasticsearch (Volltextsuche)»; Pool: «min=5, max=20, idle_timeout=300s, max_lifetime=1800s»; Index: «B-Tree auf FK-Spalten, GIN auf JSONB-Felder»


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
    **Zielgruppe:** Backend-Entwickler, Frontend-Entwickler, externe API-Konsumenten

    **Pflicht-Abschnitte:**

    - Base-URL und Umgebungen (Production, Staging, Development)
    - Versionierungsschema (URL-Pfad vs. Header)
    - Allgemeine Konventionen (JSON, UTC-Zeitstempel, Pagination, Sortierung)
    - Content-Type und Accept-Header
    - Authentifizierungs-Kurzübersicht mit Verweis auf Detailseite
    - Schnellstart-Beispiel (ein vollständiger Request/Response-Zyklus)

    **Inhaltliche Tiefe:** Kompakte Übersicht, die in 5 Minuten lesbar ist. Jede Konvention mit kurzem Code-Beispiel belegen. Tabelle für Umgebungs-URLs.

    **Abgrenzung:** Keine vollständigen Endpunkt-Beschreibungen (→ api/endpoints.md), keine Auth-Details (→ api/authentication.md), kein Changelog (→ api/api-changelog.md).

    **Beispiel-Inhalte:** Tabelle mit Base-URLs pro Umgebung, cURL-Beispiel für einen GET-Request mit API-Key-Header, JSON-Response-Beispiel mit Pagination-Metadaten.

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
    **Zielgruppe:** Entwickler, die konkrete API-Aufrufe implementieren

    **Pflicht-Abschnitte:**

    - Endpunkt-Übersichtstabelle (Method, Path, Kurzbeschreibung)
    - Detailbeschreibung pro Endpunkt: HTTP-Methode, Pfad, Path-/Query-/Body-Parameter
    - Request-Beispiel (cURL oder HTTP-Raw)
    - Response-Beispiel (JSON mit Statuscodes)
    - Fehler-Responses pro Endpunkt
    - Paginierung und Filter-Optionen

    **Inhaltliche Tiefe:** Vollständige Referenz. Jeder Parameter mit Typ, Required-Flag, Default-Wert und Beschreibung. Mindestens ein Request/Response-Paar pro Endpunkt.

    **Abgrenzung:** Keine Erklärung der Datenmodelle (→ api/models.md), keine Fehlercode-Gesamtliste (→ api/errors.md), keine Auth-Flows (→ api/authentication.md).

    **Beispiel-Inhalte:** `GET /api/v1/users?page=1&limit=20` mit vollständiger Parametertabelle, cURL-Beispiel, JSON-Response mit 200 und 404-Fehlerfall.

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
    **Zielgruppe:** Entwickler, die Request-/Response-Objekte parsen oder generieren

    **Pflicht-Abschnitte:**

    - Übersicht aller Datenmodelle (Tabelle: Name, Beschreibung, verwendet in)
    - Detailschema pro Modell: Feldname, Typ, Required, Beschreibung, Constraints
    - Verschachtelte Objekte und Referenzen zwischen Modellen
    - Enumerations und erlaubte Werte
    - Nullable-Felder und Defaults

    **Inhaltliche Tiefe:** Vollständige Schema-Dokumentation. JSON-Schema-Notation oder Tabellen mit allen Feldern. Beispiel-JSON pro Modell.

    **Abgrenzung:** Keine Endpunkt-Logik (→ api/endpoints.md), keine Datenbank-Schemas (→ development/database-guide.md).

    **Beispiel-Inhalte:** Modell `User` mit Feldern id (integer, required), email (string, required, format: email), role (enum: admin|user|viewer), created_at (string, ISO 8601). Dazu ein vollständiges JSON-Beispiel.

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
    **Zielgruppe:** Entwickler, die API-Zugriff absichern oder konsumieren

    **Pflicht-Abschnitte:**

    - Unterstützte Auth-Methoden (API-Key, Bearer Token, OAuth2)
    - Token-Erstellung und -Erneuerung (Schritt-für-Schritt)
    - Token-Lebensdauer und Refresh-Flow
    - Header-Format und Beispiele
    - Berechtigungen und Scopes
    - Fehler bei ungültiger Authentifizierung (401, 403)

    **Inhaltliche Tiefe:** Vollständige Anleitung mit Sequenzdiagramm für OAuth2-Flow. Jede Auth-Methode mit konkretem cURL-Beispiel. Tabelle der Scopes.

    **Abgrenzung:** Keine SSO-Konfiguration (→ integrations/sso.md), keine Endpunkt-Details (→ api/endpoints.md).

    **Beispiel-Inhalte:** cURL mit Bearer-Token-Header, OAuth2 Authorization-Code-Flow-Diagramm, Tabelle: Scope `read:users` → erlaubt GET /users.

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
    **Zielgruppe:** Entwickler, die Fehlerbehandlung implementieren

    **Pflicht-Abschnitte:**

    - HTTP-Statuscodes und ihre Bedeutung im API-Kontext
    - Fehler-Response-Format (JSON-Struktur)
    - Anwendungsspezifische Fehlercodes (Tabelle: Code, Bedeutung, Lösung)
    - Validierungsfehler-Format (Feld-Level-Fehler)
    - Retry-Strategien pro Fehlertyp

    **Inhaltliche Tiefe:** Jeder Fehlercode mit Beschreibung, möglicher Ursache und empfohlener Lösung. JSON-Beispiel pro Fehlerkategorie.

    **Abgrenzung:** Keine Endpunkt-spezifischen Fehler (→ api/endpoints.md), keine Rate-Limit-Details (→ api/rate-limiting.md).

    **Beispiel-Inhalte:** JSON `{"error": {"code": "VALIDATION_ERROR", "message": "...", "details": [{"field": "email", "reason": "invalid_format"}]}}`, Tabelle mit 400/401/403/404/409/422/429/500 und jeweiliger Handlungsempfehlung.

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
    **Zielgruppe:** Entwickler und Ops-Teams, die API-Nutzung planen

    **Pflicht-Abschnitte:**

    - Rate-Limit-Regeln (Requests pro Zeitfenster, pro Endpunkt/global)
    - Response-Header (X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset)
    - Verhalten bei Überschreitung (429-Response, Retry-After)
    - Quotas für verschiedene API-Tiers/Pläne
    - Best Practices: Backoff-Strategien, Request-Bündelung

    **Inhaltliche Tiefe:** Konkrete Zahlen pro Tier. Code-Beispiel für exponentiellen Backoff. Tabelle mit allen Rate-Limit-Headern.

    **Abgrenzung:** Keine allgemeine Fehlerbehandlung (→ api/errors.md), keine Batch-Optimierung (→ api/batch-operations.md).

    **Beispiel-Inhalte:** Tabelle: Free-Tier 100 req/min, Pro 1000 req/min. Python-Beispiel mit `time.sleep()` und Retry-Logik. Header-Beispiel: `X-RateLimit-Remaining: 42`.

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
    **Zielgruppe:** Entwickler, die auf API-Events reagieren möchten

    **Pflicht-Abschnitte:**

    - Verfügbare Event-Typen (Tabelle: Event, Beschreibung, Payload)
    - Webhook-Registrierung (API-Endpunkt oder UI)
    - Payload-Format und Signatur-Verifizierung (HMAC)
    - Retry-Verhalten bei fehlgeschlagener Zustellung
    - Best Practices: Idempotenz, Timeout-Handling
    - Webhook-Debugging und Logs

    **Inhaltliche Tiefe:** Vollständiges Payload-Beispiel pro Event-Typ. Code-Beispiel für HMAC-Verifizierung in Python und Node.js.

    **Abgrenzung:** Keine Integration in externe Systeme (→ integrations/webhooks.md), keine WebSocket-Echtzeit-Events (→ api/websockets.md).

    **Beispiel-Inhalte:** Event `user.created` mit JSON-Payload, Python-Code für `hmac.compare_digest()`, Sequenzdiagramm: API → Webhook-Endpoint → Bestätigung.

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
    **Zielgruppe:** API-Konsumenten und API-Maintainer

    **Pflicht-Abschnitte:**

    - Versionierungsstrategie (URL-Pfad, Header, Query-Parameter)
    - Semantic Versioning und Breaking-Change-Definition
    - Deprecation-Policy (Zeiträume, Kommunikation)
    - Migration zwischen Versionen (Leitfaden)
    - Sunset-Header und -Prozess

    **Inhaltliche Tiefe:** Klare Regeln, was als Breaking Change gilt. Timeline-Beispiel für Deprecation. Konkrete Migrations-Checkliste.

    **Abgrenzung:** Kein Changelog (→ api/api-changelog.md), keine Endpunkt-Details (→ api/endpoints.md).

    **Beispiel-Inhalte:** Tabelle: v1 (stable), v2 (current), v3 (beta). Beispiel: `Accept: application/vnd.api.v2+json`. Deprecation-Timeline: Ankündigung → 6 Monate → Sunset.

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
    **Zielgruppe:** Entwickler, die offizielle Client-Bibliotheken nutzen

    **Pflicht-Abschnitte:**

    - Verfügbare SDKs (Sprache, Version, Repository-Link)
    - Installation pro SDK (pip, npm, gem etc.)
    - Schnellstart-Beispiel pro SDK
    - Konfiguration (Base-URL, Auth, Timeouts)
    - Fehlerbehandlung im SDK
    - Community-SDKs (nicht offiziell unterstützt)

    **Inhaltliche Tiefe:** Mindestens ein vollständiges Beispiel pro SDK (Initialisierung, API-Aufruf, Fehlerbehandlung). Versionskompatibilitäts-Matrix.

    **Abgrenzung:** Keine rohen HTTP-Beispiele (→ api/examples.md), keine API-Referenz (→ api/endpoints.md).

    **Beispiel-Inhalte:** Python: `pip install myapi-sdk`, `client = MyAPI(api_key='...')`, `users = client.users.list()`. Tabelle: Python 3.8+, Node.js 16+, Go 1.19+.

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
    **Zielgruppe:** Entwickler aller Erfahrungsstufen, die schnell starten wollen

    **Pflicht-Abschnitte:**

    - cURL-Beispiele (CRUD-Operationen)
    - Python-Beispiele (requests-Bibliothek)
    - JavaScript-Beispiele (fetch/axios)
    - Häufige Workflows (z. B. Datei hochladen, Pagination durchlaufen)
    - Fehlerbehandlungs-Beispiele
    - Copy-Paste-fähige Code-Blöcke

    **Inhaltliche Tiefe:** Jedes Beispiel vollständig lauffähig. Kommentare im Code erklären jeden Schritt. Mindestens 3 Sprachen.

    **Abgrenzung:** Keine SDK-spezifischen Beispiele (→ api/sdks.md), keine Endpunkt-Referenz (→ api/endpoints.md).

    **Beispiel-Inhalte:** cURL: `curl -H 'Authorization: Bearer TOKEN' https://api.example.com/v1/users`, Python: vollständiges Skript mit Error-Handling, JS: async/await fetch-Beispiel.

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
    **Zielgruppe:** Entwickler, die den GraphQL-Endpunkt nutzen

    **Pflicht-Abschnitte:**

    - GraphQL-Endpunkt-URL und Playground/Explorer
    - Schema-Übersicht (Types, Queries, Mutations, Subscriptions)
    - Authentifizierung für GraphQL-Requests
    - Query-Beispiele mit Variablen
    - Mutation-Beispiele
    - Fehlerbehandlung im GraphQL-Kontext
    - Pagination (Cursor-basiert, Relay-Style)
    - Rate-Limiting und Query-Komplexität

    **Inhaltliche Tiefe:** Vollständige Type-Definitionen. Mindestens 5 Query-Beispiele mit Variablen und Response.

    **Abgrenzung:** Keine REST-Endpunkte (→ api/endpoints.md), keine allgemeine Auth-Doku (→ api/authentication.md).

    **Beispiel-Inhalte:** Query `{ users(first: 10) { edges { node { id name } } } }`, Mutation `createUser(input: {...})`, Fehler-Response mit `errors`-Array und `extensions`.

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
    **Zielgruppe:** Entwickler, die Echtzeit-Kommunikation implementieren

    **Pflicht-Abschnitte:**

    - WebSocket-Endpunkt-URL und Verbindungsaufbau
    - Authentifizierung (Token im Query-String oder erste Nachricht)
    - Nachrichtenformate (JSON-Struktur pro Event-Typ)
    - Verfügbare Channels/Topics und Subscription-Mechanismus
    - Heartbeat/Ping-Pong und Reconnect-Strategien
    - Beispiel-Implementierungen (Python, JS)

    **Inhaltliche Tiefe:** Vollständiger Connection-Lifecycle mit Sequenzdiagramm. Code-Beispiel für Verbindung, Subscription und Nachrichtenverarbeitung.

    **Abgrenzung:** Keine Webhook-Konfiguration (→ api/webhooks.md), keine REST-Endpunkte (→ api/endpoints.md).

    **Beispiel-Inhalte:** JS: `new WebSocket('wss://api.example.com/ws?token=...')`, Nachrichtenformat `{"type": "subscribe", "channel": "updates"}`, Reconnect-Code mit exponential Backoff.

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
    **Zielgruppe:** Entwickler, die Massen-Operationen effizient durchführen

    **Pflicht-Abschnitte:**

    - Batch-Endpunkt und Request-Format
    - Maximale Batch-Größe und Limits
    - Atomarität (alles-oder-nichts vs. partial success)
    - Response-Format (Status pro Operation)
    - Asynchrone Batch-Jobs (Job-ID, Polling, Callback)
    - Fehlerbehandlung bei Teil-Fehlschlägen

    **Inhaltliche Tiefe:** Vollständiges Request/Response-Beispiel. Entscheidungsbaum: wann Batch vs. Einzel-Requests.

    **Abgrenzung:** Keine Einzelendpunkte (→ api/endpoints.md), keine Rate-Limits (→ api/rate-limiting.md).

    **Beispiel-Inhalte:** POST `/api/v1/batch` mit Body `{"operations": [{"method": "POST", "path": "/users", "body": {...}}, ...]}`, Response mit `results`-Array und Status pro Operation.

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
    **Zielgruppe:** Alle API-Konsumenten, Release-Manager

    **Pflicht-Abschnitte:**

    - Änderungshistorie (chronologisch, neueste zuerst)
    - Pro Eintrag: Datum, Version, Art der Änderung, betroffene Endpunkte
    - Breaking Changes hervorgehoben (Warnung/Admonition)
    - Deprecation-Hinweise mit Sunset-Datum
    - Migrationstipps für Breaking Changes

    **Inhaltliche Tiefe:** Jeder Eintrag klar kategorisiert (Added, Changed, Deprecated, Removed, Fixed). Kurzbeschreibung plus Link zur Detaildoku.

    **Abgrenzung:** Keine Versionierungs-Strategie (→ api/versioning.md), keine vollständigen Endpunkt-Beschreibungen (→ api/endpoints.md).

    **Beispiel-Inhalte:** `## 2024-03-15 — v2.3.0`, `### Added`, `- POST /api/v1/exports — Neuer Export-Endpunkt`, `### Breaking`, `- ⚠️ Field 'name' in User-Modell umbenannt zu 'display_name'`.

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
    **Zielgruppe:** Entwickler, die Datei-Uploads implementieren

    **Pflicht-Abschnitte:**

    - Upload-Endpunkt und HTTP-Methode
    - Multipart/form-data-Format
    - Erlaubte Dateitypen und Größenlimits
    - Chunked Upload für große Dateien
    - Upload-Fortschritt und Resumable Uploads
    - Datei-Metadaten und Response-Format
    - Virenscanning und Validierung

    **Inhaltliche Tiefe:** Vollständige cURL- und Python-Beispiele. Sequenzdiagramm für Chunked Upload.

    **Abgrenzung:** Keine Speicher-Konfiguration (→ integrations/storage.md), keine allgemeine Endpunkt-Referenz (→ api/endpoints.md).

    **Beispiel-Inhalte:** cURL: `curl -F 'file=@report.pdf' -F 'folder_id=123' ...`, Tabelle: max 100 MB, erlaubt: pdf/png/jpg/xlsx, Chunked-Upload-Sequenz: initiate → upload parts → complete.

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
    **Zielgruppe:** Entwickler, die Suchfunktionalität integrieren

    **Pflicht-Abschnitte:**

    - Such-Endpunkt und Query-Syntax
    - Suchbare Felder und Filter-Optionen
    - Volltextsuche vs. strukturierte Suche
    - Sortierung und Relevanz-Scoring
    - Facetten und Aggregationen
    - Pagination der Suchergebnisse
    - Suchvorschläge (Autocomplete)

    **Inhaltliche Tiefe:** Query-Syntax vollständig dokumentiert. Mindestens 5 Suchbeispiele mit Filtern. Response-Format mit Score.

    **Abgrenzung:** Keine Suchmaschinen-Konfiguration (→ integrations/search-engine.md), keine allgemeine API-Referenz (→ api/endpoints.md).

    **Beispiel-Inhalte:** `GET /api/v1/search?q=report&type=document&date_from=2024-01-01`, Response mit `hits`, `total_count`, `facets`. Autocomplete: `GET /api/v1/search/suggest?q=rep`.

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
    **Zielgruppe:** Systemadministratoren und DevOps-Ingenieure

    **Pflicht-Abschnitte:**

    - Admin-Endpunkte-Übersicht (nur mit Admin-Rechten zugänglich)
    - Benutzerverwaltung (CRUD, Rollen zuweisen)
    - Systemkonfiguration über API
    - Audit-Log-Abfragen
    - Lizenz- und Quota-Verwaltung
    - Sicherheitshinweise für Admin-Endpoints

    **Inhaltliche Tiefe:** Jeder Admin-Endpunkt mit Berechtigungsanforderungen. Warnung bei destruktiven Operationen. Vollständige Request/Response-Beispiele.

    **Abgrenzung:** Keine Standard-API-Endpunkte (→ api/endpoints.md), keine operative Sicherheit (→ operations/security.md).

    **Beispiel-Inhalte:** `DELETE /api/v1/admin/users/42` mit Bestätigungsheader, `GET /api/v1/admin/audit-log?action=login&from=2024-01-01`, Tabelle der Admin-Scopes.

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
    **Zielgruppe:** Ops-Teams, Monitoring-Systeme, Load Balancer

    **Pflicht-Abschnitte:**

    - Health-Check-Endpunkte (Liveness, Readiness, Startup)
    - Response-Format und Statuscodes (200 vs. 503)
    - Detaillierter Health-Status (Datenbank, Cache, externe Dienste)
    - Konfiguration für Kubernetes-Probes
    - Metriken-Endpunkt (Prometheus-kompatibel)

    **Inhaltliche Tiefe:** Vollständige Response-Beispiele für healthy und unhealthy. Kubernetes-YAML-Snippet für Probe-Konfiguration.

    **Abgrenzung:** Keine Monitoring-Einrichtung (→ operations/monitoring.md), keine allgemeine API-Referenz (→ api/endpoints.md).

    **Beispiel-Inhalte:** `GET /health` → `{"status": "ok", "checks": {"db": "ok", "cache": "ok"}}`, `GET /health/ready` → 503 bei DB-Ausfall, Kubernetes: `livenessProbe: httpGet: path: /health port: 8080`.

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
    **Zielgruppe:** Architekten, Entwickler, Ops-Teams

    **Pflicht-Abschnitte:**

    - Übersicht aller verfügbaren Integrationen (Tabelle mit Status)
    - Kategorisierung (Authentifizierung, CI/CD, Speicher, Messaging etc.)
    - Allgemeine Integrations-Architektur (Diagramm)
    - Voraussetzungen und Kompatibilitätsmatrix
    - Schnellstart-Links zu den Einzelseiten

    **Inhaltliche Tiefe:** Navigationsseite mit kurzem Absatz pro Integration. Architekturdiagramm zeigt Datenflüsse zwischen Systemen.

    **Abgrenzung:** Keine Detail-Konfiguration (→ jeweilige Unterseiten), keine API-Endpunkte (→ api/endpoints.md).

    **Beispiel-Inhalte:** Tabelle: Integration | Typ | Status (✓/Beta/Planned), Mermaid-Diagramm mit System → Integration → Externer Dienst, Links: 'SSO einrichten → integrations/sso.md'.

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
    **Zielgruppe:** IT-Admins, Security-Ingenieure

    **Pflicht-Abschnitte:**

    - Unterstützte Protokolle: LDAP, SAML 2.0, OAuth2, OpenID Connect
    - Konfiguration pro Protokoll (Schritt-für-Schritt)
    - Identity Provider Setup (Keycloak, Azure AD, Okta etc.)
    - Attribut-Mapping (User-Felder, Gruppen, Rollen)
    - Fallback-Authentifizierung und lokale Konten
    - Troubleshooting häufiger SSO-Probleme

    **Inhaltliche Tiefe:** Vollständige Konfigurationsbeispiele pro Protokoll. Screenshots oder YAML-Snippets für IdP-Setup. Debug-Checkliste.

    **Abgrenzung:** Keine API-Token-Auth (→ api/authentication.md), keine Netzwerk-Konfiguration (→ operations/network.md).

    **Beispiel-Inhalte:** SAML-Config: `sso.saml.entity_id`, `sso.saml.metadata_url`, LDAP: `ldap.base_dn: 'dc=example,dc=com'`, Troubleshooting: 'SAML-Response ungültig → Zertifikat prüfen'.

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
    **Zielgruppe:** DevOps-Ingenieure, Entwickler

    **Pflicht-Abschnitte:**

    - Unterstützte CI/CD-Systeme (Jenkins, GitLab CI, GitHub Actions, etc.)
    - Pipeline-Integration (API-Trigger, Webhooks, CLI)
    - Konfigurations-Beispiele pro CI/CD-System
    - Umgebungsvariablen und Secrets-Management
    - Artefakt-Handling (Upload, Download, Versionierung)
    - Status-Reporting (Commit-Status, PR-Checks)

    **Inhaltliche Tiefe:** Mindestens ein vollständiges Pipeline-Beispiel pro System. YAML-Snippets für GitHub Actions und GitLab CI.

    **Abgrenzung:** Keine interne CI/CD-Pipeline-Doku (→ development/ci-cd.md), keine Deployment-Strategien (→ operations/deployment.md).

    **Beispiel-Inhalte:** GitHub Actions Workflow mit API-Aufruf, GitLab CI `.gitlab-ci.yml`-Stage, Jenkins Pipeline-Script mit `httpRequest`-Step.

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
    **Zielgruppe:** Entwickler und Integrations-Architekten

    **Pflicht-Abschnitte:**

    - Webhook-Anbindung an externe Systeme (Slack, Teams, Jira etc.)
    - Konfiguration der Webhook-Ziel-URLs
    - Payload-Transformation und Mapping
    - Sicherheit: Secret-Verifizierung, IP-Whitelisting
    - Monitoring und Fehlerbehandlung bei Zustellung
    - Vorgefertigte Integrations-Templates

    **Inhaltliche Tiefe:** Schritt-für-Schritt-Anleitung pro Zielsystem. Mapping-Tabelle: internes Event → externes Format.

    **Abgrenzung:** Keine API-Webhook-Definition (→ api/webhooks.md), keine Message-Queue-Integration (→ integrations/messaging.md).

    **Beispiel-Inhalte:** Slack-Webhook: URL eintragen, Payload-Format für Slack-Blocks, Jira-Webhook: Issue erstellen bei Event `ticket.created`, Test-Funktion: `POST /api/v1/webhooks/test`.

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
    **Zielgruppe:** Entwickler, Architekten, Projektleiter

    **Pflicht-Abschnitte:**

    - Übersicht unterstützter Drittanbieter-Dienste
    - Konfiguration pro Dienst (API-Keys, Endpoints, Optionen)
    - Datenfluss und Synchronisierung
    - Authentifizierung gegenüber Drittanbietern (OAuth2, API-Keys)
    - Fehlerbehandlung bei Drittanbieter-Ausfällen
    - Datenschutz und Compliance-Hinweise

    **Inhaltliche Tiefe:** Pro Dienst: Zweck, Konfiguration, Datenfluss-Diagramm. Fallback-Verhalten bei Ausfall dokumentieren.

    **Abgrenzung:** Keine SSO-Details (→ integrations/sso.md), keine Monitoring-Tools (→ integrations/monitoring.md).

    **Beispiel-Inhalte:** Stripe-Integration: API-Key konfigurieren, Webhook für Payment-Events, Datenfluss-Diagramm, Fehler: 'Stripe nicht erreichbar → Retry-Queue aktiviert'.

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
    **Zielgruppe:** Ops-Teams, SREs, DevOps-Ingenieure

    **Pflicht-Abschnitte:**

    - Unterstützte Monitoring-Systeme (Prometheus, Grafana, Datadog, etc.)
    - Metriken-Export-Konfiguration
    - Verfügbare Metriken (Tabelle: Name, Typ, Beschreibung)
    - Dashboard-Vorlagen und Import-Anleitung
    - Alert-Integration (PagerDuty, OpsGenie, E-Mail)
    - Tracing-Integration (Jaeger, Zipkin, OpenTelemetry)

    **Inhaltliche Tiefe:** Vollständige Konfigurationsbeispiele. Grafana-Dashboard-JSON zum Import. Prometheus-Scrape-Config.

    **Abgrenzung:** Keine Alert-Regeln-Definition (→ operations/monitoring-alerts.md), keine interne Monitoring-Strategie (→ operations/monitoring.md).

    **Beispiel-Inhalte:** Prometheus: `scrape_configs: - job_name: 'myapp' static_configs: - targets: ['localhost:8080']`, Grafana-Dashboard-Screenshot-Beschreibung, Metriken-Tabelle: `http_requests_total` (counter), `request_duration_seconds` (histogram).

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
    **Zielgruppe:** Ops-Teams, Backend-Entwickler

    **Pflicht-Abschnitte:**

    - Unterstützte Speicherdienste (S3, MinIO, Azure Blob, GCS)
    - Konfiguration pro Anbieter (Credentials, Bucket, Region)
    - Datei-Management (Upload, Download, Löschen)
    - Verschlüsselung (at-rest, in-transit)
    - Lifecycle-Policies (Archivierung, automatisches Löschen)
    - Lokaler Speicher als Fallback

    **Inhaltliche Tiefe:** Vollständige Konfigurationsbeispiele pro Anbieter. Entscheidungshilfe: welcher Anbieter wann.

    **Abgrenzung:** Keine Backup-Strategie (→ integrations/backup-services.md, operations/backup.md), keine Datei-Upload-API (→ api/file-upload.md).

    **Beispiel-Inhalte:** S3-Config: `storage.type: s3`, `storage.bucket: my-bucket`, `storage.region: eu-central-1`, MinIO: `storage.endpoint: https://minio.local:9000`.

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
    **Zielgruppe:** Backend-Entwickler, Architekten

    **Pflicht-Abschnitte:**

    - Unterstützte Message-Broker (RabbitMQ, Kafka, Redis Pub/Sub, NATS)
    - Konfiguration pro Broker (Connection-String, Credentials)
    - Queue-/Topic-Konfiguration
    - Nachrichtenformat und Serialisierung
    - Dead-Letter-Queues und Fehlerbehandlung
    - Skalierung und Partitionierung

    **Inhaltliche Tiefe:** Vollständige Konfiguration pro Broker. Architekturdiagramm mit Producer/Consumer-Muster.

    **Abgrenzung:** Keine Webhook-Konfiguration (→ integrations/webhooks.md), keine E-Mail-Versand (→ integrations/email.md).

    **Beispiel-Inhalte:** RabbitMQ: `messaging.broker: amqp://user:pass@localhost:5672`, Kafka: `messaging.bootstrap_servers: ['kafka:9092']`, Nachrichtenformat: `{"event": "user.created", "data": {...}, "timestamp": "..."}`.

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
    **Zielgruppe:** Backend-Entwickler, DBAs, Ops-Teams

    **Pflicht-Abschnitte:**

    - Unterstützte Datenbanken (PostgreSQL, MySQL, MongoDB, Redis)
    - Connection-String-Format und Konfiguration
    - Connection-Pooling-Einstellungen
    - SSL/TLS-Verbindung konfigurieren
    - Read-Replicas und Failover
    - Migrationstool-Konfiguration

    **Inhaltliche Tiefe:** Vollständige Connection-Beispiele pro Datenbank. Performance-Tuning-Tipps für Connection-Pools.

    **Abgrenzung:** Keine Schema-Design-Richtlinien (→ development/database-guide.md), keine Migrations-Anleitung (→ development/migration-writing.md), keine Backup-Strategien (→ operations/backup.md).

    **Beispiel-Inhalte:** PostgreSQL: `database.url: postgresql://user:pass@host:5432/dbname`, Pool: `database.pool_size: 20, database.max_overflow: 10`, SSL: `database.ssl_mode: verify-full, database.ssl_ca: /path/to/ca.pem`.

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
    **Zielgruppe:** Backend-Entwickler, Ops-Teams

    **Pflicht-Abschnitte:**

    - Unterstützte E-Mail-Dienste (SMTP, SendGrid, SES, Mailgun)
    - SMTP-Konfiguration (Host, Port, TLS, Credentials)
    - API-basierter Versand (Konfiguration pro Anbieter)
    - E-Mail-Templates und Variablen
    - Bounce-Handling und Zustellüberwachung
    - Rate-Limits und Queuing

    **Inhaltliche Tiefe:** Vollständige SMTP-Konfiguration. Beispiel-Template mit Variablen-Platzhaltern. Test-Anleitung.

    **Abgrenzung:** Keine Benachrichtigungs-Logik (→ api/webhooks.md), keine Message-Queue-Details (→ integrations/messaging.md).

    **Beispiel-Inhalte:** SMTP: `email.host: smtp.gmail.com`, `email.port: 587`, `email.tls: true`, SES: `email.provider: ses, email.region: eu-west-1`, Template: `Hallo {{user.name}}, Ihr Passwort wurde geändert.`

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
    **Zielgruppe:** Backend-Entwickler, Ops-Teams

    **Pflicht-Abschnitte:**

    - Unterstützte Suchmaschinen (Elasticsearch, OpenSearch, MeiliSearch, Typesense)
    - Verbindungs-Konfiguration (Host, Port, Credentials, Index-Prefix)
    - Index-Management (Erstellung, Mapping, Reindexierung)
    - Synchronisierung: Datenbank → Suchindex
    - Analyzer- und Tokenizer-Konfiguration (Sprachen, Stemming)
    - Performance-Tuning (Shards, Replicas, Caching)

    **Inhaltliche Tiefe:** Vollständige Index-Mapping-Beispiele. Synchronisierungs-Strategien (Echtzeit vs. Batch).

    **Abgrenzung:** Keine Such-API-Endpunkte (→ api/search-api.md), keine CDN-Konfiguration (→ integrations/cdn.md).

    **Beispiel-Inhalte:** Elasticsearch: `search.hosts: ['https://es:9200']`, Index-Mapping: `{"properties": {"title": {"type": "text", "analyzer": "german"}}}`, Reindex-Befehl: `POST /api/v1/admin/reindex`.

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
    **Zielgruppe:** Ops-Teams, Frontend-Entwickler

    **Pflicht-Abschnitte:**

    - Unterstützte CDN-Anbieter (CloudFront, Cloudflare, Fastly, Bunny)
    - CDN-Konfiguration (Origin, Cache-Regeln, TTL)
    - Cache-Invalidierung (API, CLI, automatisch bei Deploy)
    - Custom-Domain und SSL-Zertifikate
    - Asset-Optimierung (Kompression, Bildformate)
    - Geo-Routing und Failover

    **Inhaltliche Tiefe:** Konfigurationsbeispiel pro Anbieter. Cache-Strategie-Entscheidungsbaum.

    **Abgrenzung:** Keine Netzwerk-Konfiguration (→ operations/network.md), keine Speicher-Konfiguration (→ integrations/storage.md).

    **Beispiel-Inhalte:** CloudFront: Distribution-Config mit Origin-Settings, Cache-Behavior: `*.js → max-age=31536000`, `*.html → max-age=300`, Invalidierung: `aws cloudfront create-invalidation --paths '/*'`.

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
    **Zielgruppe:** Ops-Teams, Systemadministratoren

    **Pflicht-Abschnitte:**

    - Unterstützte Backup-Dienste (AWS Backup, Restic, Velero, BorgBackup)
    - Konfiguration pro Dienst (Ziel-Speicher, Credentials, Zeitplan)
    - Backup-Umfang (Datenbank, Dateien, Konfiguration)
    - Verschlüsselung und Aufbewahrungsrichtlinien
    - Restore-Test-Anleitung
    - Monitoring und Alerting bei Backup-Fehlern

    **Inhaltliche Tiefe:** Vollständige Konfiguration pro Dienst. Cron-Ausdruck-Beispiele. Restore-Checkliste.

    **Abgrenzung:** Keine Backup-Strategie-Entscheidung (→ operations/backup.md), keine Speicher-Konfiguration (→ integrations/storage.md).

    **Beispiel-Inhalte:** Restic: `backup.type: restic`, `backup.repo: s3:s3.amazonaws.com/backup-bucket`, Zeitplan: `backup.schedule: '0 2 * * *'` (täglich 02:00), Aufbewahrung: `backup.retention: {daily: 7, weekly: 4, monthly: 12}`.

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
    **Zielgruppe:** Entwickler, Architekten, neue Teammitglieder (technisch)

    **Pflicht-Abschnitte:**

    - Überblick der automatisch generierten Developer-Dokumentation
    - Verzeichnis aller Unterbereiche (Klassen, Module, Diagramme) mit Kurzbeschreibung
    - Generierungsprozess: welches Tool, wann wird aktualisiert, Trigger (CI/manuell)
    - Hinweis auf manuelle Ergänzungen vs. generierte Inhalte
    - Quick-Links zu den wichtigsten Klassen und Modulen
    - Versionsinformation: aus welchem Code-Stand generiert

    **Inhaltliche Tiefe:** Navigationsseite mit klarer Struktur; kurze Beschreibung je Unterbereich; Verlinkung zu Quellcode-Repository; Generierungszeitstempel

    **Abgrenzung:** Keine vollständige Klassen-Doku → `generated/developer/classes/`; keine Architekturentscheidungen → `architecture/decisions/`

    **Beispiel-Inhalte:** Struktur: Klassen (42 dokumentiert) | Module (12 dokumentiert) | Diagramme (8 generiert); Generiert am: 2025-01-15 aus Commit abc1234

## Abschnitte

- [Klassen](classes/index.md) — Klassenhierarchie und Verantwortlichkeiten
- [Module](modules/index.md) — Modulstruktur und Abhängigkeiten
- [Diagramme](diagrams/index.md) — Visualisierungen der Architektur

Dieser Bereich wird automatisch aus dem Quellcode generiert.
"""),

    ("generated/developer/classes/index.md", "Klassen", """
!!! tip "Inhaltsrichtlinie"
    **Zielgruppe:** Entwickler, Code-Reviewer, Architekten

    **Pflicht-Abschnitte:**

    - Alphabetische Liste aller dokumentierten Klassen
    - Gruppierung nach Modul/Package (z.B. auth, core, api, models)
    - Je Klasse: Kurzname, vollständiger Pfad, Ein-Satz-Beschreibung
    - Vererbungshierarchie (Basisklassen und abgeleitete Klassen)
    - Filtermöglichkeit nach Modul oder Funktionsbereich
    - Verlinkung zur Detail-Seite jeder Klasse

    **Inhaltliche Tiefe:** Index-Ebene: keine vollständige API-Doku, sondern Übersicht und Navigation; Klassen-Anzahl und Abdeckungsgrad; Hinweis auf undokumentierte Klassen

    **Abgrenzung:** Keine vollständige Methoden-Dokumentation → Klassen-Detailseiten; keine Module-Übersicht → `generated/developer/modules/index.md`

    **Beispiel-Inhalte:** Tabelle: Klasse | Modul | Beschreibung; z.B. `UserService` | `auth` | „Verwaltung von Benutzerkonten und Authentifizierung"
"""),

    ("generated/developer/modules/index.md", "Module", """
!!! tip "Inhaltsrichtlinie"
    **Zielgruppe:** Entwickler, Architekten, neue Teammitglieder (technisch)

    **Pflicht-Abschnitte:**

    - Liste aller Module/Packages mit Kurzbeschreibung
    - Abhängigkeitsgraph zwischen Modulen (textuell oder als Diagramm-Verweis)
    - Je Modul: Name, Zweck, öffentliche API-Oberfläche, Anzahl Klassen/Funktionen
    - Schichtung: welche Module auf welcher Ebene liegen (Presentation, Business, Data)
    - Verlinkung zur Detail-Seite jedes Moduls

    **Inhaltliche Tiefe:** Architektonische Einordnung je Modul; Import-Richtlinien (welches Modul darf welches importieren); Abhängigkeitsrichtung (nur nach unten)

    **Abgrenzung:** Keine Klassen-Details → `generated/developer/classes/index.md`; keine Architekturdiagramme → `generated/developer/diagrams/index.md`

    **Beispiel-Inhalte:** Tabelle: Modul | Schicht | Abhängigkeiten | Klassen | Beschreibung; z.B. `auth` | Business | `core`, `db` | 8 Klassen | „Authentifizierung und Autorisierung"
"""),

    ("generated/developer/diagrams/index.md", "Diagramme", """
!!! tip "Inhaltsrichtlinie"
    **Zielgruppe:** Architekten, Entwickler, technische Projektleitung

    **Pflicht-Abschnitte:**

    - Katalog aller generierten Diagramme mit Vorschaubild und Beschreibung
    - Diagrammtypen: Klassendiagramme, Sequenzdiagramme, Komponentendiagramme, ER-Diagramme
    - Generierungswerkzeug (PlantUML, Mermaid, Draw.io) und Quellformat
    - Aktualisierungshinweise: wann zuletzt generiert, aus welchem Code-Stand
    - Anleitung zur Regenerierung und manuellen Anpassung
    - Verlinkung zur Vollansicht jedes Diagramms

    **Inhaltliche Tiefe:** Vorschaubilder mit Klickvergrößerung; Beschreibung was jedes Diagramm zeigt; Hinweis auf Einschränkungen der automatischen Generierung

    **Abgrenzung:** Keine Architekturentscheidungen → `architecture/decisions/`; keine handgezeichneten Architekturbilder → `architecture/`

    **Beispiel-Inhalte:** Katalog: Klassendiagramm-auth | Sequenz-Login-Flow | ER-Diagramm-Datenbank | Komponentenübersicht; Generiert mit PlantUML aus Docstrings
"""),

    # ━━ Entwicklung ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ("development/contributing.md", "Contributing", """
!!! tip "Inhaltsrichtlinie"
    **Zielgruppe:** Neue und bestehende Entwickler, Open-Source-Beitragende

    **Pflicht-Abschnitte:**

    - Willkommensnachricht und Projekt-Überblick
    - Voraussetzungen (Tools, Versionen, Accounts)
    - Schritt-für-Schritt: Ersten Beitrag erstellen
    - Issue-Typen und Labels (Bug, Feature, Good First Issue)
    - Pull-Request-Richtlinien (Titel, Beschreibung, Größe)
    - Code of Conduct und Kommunikationskanäle
    - Lizenz-Hinweis für Beiträge

    **Inhaltliche Tiefe:** Einsteigerfreundlich. Jeder Schritt mit Befehl. Entscheidungsbaum: 'Was möchtest du beitragen?'

    **Abgrenzung:** Keine Entwicklungsumgebung-Details (→ development/setup.md), keine Code-Stil-Regeln (→ development/code-style.md).

    **Beispiel-Inhalte:** `git clone ...`, `git checkout -b feature/mein-beitrag`, PR-Template: Titel: 'feat: Kurzbeschreibung', Labels: `good-first-issue`, `help-wanted`, `bug`.

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
    **Zielgruppe:** Neue Entwickler im Team

    **Pflicht-Abschnitte:**

    - System-Voraussetzungen (OS, Sprachen, Laufzeiten, Versionen)
    - Repository klonen und Dependencies installieren
    - Umgebungsvariablen und Konfigurationsdateien (.env)
    - Datenbank und externe Dienste lokal aufsetzen (Docker-Compose)
    - Applikation starten und verifizieren
    - IDE-Setup und empfohlene Plugins
    - Häufige Setup-Probleme und Lösungen

    **Inhaltliche Tiefe:** Copy-Paste-fertige Befehle. Erwartete Ausgabe nach jedem Schritt. Troubleshooting-Tabelle.

    **Abgrenzung:** Keine Beitragsrichtlinien (→ development/contributing.md), keine CI/CD-Konfiguration (→ development/ci-cd.md).

    **Beispiel-Inhalte:** `python -m venv .venv && source .venv/bin/activate`, `docker-compose up -d postgres redis`, `cp .env.example .env`, `python manage.py migrate`, Troubleshooting: 'Port 5432 belegt → `lsof -i :5432`'.

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
    **Zielgruppe:** Alle Entwickler im Projekt

    **Pflicht-Abschnitte:**

    - Allgemeine Prinzipien (Clean Code, SOLID, DRY)
    - Sprach-spezifische Regeln (Linter-Konfiguration, Formatter)
    - Naming-Konventionen (Variablen, Funktionen, Klassen, Dateien)
    - Import-Ordnung und Modul-Struktur
    - Kommentar- und Docstring-Richtlinien
    - Automatische Formatierung (Pre-Commit-Hooks)

    **Inhaltliche Tiefe:** Jede Regel mit positivem und negativem Beispiel. Linter-Konfigurationsdatei vollständig abgedruckt.

    **Abgrenzung:** Keine Architektur-Entscheidungen (→ development/api-design.md), keine Test-Richtlinien (→ development/testing.md).

    **Beispiel-Inhalte:** Gut: `def calculate_total_price(items: list[Item]) -> Decimal`, Schlecht: `def calc(x)`, `.flake8`: `max-line-length = 120`, Pre-Commit: `repos: - repo: https://github.com/psf/black`.

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
    **Zielgruppe:** Alle Entwickler

    **Pflicht-Abschnitte:**

    - Test-Pyramide (Unit, Integration, E2E) und Zielquoten
    - Test-Framework und -Tools (pytest, Jest, Cypress etc.)
    - Testdaten-Management (Fixtures, Factories, Faker)
    - Mocking-Strategien (externe Dienste, Datenbank)
    - Test-Organisation (Verzeichnisstruktur, Namenskonventionen)
    - Coverage-Anforderungen und -Berichte
    - Tests lokal und in CI ausführen

    **Inhaltliche Tiefe:** Konkretes Beispiel pro Testtyp. Minimale Coverage-Schwelle definiert. Mocking-Beispiel mit Code.

    **Abgrenzung:** Keine Sicherheitstests (→ development/security-testing.md), keine Performance-Tests (→ development/performance-testing.md).

    **Beispiel-Inhalte:** pytest: `def test_user_creation():`, Factory: `UserFactory(role='admin')`, Mock: `@patch('app.services.email.send')`, Coverage: `pytest --cov=src --cov-fail-under=80`.

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
    **Zielgruppe:** Release-Manager, Senior-Entwickler

    **Pflicht-Abschnitte:**

    - Release-Zyklus und Versionierungsschema (SemVer)
    - Release-Checkliste (Tests, Changelog, Tag, Build)
    - Branching-Strategie für Releases (Release-Branch, Hotfix)
    - Changelog-Generierung (automatisch/manuell)
    - Artefakt-Erstellung und -Publikation
    - Rollback-Verfahren
    - Kommunikation (intern, extern, Changelog veröffentlichen)

    **Inhaltliche Tiefe:** Vollständige Checkliste mit Befehlen. Entscheidungsbaum für Versionserhöhung.

    **Abgrenzung:** Keine Deployment-Strategien (→ operations/deployment.md), keine Git-Workflow-Details (→ development/git-workflow.md).

    **Beispiel-Inhalte:** Checkliste: 1. `git checkout -b release/1.2.0`, 2. `bumpversion minor`, 3. Changelog aktualisieren, 4. `git tag v1.2.0`, 5. CI baut Artefakte, 6. Merge in main und develop.

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
    **Zielgruppe:** Alle Entwickler

    **Pflicht-Abschnitte:**

    - Debug-Tools und -Konfiguration (Debugger, IDE-Integration)
    - Logging für Debugging (Log-Level temporär erhöhen)
    - Remote-Debugging (Docker, Kubernetes)
    - Debugging von Datenbank-Queries (Query-Log, EXPLAIN)
    - Profiling (CPU, Memory, I/O)
    - Häufige Fehlerbilder und systematische Analyse

    **Inhaltliche Tiefe:** Konkrete Befehle und Konfigurationen pro Tool. Schritt-für-Schritt-Anleitung für typische Debug-Szenarien.

    **Abgrenzung:** Keine Error-Handling-Patterns (→ development/error-handling-guide.md), keine Logging-Strategie (→ development/logging-guide.md).

    **Beispiel-Inhalte:** Python: `import pdb; pdb.set_trace()`, VS Code `launch.json` für Remote-Attach, PostgreSQL: `SET log_statement = 'all';`, Memory-Profiling: `python -m memory_profiler script.py`.

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
    **Zielgruppe:** DevOps-Ingenieure, alle Entwickler

    **Pflicht-Abschnitte:**

    - Pipeline-Übersicht (Stages: Lint, Test, Build, Deploy)
    - Pipeline-Konfigurationsdatei erklärt (Zeile für Zeile)
    - Trigger-Regeln (Push, PR, Tag, Schedule)
    - Umgebungsvariablen und Secrets in der Pipeline
    - Caching-Strategie (Dependencies, Build-Artefakte)
    - Pipeline-Debugging und Log-Analyse
    - Pipeline lokal ausführen (act, gitlab-runner exec)

    **Inhaltliche Tiefe:** Vollständige Pipeline-Datei mit Kommentaren. Troubleshooting-Tabelle für häufige Pipeline-Fehler.

    **Abgrenzung:** Keine externen CI/CD-Integrationen (→ integrations/ci-cd.md), keine Deployment-Strategie (→ operations/deployment.md).

    **Beispiel-Inhalte:** GitHub Actions: `on: [push, pull_request]`, Jobs: lint → test → build → deploy, Cache: `actions/cache@v3 with path: ~/.cache/pip`, Secret: `${{ secrets.API_KEY }}`.

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
    **Zielgruppe:** Alle Entwickler, Security-Team

    **Pflicht-Abschnitte:**

    - Dependency-Management-Tool (pip, npm, cargo etc.)
    - Lockfile-Strategie und Versionspinning
    - Neue Abhängigkeiten hinzufügen (Evaluationskriterien)
    - Sicherheits-Scanning (Dependabot, Snyk, Safety)
    - Update-Strategie (automatisch, manuell, Zeitplan)
    - Private Registries und interne Pakete
    - Lizenz-Compliance-Prüfung

    **Inhaltliche Tiefe:** Evaluations-Checkliste für neue Dependencies. Automatisierungs-Konfiguration vollständig.

    **Abgrenzung:** Keine Setup-Anleitung (→ development/setup.md), keine Release-Prozess-Details (→ development/release.md).

    **Beispiel-Inhalte:** Checkliste: Aktive Maintenance? Lizenz kompatibel? Sicherheits-Historie? Download-Zahlen?, Dependabot: `.github/dependabot.yml` mit wöchentlichem Schedule, `pip-audit` oder `npm audit` in CI-Pipeline.

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
    **Zielgruppe:** Alle Entwickler, technische Redakteure

    **Pflicht-Abschnitte:**

    - Dokumentations-Typen (API-Docs, Guides, ADRs, Inline-Kommentare)
    - Wann was dokumentieren (Entscheidungsmatrix)
    - Markdown-Konventionen und Templates
    - Docs-as-Code-Workflow (neben dem Code pflegen)
    - Diagramme (Mermaid, PlantUML, draw.io)
    - Review-Prozess für Dokumentation
    - Lokale Vorschau (MkDocs serve, Docusaurus)

    **Inhaltliche Tiefe:** Template pro Dokumentationstyp. Beispiel-ADR vollständig ausgeschrieben.

    **Abgrenzung:** Keine API-Endpunkt-Doku (→ api/endpoints.md), keine Code-Kommentar-Regeln (→ development/code-style.md).

    **Beispiel-Inhalte:** ADR-Template: Titel, Status, Kontext, Entscheidung, Konsequenzen. Mermaid-Beispiel: `graph LR; A-->B;`, Vorschau: `mkdocs serve --dev-addr 0.0.0.0:8001`.

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
    **Zielgruppe:** Alle Entwickler

    **Pflicht-Abschnitte:**

    - Branching-Modell (Git Flow, GitHub Flow, Trunk-Based)
    - Branch-Namenskonventionen (feature/, bugfix/, hotfix/)
    - Commit-Message-Format (Conventional Commits)
    - Merge-Strategie (Merge-Commit, Squash, Rebase)
    - Konflikt-Lösung (Schritt-für-Schritt)
    - Protected Branches und Branch-Regeln
    - Git-Hooks (Pre-Commit, Commit-Msg)

    **Inhaltliche Tiefe:** Visuelles Branching-Diagramm. Jede Konvention mit Beispiel-Befehl.

    **Abgrenzung:** Keine Release-Strategie (→ development/release.md), keine Code-Review-Details (→ development/code-review.md).

    **Beispiel-Inhalte:** Branch: `feature/TICKET-123-add-user-export`, Commit: `feat(users): add CSV export endpoint`, Merge: `git merge --no-ff feature/...`, Pre-Commit: `pre-commit install`.

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
    **Zielgruppe:** Alle Entwickler (Autoren und Reviewer)

    **Pflicht-Abschnitte:**

    - Review-Pflicht und Mindestanzahl Approvals
    - Was der Reviewer prüft (Checkliste)
    - Feedback-Kultur (konstruktiv, konkret, lösungsorientiert)
    - Review-Kommentar-Konventionen (nit:, blocker:, question:)
    - Zeitrahmen für Reviews (SLA)
    - Auto-Merge-Regeln
    - Umgang mit großen PRs (Aufteilen, Stacked PRs)

    **Inhaltliche Tiefe:** Checkliste zum Ausdrucken/Einbetten. Beispiele für gute und schlechte Review-Kommentare.

    **Abgrenzung:** Keine Git-Workflow-Details (→ development/git-workflow.md), keine Code-Style-Regeln (→ development/code-style.md).

    **Beispiel-Inhalte:** Checkliste: Tests vorhanden? Docs aktualisiert? Keine Secrets im Code? Performance-Implikationen?, Gut: 'Dieser Loop hat O(n²) — könnten wir ein Set nutzen?', Schlecht: 'Das ist falsch.'.

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
    **Zielgruppe:** Backend-Entwickler, Architekten

    **Pflicht-Abschnitte:**

    - REST-Designprinzipien (Ressourcen, HTTP-Verben, Statuscodes)
    - URL-Struktur und Naming-Konventionen
    - Request/Response-Format-Standards
    - Pagination-Muster (Offset, Cursor, Keyset)
    - Filterung, Sortierung, Feld-Selektion
    - Versionierung neuer Endpunkte
    - API-Review-Prozess vor Implementierung

    **Inhaltliche Tiefe:** Jedes Muster mit Positivbeispiel und Anti-Pattern. Entscheidungsbaum für Pagination-Strategie.

    **Abgrenzung:** Keine konkrete Endpunkt-Dokumentation (→ api/endpoints.md), keine GraphQL-Richtlinien (→ api/graphql.md).

    **Beispiel-Inhalte:** Gut: `GET /api/v1/users/42/orders`, Schlecht: `GET /api/v1/getUserOrders?userId=42`, Pagination: `?cursor=abc123&limit=20` mit `next_cursor` in Response, Review: API-Design-Doc vor Implementierung vorlegen.

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
    **Zielgruppe:** Entwickler, Security-Ingenieure

    **Pflicht-Abschnitte:**

    - SAST-Tools (Static Application Security Testing)
    - DAST-Tools (Dynamic Application Security Testing)
    - Dependency-Scanning (bekannte Schwachstellen)
    - OWASP Top 10 Testfälle
    - Security-Tests in CI/CD integrieren
    - Penetration-Testing-Vorgehen
    - Responsible Disclosure und Bug-Bounty

    **Inhaltliche Tiefe:** Tool-Konfiguration vollständig. Mindestens ein Testfall pro OWASP-Kategorie.

    **Abgrenzung:** Keine operative Sicherheit (→ operations/security.md), keine allgemeine Test-Strategie (→ development/testing.md).

    **Beispiel-Inhalte:** SAST: `bandit -r src/`, DAST: `zap-cli quick-scan https://staging.example.com`, OWASP A01 Broken Access Control: Test unautorisierter Zugriff auf Admin-Endpunkte, CI: Stage `security-scan` nach Unit-Tests.

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
    **Zielgruppe:** Entwickler, QA-Ingenieure, Ops-Teams

    **Pflicht-Abschnitte:**

    - Performance-Test-Typen (Load, Stress, Spike, Soak)
    - Tools (Locust, k6, JMeter, Artillery)
    - Test-Szenarien und Lastprofile definieren
    - Messwerte und Akzeptanzkriterien (p50, p95, p99, Throughput)
    - Performance-Baselines und Regression-Erkennung
    - Ergebnis-Auswertung und Reporting
    - Performance-Tests in CI/CD

    **Inhaltliche Tiefe:** Vollständiges k6-/Locust-Skript. Tabelle mit SLOs (z. B. p99 < 500ms).

    **Abgrenzung:** Keine Produktions-Performance-Optimierung (→ operations/performance.md), keine funktionalen Tests (→ development/testing.md).

    **Beispiel-Inhalte:** k6-Skript: `export default function() { http.get('...'); }` mit `stages: [{duration: '2m', target: 100}]`, SLO-Tabelle: Endpoint | p95 | p99 | Max RPS, CI: 'Performance-Regression wenn p95 > 120% Baseline'.

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
    **Zielgruppe:** Alle Entwickler

    **Pflicht-Abschnitte:**

    - Fehlerbehandlungs-Philosophie (fail fast, explizite Fehler)
    - Exception-Hierarchie (Custom Exceptions)
    - HTTP-Fehler-Mapping (Exception → HTTP-Statuscode)
    - Fehler-Logging-Regeln (was, wann, welches Level)
    - Benutzerfreundliche Fehlermeldungen (i18n-fähig)
    - Retry-Patterns (Transient vs. Permanent Errors)
    - Anti-Patterns (leere catch-Blöcke, Exception-Schlucken)

    **Inhaltliche Tiefe:** Code-Beispiele pro Pattern. Entscheidungsbaum: 'Welche Exception werfen?'

    **Abgrenzung:** Keine API-Fehler-Referenz (→ api/errors.md), keine Logging-Konfiguration (→ development/logging-guide.md).

    **Beispiel-Inhalte:** Custom Exception: `class OrderNotFoundError(AppError): status_code = 404`, Gut: `raise ValidationError('Email ungültig', field='email')`, Anti-Pattern: `except Exception: pass`.

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
    **Zielgruppe:** Alle Entwickler

    **Pflicht-Abschnitte:**

    - Log-Level-Definitionen (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    - Wann welches Level verwenden (Entscheidungstabelle)
    - Strukturiertes Logging (JSON-Format, Correlation-ID)
    - Sensitive Daten im Log vermeiden (PII, Passwörter, Tokens)
    - Log-Kontexte (Request-ID, User-ID, Trace-ID)
    - Performance-Auswirkungen von Logging
    - Logger-Konfiguration pro Umgebung

    **Inhaltliche Tiefe:** Code-Beispiel für strukturierten Logger. Tabelle: Situation → Log-Level.

    **Abgrenzung:** Keine Log-Aggregation (→ operations/logging-strategy.md), keine Debugging-Techniken (→ development/debugging.md).

    **Beispiel-Inhalte:** `logger.info('Bestellung erstellt', extra={'order_id': 42, 'user_id': 7})`, Tabelle: Benutzer-Login → INFO, DB-Verbindung verloren → ERROR, Schlecht: `logger.debug(f'User password: {password}')`, JSON: `{"level": "info", "msg": "...", "request_id": "abc-123"}`.

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
    **Zielgruppe:** Backend-Entwickler

    **Pflicht-Abschnitte:**

    - Schema-Design-Prinzipien (Normalisierung, Denormalisierung)
    - Naming-Konventionen (Tabellen, Spalten, Indizes, Constraints)
    - Index-Strategie (wann, welcher Typ, zusammengesetzte Indizes)
    - Query-Optimierung (N+1-Problem, JOINs, Subqueries)
    - ORM-Nutzung und Raw-SQL-Regeln
    - Transaktions-Handling und Isolation-Level
    - Datenbank-spezifische Features (JSONB, Arrays, CTEs)

    **Inhaltliche Tiefe:** Jede Regel mit SQL-Beispiel. EXPLAIN-Analyse-Beispiel für Query-Optimierung.

    **Abgrenzung:** Keine DB-Verbindungskonfiguration (→ integrations/database.md), keine Migrations-Anleitung (→ development/migration-writing.md).

    **Beispiel-Inhalte:** Naming: `orders` (Plural), `created_at` (snake_case), `idx_orders_user_id` (Prefix idx_), Anti-Pattern: `SELECT * FROM orders` in Schleifen (N+1), Gut: `SELECT o.*, u.name FROM orders o JOIN users u ON o.user_id = u.id`.

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
    **Zielgruppe:** Backend-Entwickler

    **Pflicht-Abschnitte:**

    - Migrationstool und Befehle (Alembic, Django Migrations, Flyway)
    - Migration erstellen, prüfen und anwenden
    - Rückwärts-kompatible Migrationen (Zero-Downtime)
    - Daten-Migrationen (vs. Schema-Migrationen)
    - Rollback-Strategie und Down-Migrationen
    - Review-Checkliste für Migrationen
    - Große Tabellen migrieren (Lock-Vermeidung)

    **Inhaltliche Tiefe:** Vollständige Beispiel-Migration. Entscheidungsbaum: 'Brauche ich eine Daten-Migration?'

    **Abgrenzung:** Keine Schema-Design-Regeln (→ development/database-guide.md), keine DB-Konfiguration (→ integrations/database.md).

    **Beispiel-Inhalte:** Alembic: `alembic revision --autogenerate -m 'add_email_to_users'`, Zero-Downtime: 1. Spalte nullable hinzufügen, 2. Daten füllen, 3. NOT NULL setzen, Checkliste: Rollback getestet? Lock-Dauer geprüft? Indizes concurrent?

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
    **Zielgruppe:** Frontend-Entwickler, UX-Designer, QA-Ingenieure

    **Pflicht-Abschnitte:**

    - Barrierefreiheitsstandards (WCAG 2.1 AA/AAA, ARIA)
    - Semantisches HTML und Landmark-Regionen
    - Tastaturnavigation und Fokus-Management
    - Farbkontrast und visuelle Gestaltung
    - Screenreader-Kompatibilität (ARIA-Labels, Live-Regions)
    - Test-Tools (axe, Lighthouse, NVDA)
    - Checkliste pro Komponente

    **Inhaltliche Tiefe:** Konkrete HTML-Beispiele pro Regel. Test-Befehle für automatisierte und manuelle Prüfung.

    **Abgrenzung:** Keine allgemeine Code-Stil-Regeln (→ development/code-style.md), keine Test-Strategie (→ development/testing.md).

    **Beispiel-Inhalte:** Gut: `<button aria-label='Menü öffnen'>`, Schlecht: `<div onclick='...'>Klick</div>`, Kontrast: mindestens 4.5:1 für normalen Text, Test: `npx axe-cli https://localhost:3000 --rules wcag2aa`.

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
    **Zielgruppe:** DevOps-Ingenieure, SREs, Release-Manager

    **Pflicht-Abschnitte:**

    - Deployment-Strategien (Rolling, Blue-Green, Canary)
    - Deployment-Pipeline und -Ablauf
    - Umgebungen (Development, Staging, Production)
    - Konfigurationsmanagement pro Umgebung
    - Rollback-Verfahren (Schritt-für-Schritt)
    - Deployment-Checkliste (Pre/Post-Deployment)
    - Deployment-Metriken und -Validierung

    **Inhaltliche Tiefe:** Entscheidungsbaum für Strategie-Wahl. Vollständige Rollback-Anleitung. Kubernetes-Manifeste oder Docker-Compose.

    **Abgrenzung:** Keine CI/CD-Pipeline-Details (→ development/ci-cd.md), keine Infrastruktur-Provisionierung (→ operations/infrastructure.md).

    **Beispiel-Inhalte:** Blue-Green: `kubectl set image deployment/app app=myapp:v2.0`, Canary: 10% Traffic → Metriken prüfen → 50% → 100%, Rollback: `kubectl rollout undo deployment/app`, Checkliste: DB-Migration lief? Health-Check grün? Alerts stummgeschaltet?

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
    **Zielgruppe:** Ops-Teams, SREs, On-Call-Ingenieure

    **Pflicht-Abschnitte:**

    - Monitoring-Strategie (USE, RED, Golden Signals)
    - Metriken-Übersicht (System, Applikation, Business)
    - Logging-Architektur (Sammlung, Aggregation, Retention)
    - Alerting-Philosophie (Alert-Fatigue vermeiden)
    - Dashboard-Übersicht (welche Dashboards existieren)
    - Distributed Tracing
    - SLIs, SLOs und Error Budgets

    **Inhaltliche Tiefe:** Vollständige Metriken-Tabelle. SLO-Definitionen mit Berechnungsbeispielen.

    **Abgrenzung:** Keine Monitoring-Tool-Integration (→ integrations/monitoring.md), keine Alert-Regeln (→ operations/monitoring-alerts.md).

    **Beispiel-Inhalte:** RED: Rate (req/s), Errors (%), Duration (Latenz), SLO: 'API-Verfügbarkeit 99.9% pro Monat = max 43 Min Downtime', Dashboard-Liste: Overview, Per-Service, Database, Queue.

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
    **Zielgruppe:** Ops-Teams, Systemadministratoren, Compliance-Beauftragte

    **Pflicht-Abschnitte:**

    - Backup-Strategie (3-2-1-Regel, RPO/RTO-Ziele)
    - Was wird gesichert (Datenbank, Dateien, Konfiguration, Secrets)
    - Backup-Zeitplan und -Typen (Voll, Inkrementell, Differentiell)
    - Verschlüsselung und Aufbewahrungsfristen
    - Restore-Prozedur (Schritt-für-Schritt)
    - Regelmäßiger Restore-Test (Zeitplan, Protokoll)
    - Backup-Monitoring und Alerting

    **Inhaltliche Tiefe:** RPO/RTO pro Datenkategorie definiert. Vollständiger Restore-Befehl. Testprotokoll-Template.

    **Abgrenzung:** Keine Backup-Tool-Konfiguration (→ integrations/backup-services.md), keine Disaster-Recovery-Pläne (→ operations/disaster-recovery.md).

    **Beispiel-Inhalte:** 3-2-1: 3 Kopien, 2 Medien, 1 offsite. RPO: Datenbank 1h, Dateien 24h. RTO: 4h. Restore: `pg_restore -d mydb backup_2024-03-15.dump`, Testprotokoll: Datum, Backup-ID, Restore-Dauer, Datenintegrität-Check.

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
    **Zielgruppe:** Ops-Teams, Security-Ingenieure, Compliance-Beauftragte

    **Pflicht-Abschnitte:**

    - Sicherheitshärtung (OS, Container, Netzwerk)
    - Secrets-Management (Vault, Sealed Secrets, Umgebungsvariablen)
    - TLS-Konfiguration und Zertifikatsverwaltung
    - Netzwerk-Segmentierung und Firewall-Regeln
    - Vulnerability-Scanning (Images, Hosts, Dependencies)
    - Audit-Logging und Compliance
    - Incident-Response-Verfahren

    **Inhaltliche Tiefe:** Konkrete Härtungs-Checklisten. Vault-Konfigurationsbeispiel. Firewall-Regelbeispiele.

    **Abgrenzung:** Keine Sicherheitstests im Code (→ development/security-testing.md), keine API-Authentifizierung (→ api/authentication.md).

    **Beispiel-Inhalte:** Dockerfile: `USER nonroot`, kein Root-Container. Vault: `vault kv put secret/app db_password=...`, TLS: `ssl_protocols TLSv1.2 TLSv1.3;`, Incident: 1. Eindämmen, 2. Analysieren, 3. Beheben, 4. Post-Mortem.

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
    **Zielgruppe:** Ops-Teams, Architekten, SREs

    **Pflicht-Abschnitte:**

    - Horizontale vs. vertikale Skalierung
    - Auto-Scaling-Konfiguration (HPA, VPA, Custom Metrics)
    - Skalierungsgrenzen und Bottlenecks identifizieren
    - Datenbank-Skalierung (Read Replicas, Sharding, Connection Pooling)
    - Cache-Skalierung (Redis Cluster, Memcached)
    - Load-Balancer-Konfiguration
    - Skalierungs-Runbooks für Notfälle

    **Inhaltliche Tiefe:** HPA-YAML vollständig. Entscheidungsbaum: 'Horizontal oder vertikal skalieren?'

    **Abgrenzung:** Keine Performance-Messung (→ operations/performance.md), keine Kapazitätsplanung (→ operations/capacity-planning.md).

    **Beispiel-Inhalte:** HPA: `minReplicas: 2, maxReplicas: 10, targetCPUUtilization: 70`, Read Replica: `database.read_url: postgresql://replica:5432/db`, Notfall: 'Traffic-Spike → HPA-Max hochsetzen → Cache-TTL erhöhen → DB Read Replicas hinzufügen'.

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
    **Zielgruppe:** Ops-Teams, Backend-Entwickler, SREs

    **Pflicht-Abschnitte:**

    - Performance-Metriken und SLOs (Latenz, Throughput, Error Rate)
    - Profiling in Produktion (CPU, Memory, I/O)
    - Datenbank-Performance (Slow Queries, Index-Nutzung)
    - Caching-Strategien (Application Cache, CDN, Browser)
    - Performance-Optimierungs-Workflows
    - Kapazitätsplanung basierend auf Metriken
    - Performance-Dashboards und Berichte

    **Inhaltliche Tiefe:** Schritt-für-Schritt-Workflow: Problem identifizieren → Messen → Optimieren → Verifizieren. Slow-Query-Analyse-Beispiel.

    **Abgrenzung:** Keine Performance-Tests in Entwicklung (→ development/performance-testing.md), keine Skalierung (→ operations/scaling.md).

    **Beispiel-Inhalte:** Slow Query: `EXPLAIN ANALYZE SELECT ...`, Cache: `redis-cli INFO stats` → Hit-Rate prüfen, Workflow: 1. APM-Dashboard prüfen, 2. Slowest Endpoints identifizieren, 3. Profiler ansetzen, 4. Optimierung implementieren, 5. A/B-Vergleich.

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
    **Zielgruppe:** Ops-Teams, Management, Compliance-Beauftragte

    **Pflicht-Abschnitte:**

    - Disaster-Recovery-Plan (DRP) Übersicht
    - Recovery-Ziele (RPO, RTO pro Service-Tier)
    - Szenarien (Datenbank-Ausfall, Region-Ausfall, Datenverlust, Sicherheitsvorfall)
    - Recovery-Prozeduren pro Szenario (Schritt-für-Schritt)
    - Kommunikationsplan (intern, Kunden, Statuspage)
    - DR-Test-Zeitplan und -Protokoll
    - Verantwortlichkeiten (RACI-Matrix)

    **Inhaltliche Tiefe:** Vollständige Runbooks pro Szenario. Kontaktlisten. Entscheidungsbäume.

    **Abgrenzung:** Keine Backup-Details (→ operations/backup.md), keine täglichen Ops-Aufgaben (→ operations/maintenance.md).

    **Beispiel-Inhalte:** Szenario: DB-Ausfall → 1. Failover auf Standby, 2. Health-Check, 3. DNS-Update, 4. Kunden informieren. RACI: DBA=Responsible, SRE-Lead=Accountable, CTO=Informed. DR-Test: Quartalweise, letzter Test: Datum, Ergebnis.

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
    **Zielgruppe:** On-Call-Ingenieure, Ops-Teams

    **Pflicht-Abschnitte:**

    - Runbook-Format und -Konventionen
    - Runbook pro häufigem Vorfall (Tabelle: Alert → Runbook)
    - Schritt-für-Schritt-Anleitungen mit Befehlen
    - Eskalationspfade und Kontaktdaten
    - Post-Incident-Checkliste
    - Runbook-Pflege und Review-Zyklus

    **Inhaltliche Tiefe:** Jedes Runbook mit exakten Befehlen. Entscheidungspunkte klar markiert ('Wenn X → Schritt Y, sonst → Schritt Z').

    **Abgrenzung:** Keine Disaster-Recovery (→ operations/disaster-recovery.md), keine Monitoring-Konfiguration (→ operations/monitoring.md).

    **Beispiel-Inhalte:** Alert: 'High Memory Usage' → 1. `kubectl top pods -n production`, 2. Pod mit höchstem Verbrauch identifizieren, 3. `kubectl describe pod <name>`, 4. Wenn OOMKilled → Restart, sonst → Heap-Dump + Eskalation an Dev-Team.

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
    **Zielgruppe:** Ops-Teams, Infrastruktur-Architekten

    **Pflicht-Abschnitte:**

    - Infrastruktur-Übersicht (Diagramm mit allen Komponenten)
    - IaC-Tool und Repository (Terraform, Pulumi, Ansible)
    - Umgebungs-Topologien (Dev, Staging, Prod)
    - Cloud-Ressourcen-Inventar (Compute, Storage, Network, DB)
    - Netzwerk-Architektur (VPC, Subnets, Security Groups)
    - DNS- und Domain-Management
    - Infrastruktur-Änderungsprozess

    **Inhaltliche Tiefe:** Architekturdiagramm als Mermaid oder ASCII. Terraform-Modul-Übersicht. Inventar-Tabelle.

    **Abgrenzung:** Keine Deployment-Prozesse (→ operations/deployment.md), keine Netzwerk-Details (→ operations/network.md).

    **Beispiel-Inhalte:** Mermaid-Diagramm: Load Balancer → App-Server (x3) → DB (Primary + Replica), Terraform: `module 'app' { source = './modules/app' instance_type = 't3.medium' }`, Inventar: Region eu-central-1, 3 EC2, 1 RDS, 1 ElastiCache.

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
    **Zielgruppe:** Ops-Teams, Systemadministratoren

    **Pflicht-Abschnitte:**

    - Regelmäßige Wartungsaufgaben (Tabelle: Aufgabe, Frequenz, Verantwortlich)
    - OS- und Paket-Updates (Patch-Strategie)
    - Zertifikatserneuerung (Automatisierung, Monitoring)
    - Datenbank-Wartung (VACUUM, ANALYZE, Index-Rebuild)
    - Log-Rotation und Speicher-Bereinigung
    - Maintenance-Window-Planung und Kommunikation
    - Automatisierungsgrad und Verbesserungspotential

    **Inhaltliche Tiefe:** Vollständiger Wartungskalender. Befehle pro Aufgabe. Automatisierungsskript-Verweise.

    **Abgrenzung:** Keine Incident-Behandlung (→ operations/runbooks.md), keine Kapazitätsplanung (→ operations/capacity-planning.md).

    **Beispiel-Inhalte:** Tabelle: 'DB VACUUM — wöchentlich — DBA', 'Zertifikate prüfen — monatlich — Ops', Befehl: `certbot renew --dry-run`, Log-Rotation: `logrotate -d /etc/logrotate.d/myapp`.

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
    **Zielgruppe:** Ops-Teams, Architekten, Management

    **Pflicht-Abschnitte:**

    - Aktuelle Ressourcenauslastung (CPU, RAM, Disk, Network)
    - Wachstumsprognosen (Benutzer, Daten, Requests)
    - Kapazitätsgrenzen pro Komponente
    - Skalierungs-Trigger und Schwellenwerte
    - Kostenmodell pro Skalierungsstufe
    - Planungs-Zyklus und Review-Termine
    - Reservierte vs. On-Demand-Ressourcen

    **Inhaltliche Tiefe:** Tabellen mit aktuellen und projizierten Werten. Grafik-Beschreibung für Trends. Kosten-Vergleichstabelle.

    **Abgrenzung:** Keine Skalierungskonfiguration (→ operations/scaling.md), keine Kostenoptimierung (→ operations/cost-optimization.md).

    **Beispiel-Inhalte:** Tabelle: Komponente | Aktuell | 6 Monate | 12 Monate, DB: 50 GB | 80 GB | 120 GB, Trigger: 'CPU > 70% über 7 Tage → Skalierungsticket erstellen', Review: Quartalsweise im Ops-Meeting.

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
    **Zielgruppe:** Ops-Teams, Backend-Entwickler

    **Pflicht-Abschnitte:**

    - Logging-Architektur (Collection, Shipping, Storage, Visualization)
    - Log-Formate und Standardisierung (JSON, Syslog)
    - Zentrale Log-Aggregation (ELK, Loki, Fluentd)
    - Retention-Policies pro Log-Typ
    - Log-Indexierung und Suche
    - Compliance-Anforderungen (Aufbewahrungspflicht, DSGVO)
    - Kosten-Management bei hohem Log-Volumen

    **Inhaltliche Tiefe:** Vollständige Pipeline-Konfiguration. Retention-Tabelle. Kosten-Schätzung pro GB/Monat.

    **Abgrenzung:** Keine Entwickler-Logging-Regeln (→ development/logging-guide.md), keine Monitoring-Strategie (→ operations/monitoring.md).

    **Beispiel-Inhalte:** Pipeline: App → Fluentd → Elasticsearch → Kibana, Retention: Access-Logs 30 Tage, Audit-Logs 365 Tage, Debug-Logs 7 Tage, Fluentd-Config: `<match app.**> @type elasticsearch host es:9200 </match>`.

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
    **Zielgruppe:** Netzwerk-Ingenieure, Ops-Teams, Security-Team

    **Pflicht-Abschnitte:**

    - Netzwerk-Topologie-Diagramm
    - VPC/Subnet-Layout und CIDR-Bereiche
    - Firewall-Regeln und Security Groups
    - Load-Balancer-Konfiguration (Layer 4/7)
    - DNS-Konfiguration (intern, extern, Service Discovery)
    - VPN- und Bastion-Host-Zugang
    - Netzwerk-Troubleshooting-Befehle

    **Inhaltliche Tiefe:** Vollständiges Topologie-Diagramm. Firewall-Regeln als Tabelle. DNS-Record-Übersicht.

    **Abgrenzung:** Keine CDN-Konfiguration (→ integrations/cdn.md), keine Infrastruktur-Provisionierung (→ operations/infrastructure.md).

    **Beispiel-Inhalte:** Subnet-Tabelle: public-a 10.0.1.0/24, private-a 10.0.10.0/24, Security Group: Ingress 443/tcp von 0.0.0.0/0, Egress all, DNS: `app.internal → 10.0.10.5 (A-Record)`, Debug: `dig app.internal`, `traceroute`, `curl -v`.

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
    **Zielgruppe:** On-Call-Ingenieure, SREs, Ops-Teams

    **Pflicht-Abschnitte:**

    - Alert-Regeln-Übersicht (Tabelle: Name, Bedingung, Severity, Empfänger)
    - Alert-Severity-Definitionen (Critical, Warning, Info)
    - Eskalationsrichtlinien pro Severity
    - Alert-Routing (Wer wird wann benachrichtigt)
    - Silencing und Maintenance-Windows
    - Alert-Tuning (False Positives reduzieren)
    - Runbook-Verlinkung pro Alert

    **Inhaltliche Tiefe:** Vollständige Alert-Rule-Definitionen (Prometheus/Grafana). Eskalations-Timeline pro Severity.

    **Abgrenzung:** Keine Monitoring-Strategie (→ operations/monitoring.md), keine Runbook-Details (→ operations/runbooks.md).

    **Beispiel-Inhalte:** Prometheus: `alert: HighErrorRate expr: rate(http_errors_total[5m]) > 0.05 for: 5m`, Severity: Critical → PagerDuty sofort, Warning → Slack #ops, Info → Dashboard, Silence: `amtool silence add alertname=HighCPU --duration=2h --comment='Deployment'`.

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
    **Zielgruppe:** Ops-Teams, Management, Finanzabteilung

    **Pflicht-Abschnitte:**

    - Aktuelle Kostenübersicht (pro Kategorie: Compute, Storage, Network, Lizenzen)
    - Kostenanalyse-Tools und Dashboards
    - Optimierungsmaßnahmen (Reserved Instances, Spot/Preemptible, Right-Sizing)
    - Ressourcen-Tagging-Strategie für Kostenzuordnung
    - Automatische Abschaltung (Dev/Staging außerhalb Geschäftszeiten)
    - Storage-Tiering und Lifecycle-Policies
    - Kosten-Alerts und Budgets

    **Inhaltliche Tiefe:** Konkrete Einsparpotentiale mit Zahlen. Implementierungs-Checkliste pro Maßnahme.

    **Abgrenzung:** Keine Kapazitätsplanung (→ operations/capacity-planning.md), keine Infrastruktur-Details (→ operations/infrastructure.md).

    **Beispiel-Inhalte:** Right-Sizing: 't3.xlarge → t3.large' spart 50%/Monat, Reserved: 1-Jahr-Reservierung spart 30% vs. On-Demand, Auto-Off: `aws lambda` schaltet Dev-Umgebung 20:00–08:00 ab, Tags: `team: backend, env: prod, service: api`.

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
    **Zielgruppe:** On-Call-Ingenieure, Team-Leads, Management

    **Pflicht-Abschnitte:**

    - On-Call-Rotationsplan (Wochenrhythmus, Primär/Sekundär)
    - Verantwortlichkeiten im Bereitschaftsdienst
    - Eskalationspfade und Kontaktdaten
    - Reaktionszeiten pro Severity (SLA)
    - On-Call-Tools (PagerDuty, OpsGenie, Telefon)
    - Handover-Prozess (Übergabe Schichtende)
    - Kompensation und Work-Life-Balance-Regeln
    - Post-Incident-Review-Pflicht

    **Inhaltliche Tiefe:** Vollständiger Rotationsplan-Beispiel. SLA-Tabelle. Handover-Template.

    **Abgrenzung:** Keine Runbook-Details (→ operations/runbooks.md), keine Alert-Regeln (→ operations/monitoring-alerts.md).

    **Beispiel-Inhalte:** Rotation: Woche 1 → Alice (Primär), Bob (Sekundär), SLA: Critical → Reaktion in 15 Min, Warning → 1 Stunde, Handover: 'Offene Incidents, bekannte Probleme, geplante Deployments', Tool: PagerDuty-App auf Diensthandy, Lautstärke auf Maximum.

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
    **Zielgruppe:** Ops-Teams, Entwickler, Management

    **Pflicht-Abschnitte:**

    - Change-Typen (Standard, Normal, Emergency)
    - Change-Request-Prozess (Antrag, Review, Genehmigung)
    - Change-Advisory-Board (CAB) und Entscheidungskriterien
    - Risikobewertung pro Change (Impact, Wahrscheinlichkeit)
    - Change-Windows und Freeze-Perioden
    - Rollback-Plan als Pflichtbestandteil
    - Post-Implementation-Review
    - Change-Log und Audit-Trail

    **Inhaltliche Tiefe:** Change-Request-Template vollständig. Risiko-Matrix. Entscheidungsbaum für Change-Typ.

    **Abgrenzung:** Keine Deployment-Details (→ operations/deployment.md), keine Incident-Management-Prozesse (→ operations/runbooks.md).

    **Beispiel-Inhalte:** Template: Titel, Beschreibung, Betroffene Systeme, Risiko (Low/Medium/High), Rollback-Plan, Genehmiger. Standard-Change: 'Dependency-Update mit bestehenden Tests' → kein CAB nötig. Emergency-Change: 'Security-Patch' → Post-hoc CAB-Review innerhalb 48h.

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
    **Zielgruppe:** Projektleitung, Compliance-Beauftragte, Auditoren, Geschäftsführung

    **Pflicht-Abschnitte:**

    - Übersicht aller regulatorischen Anforderungen (DSGVO, ISO 27001, branchenspezifische Normen)
    - Compliance-Matrix: Anforderung → Maßnahme → Verantwortlicher → Status
    - Zeitplan für Audits und Zertifizierungen
    - Eskalationspfade bei Compliance-Verstößen
    - Links zu allen Detail-Seiten im Compliance-Bereich

    **Inhaltliche Tiefe:** Strategische Übersicht mit Verlinkung auf Detail-Seiten; tabellarische Compliance-Matrix; Status-Ampelsystem (grün/gelb/rot) für jede Anforderung

    **Abgrenzung:** Keine vollständigen Richtlinientexte hier → `compliance/security-policies.md`; keine technischen Implementierungsdetails → `architecture/security.md`

    **Beispiel-Inhalte:** Tabelle mit Spalten: Regulierung | Geltungsbereich | Verantwortlich | Nächstes Audit | Status; Übersichtsgrafik des Compliance-Frameworks

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
    **Zielgruppe:** Datenschutzbeauftragte, Entwickler, Projektleitung, Rechtsabteilung

    **Pflicht-Abschnitte:**

    - Verzeichnis der Verarbeitungstätigkeiten (Art. 30 DSGVO)
    - Rechtsgrundlagen je Datenverarbeitung (Einwilligung, Vertrag, berechtigtes Interesse)
    - Technisch-organisatorische Maßnahmen (TOMs)
    - Betroffenenrechte und deren technische Umsetzung (Auskunft, Löschung, Portabilität)
    - Datenschutz-Folgenabschätzung (DSFA) bei Hochrisiko-Verarbeitungen
    - Auftragsverarbeitungsverträge (AVV) mit Dienstleistern

    **Inhaltliche Tiefe:** Juristisch korrekte Formulierungen; Verweis auf konkrete DSGVO-Artikel; Datenflussdiagramme mit Kennzeichnung personenbezogener Daten

    **Abgrenzung:** Keine allgemeinen Sicherheitsmaßnahmen → `compliance/security-policies.md`; keine Aufbewahrungsfristen → `compliance/data-retention.md`

    **Beispiel-Inhalte:** Tabelle: Datenart | Rechtsgrundlage | Speicherort | Löschfrist | Verantwortlicher; Datenflussdiagramm mit markierten PII-Feldern

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
    **Zielgruppe:** Auditoren, DevOps-Ingenieure, Compliance-Beauftragte, Systemadministratoren

    **Pflicht-Abschnitte:**

    - Audit-Log-Architektur und erfasste Ereignisse
    - Unveränderlichkeit und Integritätssicherung der Logs (Hashing, WORM-Speicher)
    - Aufbewahrungsdauer und Archivierung von Audit-Daten
    - Zugriffskontrolle auf Audit-Logs (Wer darf lesen, niemand darf löschen)
    - Suchmöglichkeiten und Reporting auf Audit-Daten
    - Regelmäßige Audit-Prüfzyklen und verantwortliche Rollen

    **Inhaltliche Tiefe:** Technisch präzise: Log-Formate, Speicherorte, Retention-Policies; Beispielabfragen für typische Audit-Szenarien; Sequenzdiagramme für Audit-Event-Flow

    **Abgrenzung:** Keine operativen Monitoring-Metriken → `operations/monitoring.md`; keine Incident-Prozesse → `compliance/incident-response.md`

    **Beispiel-Inhalte:** JSON-Beispiel eines Audit-Log-Eintrags; Tabelle: Ereignistyp | Erfasste Felder | Aufbewahrungsdauer; Diagramm der Audit-Pipeline

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
    **Zielgruppe:** Projektleitung, Kunden, Operations-Team, Support-Leitung

    **Pflicht-Abschnitte:**

    - SLA-Definitionen je Service-Tier (z.B. Gold, Silber, Bronze)
    - Verfügbarkeitsziele (z.B. 99,9 %) und deren Berechnung
    - Reaktions- und Lösungszeiten je Prioritätsstufe
    - Messmethodik und Ausschlüsse (geplante Wartung, höhere Gewalt)
    - Eskalationsprozeduren bei SLA-Verletzung
    - Kompensationsregelungen (Service-Credits)

    **Inhaltliche Tiefe:** Exakte Zahlenwerte und Formeln; Unterscheidung zwischen Verfügbarkeit, Performance und Support-SLAs; monatliche SLA-Berichtsvorlage

    **Abgrenzung:** Keine technischen Monitoring-Details → `operations/monitoring.md`; keine Incident-Prozesse → `compliance/incident-response.md`

    **Beispiel-Inhalte:** Tabelle: Priorität | Reaktionszeit | Lösungszeit | Eskalation; Formel: Verfügbarkeit = (Gesamtzeit − Ausfallzeit) / Gesamtzeit × 100

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
    **Zielgruppe:** Alle Entwickler, Systemadministratoren, Sicherheitsbeauftragte, Geschäftsführung

    **Pflicht-Abschnitte:**

    - Passwort- und Authentifizierungsrichtlinien (Länge, Komplexität, MFA-Pflicht)
    - Netzwerksicherheit (Firewall-Regeln, VPN-Pflicht, Segmentierung)
    - Verschlüsselungsstandards (TLS-Versionen, Algorithmen, Schlüssellängen)
    - Zugriffskontrollmodell (RBAC/ABAC, Least-Privilege-Prinzip)
    - Sichere Entwicklungsrichtlinien (OWASP Top 10, Code-Review-Pflicht)
    - Physische Sicherheit und Gerätemanagement

    **Inhaltliche Tiefe:** Verbindlich formulierte Richtlinien mit MUSS/SOLL/KANN; konkrete technische Parameter; Verweise auf angewandte Standards (ISO 27001, BSI-Grundschutz)

    **Abgrenzung:** Keine Incident-Prozesse → `compliance/incident-response.md`; keine Datenschutz-Themen → `compliance/data-protection.md`

    **Beispiel-Inhalte:** Richtlinie: „Passwörter MÜSSEN mindestens 14 Zeichen lang sein und MFA ist für alle Produktionsumgebungen PFLICHT"; Tabelle erlaubter TLS-Cipher-Suites

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
    **Zielgruppe:** Security-Team, DevOps, Projektleitung, Kommunikationsabteilung

    **Pflicht-Abschnitte:**

    - Incident-Klassifizierung (Schweregrade SEV1–SEV4 mit Beispielen)
    - Meldekette und Benachrichtigungsfristen (intern + DSGVO 72h-Frist)
    - Sofortmaßnahmen je Schweregrad (Containment, Eradication, Recovery)
    - Rollen und Verantwortlichkeiten im Incident-Response-Team
    - Kommunikationsvorlagen (intern, Kunden, Behörden)
    - Post-Incident-Review und Lessons-Learned-Prozess

    **Inhaltliche Tiefe:** Schritt-für-Schritt-Ablauf als Checkliste; Entscheidungsbäume für Klassifizierung; Kontaktlisten mit Erreichbarkeit (24/7-Rufbereitschaft)

    **Abgrenzung:** Keine allgemeinen Sicherheitsrichtlinien → `compliance/security-policies.md`; kein operatives Monitoring → `operations/monitoring.md`

    **Beispiel-Inhalte:** Flowchart: Incident erkannt → Klassifizierung → Containment → Analyse → Behebung → Review; Vorlage für Behördenmeldung nach Art. 33 DSGVO

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
    **Zielgruppe:** Datenschutzbeauftragte, Datenbankadministratoren, Compliance-Beauftragte

    **Pflicht-Abschnitte:**

    - Aufbewahrungsfristen je Datenkategorie (Geschäftsdaten, Logdaten, Personaldaten, Kundendaten)
    - Gesetzliche Grundlagen je Frist (HGB, AO, DSGVO, branchenspezifisch)
    - Löschmechanismen und -automatisierung (Soft-Delete, Hard-Delete, Anonymisierung)
    - Archivierungsstrategie (Warm/Cold-Storage, Zugriff auf archivierte Daten)
    - Nachweispflicht: Dokumentation durchgeführter Löschungen

    **Inhaltliche Tiefe:** Tabellarische Übersicht mit exakten Fristen; technische Beschreibung der Lösch-Jobs; Unterscheidung zwischen Löschung und Anonymisierung

    **Abgrenzung:** Keine Backup-Strategien → `operations/backup-recovery.md`; keine DSGVO-Betroffenenrechte → `compliance/data-protection.md`

    **Beispiel-Inhalte:** Tabelle: Datenkategorie | Aufbewahrungsfrist | Gesetzliche Grundlage | Löschmethode | Automatisiert; Cron-Job-Konfiguration für automatische Löschung

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
    **Zielgruppe:** Einkauf, Compliance-Beauftragte, Architekten, Projektleitung

    **Pflicht-Abschnitte:**

    - Bewertungskriterien für Drittanbieter (Sicherheit, Datenschutz, Verfügbarkeit, Finanzkraft)
    - Risikokategorisierung (niedrig/mittel/hoch/kritisch) mit Schwellenwerten
    - Due-Diligence-Checkliste vor Beauftragung
    - Vertragliche Anforderungen (AVV, SLA, Audit-Rechte, Exit-Klauseln)
    - Regelmäßige Neubewertung und Monitoring laufender Anbieter
    - Notfallplan bei Ausfall eines kritischen Anbieters

    **Inhaltliche Tiefe:** Strukturierte Bewertungsbögen mit Punktesystem; Entscheidungsmatrix für Anbieterauswahl; Vertragsklausel-Vorlagen

    **Abgrenzung:** Keine Lizenz-Compliance → `compliance/licensing-compliance.md`; keine SLA-Details → `compliance/sla.md`

    **Beispiel-Inhalte:** Bewertungsmatrix: Anbieter | Sicherheitszertifikate | Datenschutzniveau | Abhängigkeitsgrad | Risikostufe; Checkliste mit 20+ Prüfpunkten für Due Diligence

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
    **Zielgruppe:** Entwickler, Designer, Projektleitung, Rechtsabteilung

    **Pflicht-Abschnitte:**

    - Geltende Gesetze (BITV 2.0, EU-Richtlinie 2016/2102, EAA/European Accessibility Act)
    - Anwendungsbereich und betroffene Systeme
    - Fristen und Übergangsregelungen
    - Pflichtdokumentation (Barrierefreiheitserklärung, Feedback-Mechanismus)
    - Prüfverfahren und Zertifizierung (BITV-Test, externe Audits)
    - Konsequenzen bei Nichteinhaltung

    **Inhaltliche Tiefe:** Juristische Anforderungen mit Gesetzesverweisen; Zuordnung zu WCAG-Kriterien → `design/accessibility-guidelines.md`; Zeitplan für Umsetzung

    **Abgrenzung:** Keine technischen WCAG-Details → `design/accessibility-guidelines.md`; keine Test-Ergebnisse → `testing/accessibility-tests.md`

    **Beispiel-Inhalte:** Zeitstrahl: Gesetzesfristen und interne Meilensteine; Vorlage für die Barrierefreiheitserklärung nach EU-Muster

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
    **Zielgruppe:** Entwickler, Architekten, Rechtsabteilung, Open-Source-Beauftragte

    **Pflicht-Abschnitte:**

    - Inventar aller verwendeten Open-Source-Bibliotheken mit Lizenztyp
    - Lizenzkompatibilitätsmatrix (MIT, Apache 2.0, GPL, LGPL, AGPL, MPL)
    - Pflichten je Lizenztyp (Attribution, Quellcode-Offenlegung, Copyleft)
    - SBOM-Erstellung (Software Bill of Materials) und Aktualisierungsprozess
    - Genehmigungsprozess für neue Abhängigkeiten
    - Verbotene Lizenzen und Ausnahmen

    **Inhaltliche Tiefe:** Vollständige SBOM-Tabelle; Entscheidungsbaum für Lizenzkompatibilität; automatisierte Prüfung via CI/CD-Pipeline (z.B. FOSSA, Snyk)

    **Abgrenzung:** Keine Projekt-Lizenz → `reference/license.md`; keine Drittanbieter-Risiken → `compliance/third-party-risk.md`

    **Beispiel-Inhalte:** SBOM-Tabelle: Bibliothek | Version | Lizenz | Copyleft | Kompatibel; Entscheidungsbaum: „Ist die Lizenz GPL-kompatibel? → Ja/Nein → nächster Schritt"

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
    **Zielgruppe:** Geschäftsführung, Vertrieb, Compliance-Beauftragte, Entwickler (Kryptographie)

    **Pflicht-Abschnitte:**

    - Relevante Exportkontrollvorschriften (EU Dual-Use-VO, US EAR/ITAR falls zutreffend)
    - Klassifizierung der Software nach Güterlisten (AL, EKL, ECCN)
    - Kryptographie-Exportbeschränkungen und Ausnahmen
    - Embargolisten und Screening-Prozess für Endkunden
    - Dokumentationspflichten und Genehmigungsverfahren
    - Schulungspflichten für betroffene Mitarbeiter

    **Inhaltliche Tiefe:** Konkrete Einordnung der eigenen Software; Checkliste für Vertrieb vor Auslandsgeschäften; Verweis auf aktuelle Sanktionslisten (EU, UN, OFAC)

    **Abgrenzung:** Keine Lizenz-Themen → `compliance/licensing-compliance.md`; keine allgemeine Rechtsberatung

    **Beispiel-Inhalte:** Checkliste: „Verwendet die Software Verschlüsselung > 56 Bit? → Prüfung auf Listung erforderlich"; Tabelle: Zielland | Sanktionsstatus | Genehmigung erforderlich

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
    **Zielgruppe:** Neue Teammitglieder, HR, Teamleitung, Buddy/Mentor

    **Pflicht-Abschnitte:**

    - Onboarding-Checkliste: Tag 1, Woche 1, Monat 1 (mit Verantwortlichkeiten)
    - Zugänge und Accounts: welche Systeme, wer beantragt, Bearbeitungszeit
    - Entwicklungsumgebung einrichten: Schritt-für-Schritt-Anleitung
    - Architektur-Überblick für Neueinsteiger (vereinfachtes Diagramm)
    - Ansprechpartner und Buddy-System
    - Erste Aufgaben (Good-First-Issues, Pair-Programming-Sessions)

    **Inhaltliche Tiefe:** Konkrete Checkliste mit Checkboxen; Links zu relevanten Wiki-Seiten; Zeitschätzungen pro Schritt; Feedback-Meilensteine (nach 2 Wochen, nach 1 Monat)

    **Abgrenzung:** Keine vollständige Entwicklerdoku → `generated/developer/`; keine Projektübersicht → `project/overview.md`

    **Beispiel-Inhalte:** Tag 1: Laptop einrichten, Slack beitreten, Git-Zugang erhalten; Woche 1: Architektur-Walkthrough, erstes PR erstellen; Monat 1: eigenständige Feature-Entwicklung

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
    **Zielgruppe:** Entwickler, QA-Ingenieure, Product Owner, Scrum Master

    **Pflicht-Abschnitte:**

    - Definition of Done für User Stories (Code, Tests, Review, Doku)
    - Definition of Done für Sprints (alle Stories abgenommen, Deployment-bereit)
    - Definition of Done für Releases (Regressionstests, Performance-Check, Release-Notes)
    - Qualitäts-Gates: was muss erfüllt sein, bevor der nächste Schritt erlaubt ist
    - Ausnahmen und Umgang mit technischer Schuld

    **Inhaltliche Tiefe:** Klare Checklisten je Ebene; messbare Kriterien (z.B. „Code-Coverage ≥ 80 %"); Beispiele für „Done" vs. „Nicht Done"

    **Abgrenzung:** Keine einzelnen Testfälle → `testing/test-cases.md`; keine Prozessbeschreibung → `project/overview.md`

    **Beispiel-Inhalte:** Story-DoD: Code geschrieben → Unit-Tests ≥ 80 % → Code-Review bestanden → Dokumentation aktualisiert → QA abgenommen → In Staging deployed

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
    **Zielgruppe:** Projektleitung, Stakeholder, Kommunikationsverantwortliche, gesamtes Team

    **Pflicht-Abschnitte:**

    - Kommunikationsmatrix: Zielgruppe → Kanal → Frequenz → Inhalt → Verantwortlicher
    - Interne Kommunikation: Slack-Channels, E-Mail-Verteiler, Wiki-Bereiche
    - Externe Kommunikation: Kunden-Updates, Stakeholder-Reports, Release-Ankündigungen
    - Eskalationskommunikation: wer informiert wen bei Problemen
    - Status-Reporting: Vorlage und Rhythmus (wöchentlich, monatlich)
    - Dokumentationsstandards: wo wird was festgehalten

    **Inhaltliche Tiefe:** Vollständige Kommunikationsmatrix als Tabelle; Vorlagen für Status-Reports; Kanal-Übersicht mit Zweck und Regeln

    **Abgrenzung:** Keine Stakeholder-Details → `project/stakeholders.md`; keine Meeting-Agenden → `project/meetings.md`

    **Beispiel-Inhalte:** Matrix: Stakeholder-Gruppe | Kanal | Frequenz | Inhalt | Verantwortlich; Vorlage: „Wöchentlicher Status: Fortschritt | Risiken | Nächste Schritte"

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
    **Zielgruppe:** Endanwender, Entwickler, Support-Team, neue Teammitglieder

    **Pflicht-Abschnitte:**

    - FAQ nach Kategorien geordnet (Allgemein, Installation, Konfiguration, Fehlerbehebung, Lizenzierung)
    - Je Frage: klare, kurze Antwort mit weiterführendem Link
    - Häufigste Support-Anfragen als Top-10
    - Suchfunktion oder Inhaltsverzeichnis für schnellen Zugriff

    **Inhaltliche Tiefe:** Praxisnahe Fragen aus echtem Support-Aufkommen; Code-Snippets wo hilfreich; max. 5 Sätze pro Antwort, dann Verweis auf Detail-Seite

    **Abgrenzung:** Keine vollständigen Anleitungen → spezifische Doku-Seiten; keine Fehlercodes → `reference/error-codes.md`

    **Beispiel-Inhalte:** F: „Wie setze ich mein Passwort zurück?" A: „Klicken Sie auf ‚Passwort vergessen' auf der Login-Seite. Sie erhalten eine E-Mail mit Zurücksetzungslink."

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
    **Zielgruppe:** Entwickler, Systemadministratoren, Support-Team

    **Pflicht-Abschnitte:**

    - Problemkategorien (Installation, Verbindung, Performance, Authentifizierung, Daten)
    - Je Problem: Symptom → Ursache → Lösung (strukturiertes Format)
    - Diagnose-Tools und -Befehle (Log-Dateien, Debug-Modus, Health-Checks)
    - Entscheidungsbaum für häufige Problemsituationen
    - Eskalationspfade wenn Selbsthilfe nicht ausreicht

    **Inhaltliche Tiefe:** Reproduzierbare Lösungsschritte mit Befehlen; Log-Ausgabe-Beispiele mit Erklärung; Verlinkung zu relevanten Konfigurationsseiten

    **Abgrenzung:** Keine Fehlercodes → `reference/error-codes.md`; keine bekannten Einschränkungen → `reference/known-issues.md`

    **Beispiel-Inhalte:** Problem: „Verbindung zur Datenbank schlägt fehl" → Prüfung: `telnet db-host 5432` → Ursache: Firewall blockiert → Lösung: Port freigeben

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
    **Zielgruppe:** Entwickler, Support-Team, Systemadministratoren

    **Pflicht-Abschnitte:**

    - Fehlercode-Schema und Namenskonvention (z.B. E-AUTH-001, E-DB-042)
    - Vollständige Fehlercode-Tabelle: Code | Nachricht | Beschreibung | Lösung
    - HTTP-Statuscodes und deren projektspezifische Bedeutung
    - Fehlercode-Bereiche je Modul/Subsystem
    - Logging-Level-Zuordnung je Fehlercode (ERROR, WARN, INFO)

    **Inhaltliche Tiefe:** Jeder Fehlercode mit konkreter Lösungsanweisung; Suchbare Tabelle; Beispiel-Fehlermeldung wie sie dem Nutzer angezeigt wird

    **Abgrenzung:** Keine Fehlerbehebungs-Anleitungen → `reference/troubleshooting.md`; keine API-Fehlermeldungen → API-Dokumentation

    **Beispiel-Inhalte:** E-AUTH-001 | „Ungültige Anmeldedaten" | Benutzername oder Passwort falsch | Lösung: Passwort zurücksetzen; HTTP 429: Rate-Limit überschritten

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
    **Zielgruppe:** Entwickler, DevOps-Ingenieure, Systemadministratoren

    **Pflicht-Abschnitte:**

    - Vollständige Liste aller Umgebungsvariablen
    - Je Variable: Name, Beschreibung, Typ, Pflicht/Optional, Standardwert, Beispielwert
    - Gruppierung nach Subsystem (Datenbank, Cache, Auth, Logging, Feature-Flags)
    - Validierungsregeln und erlaubte Wertemenge
    - Sicherheitshinweise: welche Variablen geheim sind (Secrets)
    - `.env.example`-Datei als Vorlage

    **Inhaltliche Tiefe:** Tabellarische Referenz; Typ-Angaben (string, int, bool, URL); Wechselwirkungen zwischen Variablen dokumentieren

    **Abgrenzung:** Keine Konfigurationsdateien → `reference/configuration-reference.md`; keine Deployment-Anleitungen → `operations/`

    **Beispiel-Inhalte:** `DATABASE_URL` | PostgreSQL Connection String | Pflicht | — | `postgres://user:pass@localhost:5432/mydb` | SECRET

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
    **Zielgruppe:** Entwickler, QA-Ingenieure, Support-Team, Product Owner

    **Pflicht-Abschnitte:**

    - Liste bekannter Einschränkungen und Bugs mit Status
    - Je Eintrag: ID, Beschreibung, betroffene Version, Schweregrad, Workaround, geplante Behebung
    - Kategorisierung (UI, API, Performance, Sicherheit, Kompatibilität)
    - Verknüpfung mit Issue-Tracker (Jira/GitHub-Issue-Nummer)
    - Wann zuletzt aktualisiert

    **Inhaltliche Tiefe:** Konkrete Reproduktionsschritte für jeden Bug; Workarounds mit Code-Beispielen wo möglich; Zeitplan für Fixes

    **Abgrenzung:** Keine behobenen Bugs → `reference/changelog.md`; keine allgemeine Fehlerbehebung → `reference/troubleshooting.md`

    **Beispiel-Inhalte:** KI-023: „CSV-Export bricht bei > 10.000 Zeilen ab" | v2.3 | Hoch | Workaround: Daten in Batches exportieren | Fix geplant: v2.5

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
    **Zielgruppe:** Entwickler, DevOps-Ingenieure, Systemadministratoren

    **Pflicht-Abschnitte:**

    - Migrations-Übersicht: von welcher Version zu welcher Version
    - Voraussetzungen und Backup-Empfehlung vor Migration
    - Schritt-für-Schritt-Anleitung (mit Befehlen und Konfigurationsänderungen)
    - Breaking Changes: was sich geändert hat und wie der Code angepasst werden muss
    - Datenbank-Migrationen: Schema-Änderungen, Datenmigrationsskripte
    - Rollback-Plan falls die Migration fehlschlägt
    - Verifikation: wie prüft man, ob die Migration erfolgreich war

    **Inhaltliche Tiefe:** Exakte Befehle mit Versions-Parametern; Vorher-Nachher-Code-Vergleiche für Breaking Changes; geschätzte Ausfallzeit; Checkliste

    **Abgrenzung:** Keine Versionshistorie → `reference/changelog.md`; keine allgemeine Konfiguration → `reference/configuration-reference.md`

    **Beispiel-Inhalte:** Migration v2→v3: 1. Backup erstellen, 2. `npm install @app/core@3.0`, 3. `config.yml` aktualisieren (Auth-Sektion umbenannt), 4. DB-Migration ausführen

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
    **Zielgruppe:** Alle Projektbeteiligten, neue Teammitglieder, Fachbereich

    **Pflicht-Abschnitte:**

    - Alphabetisch sortiertes Verzeichnis aller Fachbegriffe
    - Je Begriff: Definition, Kontext/Verwendung im Projekt, Synonyme
    - Unterscheidung zwischen fachlichen und technischen Begriffen
    - Abkürzungsverzeichnis (Akronyme mit Auflösung)

    **Inhaltliche Tiefe:** Kurze, präzise Definitionen (1–3 Sätze); Verlinkung zu relevanten Doku-Seiten; konsistente Verwendung im gesamten Projekt sicherstellen

    **Abgrenzung:** Keine vollständigen Erklärungen → spezifische Doku-Seiten; kein allgemeines IT-Glossar, nur projektrelevante Begriffe

    **Beispiel-Inhalte:** **Tenant** – Ein isolierter Mandant im Multi-Tenancy-System. Jeder Tenant hat eigene Daten und Konfiguration. Siehe: `architecture/data-model.md`

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
    **Zielgruppe:** Entwickler, Product Owner, Kunden, Support-Team

    **Pflicht-Abschnitte:**

    - Versionshistorie in umgekehrt chronologischer Reihenfolge (neueste zuerst)
    - Je Version: Versionsnummer, Datum, Kategorien (Added, Changed, Fixed, Removed, Security)
    - Semantic Versioning erklären (Major.Minor.Patch)
    - Verlinkung zu zugehörigen Release Notes, Git-Tags, Merge-Requests
    - Breaking Changes klar hervorgehoben

    **Inhaltliche Tiefe:** Keep-a-Changelog-Format; entwicklerzentriert (technisch); jeder Eintrag verlinkt auf Issue/PR; automatisierte Generierung wo möglich

    **Abgrenzung:** Keine nutzerzentrierte Sprache → `reference/release-notes.md`; keine Migrationsanleitung → `reference/migration-guide.md`

    **Beispiel-Inhalte:** ## [2.5.0] - 2025-01-15 / Added: Multi-Tenant-Support (#234) / Fixed: CSV-Export bei großen Dateien (#189) / Breaking: Auth-Config-Key umbenannt

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
    **Zielgruppe:** Entwickler, DevOps-Ingenieure, Systemadministratoren

    **Pflicht-Abschnitte:**

    - Vollständige Referenz aller Konfigurationsdateien (YAML, JSON, TOML, INI)
    - Je Option: Schlüssel, Beschreibung, Typ, Standardwert, erlaubte Werte, Beispiel
    - Konfigurationshierarchie: Datei → Umgebungsvariable → CLI-Flag (Priorität)
    - Validierungsregeln und Fehlermeldungen bei ungültiger Konfiguration
    - Minimal-Konfiguration vs. vollständige Konfiguration

    **Inhaltliche Tiefe:** Vollständige kommentierte Beispiel-Konfigurationsdatei; Typ-Angaben und Constraints; Seiteneffekte bei Kombinationen dokumentieren

    **Abgrenzung:** Keine Umgebungsvariablen → `reference/env-variables.md`; keine Deployment-Anleitung → `operations/`

    **Beispiel-Inhalte:** `server.port` | int | 8080 | 1024–65535 | HTTP-Port des Servers; Beispiel: vollständige `config.yml` mit Kommentaren

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
    **Zielgruppe:** Projektleitung, Administratoren, Sicherheitsbeauftragte, Entwickler

    **Pflicht-Abschnitte:**

    - Rollen-Definitionen (Admin, Manager, User, Guest, Service-Account)
    - Berechtigungs-Matrix: Rolle × Ressource × Aktion (Lesen, Schreiben, Löschen, Admin)
    - Feingranulare Berechtigungen je Modul/Feature
    - Rollenvererbung und -hierarchie
    - Sonderfälle: Tenant-übergreifende Berechtigungen, API-Key-Scopes
    - Änderungsprozess für Berechtigungen

    **Inhaltliche Tiefe:** Vollständige Matrix als Tabelle; RBAC-Modell-Diagramm; Code-Beispiele für Berechtigungsprüfung; Audit-Anforderungen

    **Abgrenzung:** Keine Sicherheitsrichtlinien → `compliance/security-policies.md`; keine API-Auth-Details → API-Dokumentation

    **Beispiel-Inhalte:** Matrix: Rolle | Benutzer verwalten | Reports lesen | Einstellungen ändern | Daten exportieren; Admin: ✓/✓/✓/✓; User: ✗/✓/✗/✓

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
    **Zielgruppe:** Kunden, Vertrieb, DevOps, Support-Team

    **Pflicht-Abschnitte:**

    - Unterstützte Betriebssysteme mit Versionsangaben
    - Unterstützte Browser und Mindestversionen
    - Hardware-Mindestanforderungen (CPU, RAM, Speicher)
    - Unterstützte Datenbanken und Versionen
    - Runtime-Anforderungen (Node.js, Python, Java-Version)
    - Support-Lifecycle: wie lange wird eine Plattform unterstützt nach EOL

    **Inhaltliche Tiefe:** Klare Tabellen mit Status (unterstützt, eingeschränkt, nicht unterstützt, abgekündigt); Datum der nächsten Abkündigung; empfohlene Konfiguration

    **Abgrenzung:** Keine Kompatibilitätstests → `testing/compatibility-tests.md`; keine Installationsanleitung → relevante Doku

    **Beispiel-Inhalte:** Tabelle: Plattform | Version | Status | Support-Ende; Linux Ubuntu 22.04: voll unterstützt bis 04/2027; Windows Server 2019: eingeschränkt

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
    **Zielgruppe:** Endanwender, Kunden, Product Owner, Marketing

    **Pflicht-Abschnitte:**

    - Versionsnummer und Veröffentlichungsdatum
    - Zusammenfassung der wichtigsten Neuerungen (nutzerzentriert formuliert)
    - Neue Features mit Beschreibung und ggf. Screenshots
    - Verbesserungen und Fehlerbehebungen (verständlich, nicht technisch)
    - Hinweise auf Breaking Changes oder erforderliche Aktionen
    - Update-Anleitung oder Verweis auf Migrations-Guide

    **Inhaltliche Tiefe:** Nutzerzentriert, nicht technisch; Bilder/GIFs für neue Features; klare Handlungsanweisungen bei Breaking Changes

    **Abgrenzung:** Keine technischen Details → `reference/changelog.md`; keine Migrationsschritte → `reference/migration-guide.md`

    **Beispiel-Inhalte:** „Neu in v2.5: Dashboard jetzt mit Echtzeit-Updates! Ihre Daten werden automatisch aktualisiert, ohne die Seite neu zu laden."

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
    **Zielgruppe:** Rechtsabteilung, Kunden, Open-Source-Community, Vertrieb

    **Pflicht-Abschnitte:**

    - Vollständiger Lizenztext des Projekts
    - Lizenztyp und wesentliche Bestimmungen in verständlicher Sprache
    - Rechte: was darf man mit der Software tun
    - Pflichten: was muss man beachten (Attribution, Copyleft)
    - Einschränkungen: was ist nicht erlaubt
    - Kontakt für Lizenzanfragen (kommerzielle Lizenzen, Sondergenehmigungen)

    **Inhaltliche Tiefe:** Vollständiger, unveränderter Lizenztext; zusätzlich eine Kurzfassung in verständlicher Sprache; SPDX-Identifier

    **Abgrenzung:** Keine Drittanbieter-Lizenzen → `compliance/licensing-compliance.md`; keine Vertragsbedingungen

    **Beispiel-Inhalte:** SPDX: MIT; Kurzfassung: „Sie dürfen die Software frei verwenden, kopieren und verändern, solange der Copyright-Vermerk erhalten bleibt."

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

    # ━━ Design-System ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ("design/overview.md", "Design-System — Überblick", """
!!! tip "Inhaltsrichtlinie"
    **Zielgruppe:** Designer, Frontend-Entwickler, Produktmanager, UX-Researcher

    **Pflicht-Abschnitte:**

    - Vision und Prinzipien des Design-Systems (Konsistenz, Wiederverwendbarkeit, Barrierefreiheit)
    - Übersicht aller Bestandteile (Tokens, Komponenten, Patterns, Vorlagen)
    - Governance: Wer pflegt das Design-System, Änderungsprozess, Versionierung
    - Tooling und Technologie-Stack (Figma, Storybook, CSS-Framework)
    - Adoptions-Roadmap und aktueller Reifegrad
    - Links zu allen Unterseiten des Design-Bereichs

    **Inhaltliche Tiefe:** Strategische Übersicht mit visuellen Beispielen; Architekturdiagramm des Design-Systems; Entscheidungsmatrix für Komponenten-Auswahl

    **Abgrenzung:** Keine einzelnen Komponenten-Details → `design/components.md`; keine Token-Werte → `design/tokens.md`

    **Beispiel-Inhalte:** Diagramm: Tokens → Komponenten → Patterns → Seitenvorlagen; Tabelle: Prinzip | Beschreibung | Beispiel

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
    **Zielgruppe:** Frontend-Entwickler, Designer, QA-Ingenieure

    **Pflicht-Abschnitte:**

    - Komponentenkatalog mit Kategorien (Navigation, Formulare, Feedback, Layout, Daten)
    - Je Komponente: Name, Beschreibung, Varianten, Props/API, Barrierefreiheit
    - Verwendungsrichtlinien (Do's and Don'ts) je Komponente
    - Status je Komponente (stabil, beta, deprecated)
    - Kompositionsmuster: wie Komponenten kombiniert werden

    **Inhaltliche Tiefe:** Vollständige API-Dokumentation je Komponente; Code-Beispiele in der verwendeten Framework-Syntax; Screenshots aller Varianten; ARIA-Attribute

    **Abgrenzung:** Keine Design-Token-Werte → `design/tokens.md`; keine Animations-Details → `design/animations.md`; keine Formular-Patterns → `design/forms.md`

    **Beispiel-Inhalte:** Komponente „Button": Varianten (primary, secondary, ghost, danger); Props-Tabelle: Prop | Typ | Default | Beschreibung; Code-Snippet

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
    **Zielgruppe:** Frontend-Entwickler, Designer, Design-System-Maintainer

    **Pflicht-Abschnitte:**

    - Farbpalette: Primär-, Sekundär-, Neutral-, Status-Farben (Hex, HSL, CSS-Variablen)
    - Typografie-Tokens: Schriftfamilien, Größen, Zeilenhöhen, Gewichte
    - Abstands-System (Spacing-Skala: 4px-Raster)
    - Schatten, Border-Radien, Z-Index-Skala
    - Breakpoints für Responsive Design
    - Token-Namenskonvention und Alias-System (semantisch → primitiv)

    **Inhaltliche Tiefe:** Vollständige Token-Tabellen mit Werten; Farbkontrast-Verhältnisse (WCAG AA/AAA); visuelle Beispiele für jede Token-Kategorie

    **Abgrenzung:** Keine Komponenten → `design/components.md`; kein Dark-Mode-Mapping → `design/dark-mode.md`

    **Beispiel-Inhalte:** Tabelle: Token-Name | Wert (Light) | Wert (Dark) | Verwendung; z.B. `--color-primary-500: #2563eb` → Haupt-CTA-Buttons

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
    **Zielgruppe:** Designer, Content-Ersteller, Marketing, Frontend-Entwickler

    **Pflicht-Abschnitte:**

    - Logo-Verwendung (Varianten, Schutzzone, Mindestgrößen, verbotene Modifikationen)
    - Bildsprache und Fotografie-Richtlinien
    - Tonalität und Schreibstil (formell/informell, Anredeform, Fachbegriffe)
    - Layout-Raster und Seitenaufbau-Prinzipien
    - Markenfarben im Kontext (Print vs. Digital, Kontrastvorgaben)
    - Konsistenzregeln für Texte (Datum, Zahlen, Abkürzungen)

    **Inhaltliche Tiefe:** Visuelle Beispiele für korrekte und falsche Anwendung; konkrete Textbeispiele für Tonalität; Checkliste für Review

    **Abgrenzung:** Keine technischen Token-Werte → `design/tokens.md`; keine Komponentenspezifikation → `design/components.md`

    **Beispiel-Inhalte:** Do/Don't-Gegenüberstellungen für Logo-Platzierung; Textbeispiel: „Sagen Sie ‚Speichern' statt ‚Submit'"; Raster-Overlay auf Beispielseite

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
    **Zielgruppe:** Frontend-Entwickler, Designer, QA-Ingenieure, Content-Ersteller

    **Pflicht-Abschnitte:**

    - WCAG 2.1 AA-Konformitätsziele und relevante Erfolgskriterien
    - Farbkontraste: Mindestverhältnisse (4.5:1 Text, 3:1 große Schrift, 3:1 UI-Elemente)
    - Tastaturnavigation: Fokusreihenfolge, Fokus-Indikatoren, Skip-Links
    - Screenreader-Unterstützung: ARIA-Rollen, Landmarks, Live-Regions
    - Alternativtexte für Bilder, Videos und andere Medien
    - Formulare: Labels, Fehlermeldungen, Gruppierung

    **Inhaltliche Tiefe:** Code-Beispiele für ARIA-Patterns; Kontrast-Checker-Tool-Empfehlungen; Checkliste je Komponente; Prüfverfahren mit assistiven Technologien

    **Abgrenzung:** Keine gesetzlichen Anforderungen → `compliance/accessibility-compliance.md`; keine Testergebnisse → `testing/accessibility-tests.md`

    **Beispiel-Inhalte:** Code: `<button aria-label="Menü schließen">X</button>`; Kontrast-Tabelle für alle Farbkombinationen; Checkliste: Tastatur-Test je Seite

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
    **Zielgruppe:** Frontend-Entwickler, Designer, QA-Ingenieure

    **Pflicht-Abschnitte:**

    - Breakpoint-Definitionen (mobile, tablet, desktop, large-desktop) mit exakten Pixelwerten
    - Layout-Strategie: Mobile-First vs. Desktop-First
    - Grid-System und Spalten-Konfiguration je Breakpoint
    - Typografie-Skalierung (fluid typography oder stufenweise)
    - Bild- und Medien-Strategie (srcset, picture-Element, lazy loading)
    - Touch-Zielgrößen (mind. 44×44px) und Abstände auf Mobilgeräten

    **Inhaltliche Tiefe:** CSS-Code-Beispiele für Media-Queries; visuelle Vergleiche je Breakpoint; Performance-Hinweise für mobile Geräte

    **Abgrenzung:** Keine Design-Token-Werte → `design/tokens.md`; keine Komponenten-Varianten → `design/components.md`

    **Beispiel-Inhalte:** Breakpoint-Tabelle: Name | Min-Width | Spalten | Gutter; Wireframe-Vergleich: Mobile vs. Desktop-Layout

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
    **Zielgruppe:** Frontend-Entwickler, Designer, UX-Designer

    **Pflicht-Abschnitte:**

    - Animationsprinzipien (Zweck: Feedback, Orientierung, Persönlichkeit)
    - Timing-Funktionen und Dauern (schnell: 150ms, mittel: 300ms, langsam: 500ms)
    - Easing-Kurven (ease-in-out für UI, ease-out für Einblendungen)
    - Bewegungsrichtlinien (reduzierte Bewegung für prefers-reduced-motion)
    - Verbotene Animationen (endlose Loops, ablenkende Effekte)
    - Performance-Richtlinien (GPU-beschleunigte Eigenschaften bevorzugen)

    **Inhaltliche Tiefe:** CSS/JS-Code-Beispiele; Vergleich: mit und ohne Animation; Timing-Token-Tabelle; Barrierefreiheits-Hinweise

    **Abgrenzung:** Keine Komponenten-Details → `design/components.md`; keine Responsive-Layouts → `design/responsive.md`

    **Beispiel-Inhalte:** CSS: `transition: transform 300ms cubic-bezier(0.4, 0, 0.2, 1)`; Tabelle: Anwendungsfall | Dauer | Easing | Eigenschaft

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
    **Zielgruppe:** Designer, Frontend-Entwickler, Content-Ersteller

    **Pflicht-Abschnitte:**

    - Icon-Bibliothek und Quellen (eigene Icons, Icon-Set wie Material Icons, Lucide)
    - Stilrichtlinien (Strichstärke, Rastermaß, optische Größen)
    - Größenvarianten (16px, 20px, 24px, 32px) und Verwendungskontext
    - Icon-Benennung und Dateistruktur
    - Barrierefreiheit: aria-hidden für dekorative Icons, aria-label für funktionale
    - Farbverwendung und Zustandsvarianten (default, hover, disabled, active)

    **Inhaltliche Tiefe:** Vollständiger Icon-Katalog mit Vorschau; SVG-Optimierungsrichtlinien; Implementierungsbeispiele (Inline-SVG vs. Icon-Font vs. Sprite)

    **Abgrenzung:** Keine allgemeine Komponentenbibliothek → `design/components.md`; kein Logo-Guide → `design/style-guide.md`

    **Beispiel-Inhalte:** Icon-Grid: Name | Vorschau | Größen | Verwendung; Code: `<svg aria-hidden="true" class="icon icon-24">...</svg>`

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
    **Zielgruppe:** Frontend-Entwickler, Designer, Design-System-Maintainer

    **Pflicht-Abschnitte:**

    - Dark-Mode-Strategie (systemgesteuert vs. nutzerwählbar vs. beides)
    - Token-Mapping: Light-Token → Dark-Token (komplette Zuordnungstabelle)
    - Farbumkehrungsregeln (nicht einfach invertieren, sondern bewusst anpassen)
    - Kontrast-Anforderungen im Dark Mode (WCAG-konform)
    - Bilder und Medien im Dark Mode (Anpassung von Schatten, Rändern)
    - Implementierung: CSS custom properties, prefers-color-scheme

    **Inhaltliche Tiefe:** Vollständige Token-Mapping-Tabelle; Code-Beispiele für Theme-Switching; Screenshots im Vergleich; Kontrast-Prüfwerte

    **Abgrenzung:** Keine Light-Mode-Token-Definitionen → `design/tokens.md`; keine Komponenten-Details → `design/components.md`

    **Beispiel-Inhalte:** Tabelle: Token | Light-Wert | Dark-Wert | Kontrastverhältnis; CSS: `@media (prefers-color-scheme: dark) { --bg: #1a1a2e; }`

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
    **Zielgruppe:** Frontend-Entwickler, Designer, UX-Designer, QA-Ingenieure

    **Pflicht-Abschnitte:**

    - Formular-Layout-Patterns (einspaltiges, zweispaltiges, Wizard-Muster)
    - Eingabefeld-Typen und wann welcher zu verwenden ist
    - Validierung: Inline-Validierung, Zeitpunkt (on blur, on submit), Fehlermeldungs-Sprache
    - Pflichtfeld-Kennzeichnung und Hilfetexte
    - Barrierefreiheit: Label-Zuordnung, Fehlerzusammenfassung, aria-describedby
    - Formular-Zustände (loading, success, error, disabled)

    **Inhaltliche Tiefe:** Code-Beispiele für jedes Pattern; Fehlermeldungs-Textvorlagen; UX-Best-Practices mit Begründung; Vergleich guter und schlechter Formular-Gestaltung

    **Abgrenzung:** Keine Komponenten-API → `design/components.md`; keine Backend-Validierung → relevante API-Dokumentation

    **Beispiel-Inhalte:** Pattern: „Adresseingabe mit Autocomplete"; Fehlermeldung: „Bitte geben Sie eine gültige E-Mail-Adresse ein (z.B. name@beispiel.de)"

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
    **Zielgruppe:** QA-Ingenieure, Entwickler, Projektleitung, Product Owner

    **Pflicht-Abschnitte:**

    - Test-Strategie: Pyramide (Unit → Integration → E2E), Verteilung der Testarten
    - Qualitätsziele: Mindest-Coverage, maximale Fehlerrate, Defect-Escape-Rate
    - Test-Umgebungen und deren Konfiguration (Dev, Staging, Pre-Prod)
    - Rollen und Verantwortlichkeiten im Test-Prozess
    - Test-Tools und Frameworks (nach Testart aufgeteilt)
    - Metriken und Reporting-Rhythmus

    **Inhaltliche Tiefe:** Strategieebene mit Verlinkung auf Detail-Seiten; Test-Pyramide als Grafik; KPI-Dashboard-Vorlage; CI/CD-Integration beschreiben

    **Abgrenzung:** Keine einzelnen Testfälle → `testing/test-cases.md`; keine Performance-Ergebnisse → `testing/performance-tests.md`

    **Beispiel-Inhalte:** Test-Pyramide: 70 % Unit, 20 % Integration, 10 % E2E; Tabelle: Testart | Tool | Verantwortlich | Coverage-Ziel

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
    **Zielgruppe:** QA-Lead, Projektleitung, Product Owner, Entwickler

    **Pflicht-Abschnitte:**

    - Testumfang und Abgrenzung (was wird getestet, was explizit nicht)
    - Testmethoden je Feature-Bereich (manuell, automatisiert, explorativ)
    - Eingangs- und Ausgangskriterien (Entry/Exit Criteria)
    - Ressourcenplanung: Personal, Testumgebungen, Testdaten
    - Zeitplan: Testphasen mit Start-/Enddatum und Meilensteinen
    - Risikobewertung und Risikominderung für den Testprozess

    **Inhaltliche Tiefe:** Formal nach IEEE 829 oder ISO/IEC 29119 strukturiert; konkrete Deadlines und Verantwortliche; Abhängigkeiten zwischen Testphasen klar benennen

    **Abgrenzung:** Keine einzelnen Testfälle → `testing/test-cases.md`; keine Automatisierungs-Architektur → `testing/test-automation.md`

    **Beispiel-Inhalte:** Gantt-Diagramm der Testphasen; Entry Criteria: „Alle Unit-Tests grün, Code-Review abgeschlossen, Staging-Deployment erfolgreich"

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
    **Zielgruppe:** QA-Ingenieure, Entwickler, Product Owner (Abnahme)

    **Pflicht-Abschnitte:**

    - Testfall-Katalog geordnet nach Feature-Bereichen/Modulen
    - Je Testfall: ID, Titel, Vorbedingungen, Schritte, erwartetes Ergebnis, Priorität
    - Traceability-Matrix: Testfall ↔ Anforderung/User Story
    - Testfall-Status (offen, bestanden, fehlgeschlagen, blockiert)
    - Abdeckungsanalyse: Anforderungen ohne zugeordnete Testfälle

    **Inhaltliche Tiefe:** Vollständige Testfall-Dokumentation mit reproduzierbaren Schritten; Priorisierung (kritisch, hoch, mittel, niedrig); Screenshots oder Mock-Daten wo nötig

    **Abgrenzung:** Keine Testdaten-Details → `testing/test-data.md`; keine Automatisierungsskripte → `testing/test-automation.md`

    **Beispiel-Inhalte:** TC-001: „Login mit gültigem Passwort" | Vorbedingung: Benutzer existiert | Schritt 1: Seite öffnen | Schritt 2: Credentials eingeben | Erwartet: Dashboard sichtbar

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
    **Zielgruppe:** QA-Automation-Ingenieure, DevOps, Entwickler

    **Pflicht-Abschnitte:**

    - Automatisierungsframework und Technologie-Stack (z.B. Playwright, Cypress, pytest)
    - Architektur: Page-Object-Model, Fixtures, Test-Utilities
    - CI/CD-Integration: wann laufen welche Tests (Commit, PR, Nightly)
    - Parallele Ausführung, Retries, Flaky-Test-Management
    - Test-Reporting und Artefakt-Archivierung
    - Wartbarkeit: Namenskonventionen, Ordnerstruktur, Review-Prozess für Tests

    **Inhaltliche Tiefe:** Code-Beispiele für typische Testfälle; CI-Pipeline-Konfiguration (YAML-Ausschnitte); Entscheidungsbaum: wann automatisieren, wann manuell

    **Abgrenzung:** Keine manuellen Testfälle → `testing/test-cases.md`; keine Performance-Tests → `testing/performance-tests.md`

    **Beispiel-Inhalte:** Ordnerstruktur: `tests/e2e/pages/`, `tests/e2e/specs/`; CI-Snippet: „Playwright-Tests bei jedem PR mit 3 Retries"; Beispiel-Page-Object

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
    **Zielgruppe:** Performance-Ingenieure, DevOps, Architekten, Projektleitung

    **Pflicht-Abschnitte:**

    - Performance-Ziele: Antwortzeiten (P50, P95, P99), Durchsatz, gleichzeitige Benutzer
    - Testwerkzeuge (k6, JMeter, Locust, Lighthouse) und deren Konfiguration
    - Testszenarien: Lasttest, Stresstest, Spike-Test, Soak-Test
    - Ergebnisse: Metriken, Grafiken, Engpass-Analyse
    - Baselines und Schwellenwerte für CI-Gate (Test scheitert bei Regression)
    - Empfehlungen und durchgeführte Optimierungen

    **Inhaltliche Tiefe:** Grafiken mit Latenz-/Durchsatz-Kurven; Vergleich vor/nach Optimierung; konkrete Testskript-Ausschnitte; Hardware-/Umgebungs-Beschreibung

    **Abgrenzung:** Keine funktionalen Tests → `testing/test-cases.md`; keine Infrastruktur-Skalierung → `operations/scaling.md`

    **Beispiel-Inhalte:** Grafik: Latenz vs. gleichzeitige User; Tabelle: Endpunkt | P50 | P95 | P99 | Ziel; k6-Skript-Ausschnitt für Hauptszenario

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
    **Zielgruppe:** Security-Ingenieure, Entwickler, Compliance-Beauftragte

    **Pflicht-Abschnitte:**

    - Sicherheitstest-Strategie: SAST, DAST, SCA, Penetrationstest, Dependency-Scanning
    - Eingesetzte Tools je Methode (SonarQube, OWASP ZAP, Trivy, Snyk)
    - CI/CD-Integration: wann welcher Scan läuft, Break-Kriterien (Critical/High)
    - Ergebnisübersicht: gefundene Schwachstellen nach Schweregrad
    - Behebungsstatus und Zeitvorgaben (Critical: 24h, High: 7 Tage)
    - Penetrationstest-Berichte (Zusammenfassung, vollständige Reports separat)

    **Inhaltliche Tiefe:** Dashboard-artige Zusammenfassung; CVE-Nummern bei bekannten Schwachstellen; Trend-Grafiken über Zeit; OWASP-Top-10-Abdeckung

    **Abgrenzung:** Keine Sicherheitsrichtlinien → `compliance/security-policies.md`; keine Incident-Response → `compliance/incident-response.md`

    **Beispiel-Inhalte:** Tabelle: Schwachstelle | Schweregrad | CVSS | Status | Frist; CI-Gate: „Pipeline bricht bei Critical-Findings ab"

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
    **Zielgruppe:** Product Owner, Fachbereich, QA-Ingenieure, Projektleitung

    **Pflicht-Abschnitte:**

    - Abnahmekriterien je User Story / Epic (Given-When-Then-Format)
    - Abnahmeprozess: Wer nimmt ab, wann, welche Umgebung
    - Protokollvorlage für Abnahme (Datum, Tester, Ergebnis, Kommentare)
    - Umgang mit Abweichungen (Showstopper vs. akzeptable Einschränkungen)
    - Abnahme-Ergebnisse und Sign-Off-Dokumentation

    **Inhaltliche Tiefe:** Fachlich verständlich, nicht technisch; konkrete Akzeptanzkriterien; BDD-Syntax (Gherkin) wo möglich; Screenshots der Abnahme-Umgebung

    **Abgrenzung:** Keine technischen Testfälle → `testing/test-cases.md`; keine automatisierten Tests → `testing/test-automation.md`

    **Beispiel-Inhalte:** Szenario: „GEGEBEN ein eingeloggter Benutzer, WENN er auf ‚Exportieren' klickt, DANN wird eine CSV-Datei heruntergeladen"; Abnahmeprotokoll-Vorlage

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
    **Zielgruppe:** QA-Ingenieure, Entwickler, Release-Manager

    **Pflicht-Abschnitte:**

    - Regressionstests-Umfang: Welche Bereiche werden bei jedem Release geprüft
    - Automatisierte vs. manuelle Regressionstests und Begründung
    - Priorisierung: kritische Pfade zuerst (Smoke-Test-Suite)
    - Ausführungsplan: wann und wie oft (je Sprint, je Release, nightly)
    - Ergebnisse: Trend der Regressionsrate über Releases
    - Prozess bei Regressionsfund (Bug-Ticket, Priorität, Blockade)

    **Inhaltliche Tiefe:** Liste der Smoke-Test-Szenarien; Automatisierungsgrad pro Modul; Grafik: Regressionsfunde pro Release

    **Abgrenzung:** Keine neuen Feature-Tests → `testing/test-cases.md`; keine Automatisierungs-Architektur → `testing/test-automation.md`

    **Beispiel-Inhalte:** Smoke-Suite: Login → Dashboard → CRUD-Operation → Logout; Tabelle: Modul | Automatisiert (%) | Manuell (%) | Letzte Ausführung

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
    **Zielgruppe:** QA-Ingenieure, Frontend-Entwickler, Product Owner

    **Pflicht-Abschnitte:**

    - Browser-Matrix: unterstützte Browser und Versionen (Chrome, Firefox, Safari, Edge)
    - Betriebssystem-Matrix: Windows, macOS, Linux, iOS, Android
    - Geräte-Matrix: Desktop, Tablet, Smartphone (physische und emulierte Geräte)
    - Testmethodik: manuell, BrowserStack/Sauce Labs, automatisiert
    - Bekannte Inkompatibilitäten und Workarounds
    - Mindestanforderungen und Support-Abkündigungsrichtlinie

    **Inhaltliche Tiefe:** Vollständige Support-Matrix mit Status (voll unterstützt, eingeschränkt, nicht unterstützt); Screenshots je Plattform bei Abweichungen

    **Abgrenzung:** Keine Responsive-Design-Regeln → `design/responsive.md`; keine Performance → `testing/performance-tests.md`

    **Beispiel-Inhalte:** Matrix: Browser | Version | OS | Status | Bemerkung; BrowserStack-Konfiguration für CI; Screenshot-Vergleich Chrome vs. Safari

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
    **Zielgruppe:** QA-Ingenieure, Frontend-Entwickler, Accessibility-Beauftragte

    **Pflicht-Abschnitte:**

    - Testmethoden: automatisiert (axe-core, Lighthouse), manuell (Screenreader, Tastatur), Experten-Review
    - Prüfung gegen WCAG 2.1 AA: vollständige Checkliste der Erfolgskriterien
    - Screenreader-Tests: NVDA (Windows), VoiceOver (macOS/iOS), TalkBack (Android)
    - Tastaturnavigation: Tab-Reihenfolge, Fokus-Management, Skip-Links
    - Ergebnisse: Befunde, Schweregrad, Behebungsstatus
    - CI-Integration: automatisierte A11y-Prüfung bei jedem Build

    **Inhaltliche Tiefe:** Befundliste mit WCAG-Kriterium-Verweis; Screenshot + Screenreader-Transkript bei Fehlern; Trend-Grafik der A11y-Score-Entwicklung

    **Abgrenzung:** Keine Design-Richtlinien → `design/accessibility-guidelines.md`; keine gesetzlichen Anforderungen → `compliance/accessibility-compliance.md`

    **Beispiel-Inhalte:** Befund: „Formularfeld ‚Name' hat kein Label → WCAG 1.3.1 verletzt → Severity: hoch"; axe-core CI-Konfiguration

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
    **Zielgruppe:** QA-Ingenieure, Entwickler, Datenbankadministratoren

    **Pflicht-Abschnitte:**

    - Testdaten-Strategie: synthetisch, anonymisiert aus Produktion, Fixtures
    - Erstellung und Verwaltung: Factories, Seeders, Faker-Bibliotheken
    - Datenschutz: Anonymisierungs-/Pseudonymisierungsverfahren für produktionsnahe Daten
    - Testdaten-Umgebungen und -Isolierung (Tenant-Separation, DB-Snapshots)
    - Datenreset-Strategien zwischen Testläufen (Truncate, Rollback, Docker-Reset)
    - Versionierung von Testdaten-Sets

    **Inhaltliche Tiefe:** Code-Beispiele für Factories; Konfiguration der Anonymisierungs-Pipeline; Verzeichnis verfügbarer Test-Datensätze mit Beschreibung

    **Abgrenzung:** Keine Testfälle → `testing/test-cases.md`; kein Datenschutz-Recht → `compliance/data-protection.md`

    **Beispiel-Inhalte:** Factory: `UserFactory.create(role='admin', verified=True)`; Anonymisierungsregel: E-Mail → `user_{id}@test.local`; Seed-Datensatz: 100 User, 500 Bestellungen

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
    **Zielgruppe:** Gesamtes Projektteam, Stakeholder, neue Teammitglieder

    **Pflicht-Abschnitte:**

    - Projektziel und Vision (1–2 Sätze)
    - Teamstruktur: Rollen, Personen, Verantwortlichkeiten
    - Methodik: Scrum/Kanban/SAFe – Sprint-Rhythmus, Zeremonien
    - Kommunikationskanäle (Slack, E-Mail, Jira, Confluence)
    - Projekt-Timeline mit Meilensteinen
    - Links zu allen Unterseiten des Project-Bereichs

    **Inhaltliche Tiefe:** Übersichtsebene mit schnellem Einstieg für neue Mitglieder; Organigramm oder Verantwortungsmatrix (RACI); Verlinkung zu Detail-Seiten

    **Abgrenzung:** Keine fachlichen Anforderungen → Anforderungsdokumentation; keine technische Architektur → `architecture/`

    **Beispiel-Inhalte:** RACI-Matrix: Aufgabe | Responsible | Accountable | Consulted | Informed; Timeline mit 4 Meilensteinen je Quartal

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
    **Zielgruppe:** Product Owner, Projektleitung, Stakeholder, Entwickler

    **Pflicht-Abschnitte:**

    - Strategische Vision (6–12 Monate)
    - Quartals-/Release-Planung mit Epics und Features
    - Priorisierung und Abhängigkeiten zwischen Features
    - Status je Roadmap-Element (geplant, in Arbeit, abgeschlossen, verschoben)
    - Kapazitätsplanung und Ressourcenzuordnung
    - Änderungshistorie der Roadmap

    **Inhaltliche Tiefe:** Visueller Roadmap-Zeitstrahl; Verlinkung zu Jira/GitHub-Epics; Begründung für Priorisierungsentscheidungen

    **Abgrenzung:** Keine Sprint-Planung (zu granular) → Jira/Board; keine technische Architekturentscheidungen → `architecture/decisions/`

    **Beispiel-Inhalte:** Zeitstrahl: Q1: „Authentifizierung v2", Q2: „Dashboard-Redesign", Q3: „API v3"; Status-Legende: geplant/in Arbeit/fertig

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
    **Zielgruppe:** Projektleitung, Product Owner, Kommunikationsverantwortliche

    **Pflicht-Abschnitte:**

    - Stakeholder-Verzeichnis: Name, Rolle, Organisation, Kontaktdaten
    - Einfluss-/Interesse-Matrix (Power-Interest-Grid)
    - Kommunikationsbedürfnisse je Stakeholder-Gruppe
    - Erwartungen und Erfolgskriterien je Stakeholder
    - Eskalationspfade und Entscheidungsbefugnisse

    **Inhaltliche Tiefe:** Strukturierte Tabelle; Power-Interest-Grid als Diagramm; je Stakeholder: bevorzugter Kommunikationskanal und -frequenz

    **Abgrenzung:** Keine Meeting-Details → `project/meetings.md`; kein Kommunikationsplan-Detail → `project/communication-plan.md`

    **Beispiel-Inhalte:** Tabelle: Stakeholder | Rolle | Einfluss (hoch/mittel) | Interesse | Kommunikationskanal | Frequenz; Grid-Diagramm mit Quadranten

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
    **Zielgruppe:** Projektleitung, Architekten, Stakeholder, Risikomanager

    **Pflicht-Abschnitte:**

    - Risikoregister: ID, Beschreibung, Kategorie (technisch, organisatorisch, extern)
    - Bewertung: Eintrittswahrscheinlichkeit × Auswirkung = Risikoprioritätszahl
    - Mitigationsstrategien je Risiko (vermeiden, reduzieren, übertragen, akzeptieren)
    - Risikoverantwortliche (Risk Owner)
    - Überwachungs- und Eskalationsmechanismen
    - Regelmäßiger Review-Rhythmus (z.B. alle 2 Wochen)

    **Inhaltliche Tiefe:** Vollständige Risikotabelle; Risikomatrix (Heatmap); konkrete Maßnahmen mit Deadlines; Trend-Tracking (Risiko steigend/stabil/sinkend)

    **Abgrenzung:** Keine Drittanbieter-Risiken → `compliance/third-party-risk.md`; keine Sicherheitsvorfälle → `compliance/incident-response.md`

    **Beispiel-Inhalte:** R-001: „Schlüsselentwickler verlässt das Team" | W: hoch | A: hoch | Mitigation: Cross-Training, Dokumentation; Heatmap 5×5

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
    **Zielgruppe:** Scrum Master, Projektleitung, Teammitglieder

    **Pflicht-Abschnitte:**

    - Meeting-Typen: Daily, Sprint Planning, Review, Retro, Refinement, Steering Committee
    - Je Meeting-Typ: Ziel, Teilnehmer, Dauer, Frequenz, Agenda-Template
    - Moderationshinweise und Timeboxing-Regeln
    - Protokoll-Vorlage: Entscheidungen, Action Items, Verantwortliche, Fristen
    - Anti-Patterns: Welche Meeting-Praktiken vermieden werden sollen

    **Inhaltliche Tiefe:** Detaillierte Agenda-Templates je Meeting-Typ; Beispiel-Protokoll; Kalenderübersicht aller wiederkehrenden Meetings

    **Abgrenzung:** Keine Stakeholder-Details → `project/stakeholders.md`; keine Kommunikationskanäle → `project/communication-plan.md`

    **Beispiel-Inhalte:** Daily-Template: „Was habe ich gestern erreicht? Was mache ich heute? Gibt es Blocker?"; Retro-Format: „Start, Stop, Continue"

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


def _walk_tree(base: Path, current: Path, tree: list[tuple[str, int]], depth: int) -> None:
    """Recursively walk directory and build tree display."""
    entries = sorted(current.iterdir(), key=lambda p: (not p.is_dir(), p.name))
    for entry in entries:
        if entry.is_dir():
            tree.append((f"{entry.name}/", depth))
            _walk_tree(base, entry, tree, depth + 1)
        elif entry.suffix == ".md":
            tree.append((entry.name, depth))
