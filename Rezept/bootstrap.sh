#!/bin/bash
set -e

# ============================================================================
#  mkdocsOnSteroids - Bootstrap Script
#  Einziger Einstiegspunkt: ./bootstrap.sh
#  Voraussetzungen: docker, docker compose, curl
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_DIR="${SCRIPT_DIR}/app"

# Farben
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

info()  { echo -e "${CYAN}[INFO]${NC}  $*"; }
ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*"; }

banner() {
    echo ""
    echo -e "${BOLD}╔═══════════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}║        mkdocsOnSteroids - Bootstrap           ║${NC}"
    echo -e "${BOLD}║   Automatische Dokumentations-Generierung     ║${NC}"
    echo -e "${BOLD}╚═══════════════════════════════════════════════╝${NC}"
    echo ""
}

# ── 1. Voraussetzungen prüfen ──────────────────────────────────────────────

check_prerequisites() {
    info "Prüfe Voraussetzungen..."
    local missing=0

    if ! command -v docker &>/dev/null; then
        error "docker nicht gefunden. Bitte installiere Docker: https://docs.docker.com/get-docker/"
        missing=1
    else
        ok "docker $(docker --version | grep -oP '\d+\.\d+\.\d+')"
    fi

    if docker compose version &>/dev/null; then
        ok "docker compose $(docker compose version --short 2>/dev/null)"
        COMPOSE_CMD="docker compose"
    elif command -v docker-compose &>/dev/null; then
        ok "docker-compose $(docker-compose --version | grep -oP '\d+\.\d+\.\d+')"
        COMPOSE_CMD="docker-compose"
    else
        error "docker compose nicht gefunden."
        missing=1
    fi

    if ! command -v curl &>/dev/null; then
        error "curl nicht gefunden."
        missing=1
    else
        ok "curl vorhanden"
    fi

    if [ "$missing" -eq 1 ]; then
        echo ""
        error "Bitte installiere die fehlenden Voraussetzungen und starte erneut."
        exit 1
    fi
    echo ""
}

# ── 2. Quellcode besorgen ──────────────────────────────────────────────────

fetch_source() {
    if [ -d "${APP_DIR}/src" ] && [ -f "${APP_DIR}/requirements.txt" ]; then
        ok "App-Verzeichnis bereits vorhanden: ${APP_DIR}"
        return
    fi

    info "mkdocsOnSteroids Quellcode wird benötigt."
    echo ""
    echo -e "  ${BOLD}Optionen:${NC}"
    echo "  1) Lokaler Pfad (z.B. /mnt/synology/docSys/mkdocsOnSteroids)"
    echo "  2) Git-Repository URL"
    echo ""
    read -rp "  Wähle [1/2] (Standard: 1): " source_choice
    source_choice="${source_choice:-1}"

    case "$source_choice" in
        1)
            read -rp "  Pfad zum mkdocsOnSteroids-Verzeichnis: " local_path
            local_path="${local_path%/}"
            if [ ! -f "${local_path}/requirements.txt" ] || [ ! -d "${local_path}/src" ]; then
                error "Kein gültiges mkdocsOnSteroids-Verzeichnis: ${local_path}"
                exit 1
            fi
            info "Kopiere Dateien..."
            mkdir -p "${APP_DIR}"
            cp -r "${local_path}/src" "${APP_DIR}/src"
            cp -r "${local_path}/templates" "${APP_DIR}/templates" 2>/dev/null || true
            cp "${local_path}/requirements.txt" "${APP_DIR}/requirements.txt"
            cp "${local_path}/entrypoint.sh" "${APP_DIR}/entrypoint.sh"
            cp "${local_path}/config.yaml" "${APP_DIR}/config.yaml" 2>/dev/null || true
            # Manuelle Docs übernehmen falls vorhanden
            if [ -d "${local_path}/docs_project/docs/manual" ]; then
                mkdir -p "${APP_DIR}/docs_project/docs/manual"
                cp -r "${local_path}/docs_project/docs/manual/"* "${APP_DIR}/docs_project/docs/manual/" 2>/dev/null || true
            fi
            ok "Dateien kopiert nach ${APP_DIR}"
            ;;
        2)
            read -rp "  Git-Repository URL: " git_url
            if [ -z "$git_url" ]; then
                error "Keine URL angegeben."
                exit 1
            fi
            info "Klone Repository..."
            git clone --depth 1 "$git_url" "${APP_DIR}"
            ok "Repository geklont nach ${APP_DIR}"
            ;;
        *)
            error "Ungültige Auswahl."
            exit 1
            ;;
    esac
}

# ── 3. Benutzer-Konfiguration abfragen ────────────────────────────────────

configure() {
    echo ""
    echo -e "${BOLD}── Konfiguration ──${NC}"
    echo ""

    # Projektname
    read -rp "  Projektname [MyProject Documentation]: " project_name
    project_name="${project_name:-MyProject Documentation}"

    # Quellcode-Pfad zum Dokumentieren
    read -rp "  Pfad zum Quellcode der dokumentiert werden soll [./]: " source_dir
    source_dir="${source_dir:-./}"
    # Zu absolutem Pfad konvertieren
    if [[ "$source_dir" != /* ]]; then
        source_dir="$(cd "$source_dir" 2>/dev/null && pwd)" || { error "Pfad nicht gefunden: $source_dir"; exit 1; }
    fi

    # Output-Pfad
    default_output="${SCRIPT_DIR}/output"
    read -rp "  Ausgabe-Verzeichnis [${default_output}]: " output_dir
    output_dir="${output_dir:-${default_output}}"
    if [[ "$output_dir" != /* ]]; then
        output_dir="$(pwd)/${output_dir}"
    fi
    mkdir -p "$output_dir"

    # LLM Server
    read -rp "  OpenAI-kompatibler Server URL [http://host.docker.internal:11434]: " server_url
    server_url="${server_url:-http://host.docker.internal:11434}"

    # API Key
    read -rp "  API Key (leer = ohne Auth) []: " api_key
    api_key="${api_key:-}"

    # Port
    read -rp "  MkDocs Port [8000]: " serve_port
    serve_port="${serve_port:-8000}"

    # Mock mode
    read -rp "  Mock-Modus (ohne LLM testen)? [j/N]: " mock_choice
    if [[ "$mock_choice" =~ ^[jJyY] ]]; then
        mock_mode="true"
    else
        mock_mode="false"
    fi

    # Auto-Serve
    read -rp "  Dokumentation nach Generierung automatisch anzeigen? [J/n]: " serve_choice
    if [[ "$serve_choice" =~ ^[nN] ]]; then
        auto_serve="false"
    else
        auto_serve="true"
    fi

    echo ""

    # .env schreiben
    cat > "${SCRIPT_DIR}/.env" <<EOF
# mkdocsOnSteroids - generiert von bootstrap.sh am $(date '+%Y-%m-%d %H:%M')

SOURCE_DIR=${source_dir}
OUTPUT_DIR=${output_dir}
OPENAPI_SERVER_URL=${server_url}
OPENAPI_KEY=${api_key}
SERVE_PORT=${serve_port}
MOCK_MODE=${mock_mode}
PARALLEL_WORKERS=3
AUTO_SERVE=${auto_serve}
PROJECT_NAME=${project_name}
EOF

    ok ".env geschrieben"
}

# ── 4. Docker bauen ────────────────────────────────────────────────────────

build_image() {
    echo ""
    echo -e "${BOLD}── Docker Build ──${NC}"
    echo ""
    info "Baue Docker-Image (lädt Python, Node.js, pip packages)..."

    # Dockerfile aus Rezept-Ordner verwenden, aber im app/-Kontext bauen
    cp "${SCRIPT_DIR}/Dockerfile" "${APP_DIR}/Dockerfile"

    $COMPOSE_CMD -f "${SCRIPT_DIR}/docker-compose.yml" --env-file "${SCRIPT_DIR}/.env" build

    ok "Docker-Image gebaut"
}

# ── 5. Starten ─────────────────────────────────────────────────────────────

start() {
    echo ""
    echo -e "${BOLD}── Start ──${NC}"
    echo ""

    # Server-Erreichbarkeit testen (nur Info)
    local server_url
    server_url=$(grep OPENAPI_SERVER_URL "${SCRIPT_DIR}/.env" | cut -d= -f2-)
    # host.docker.internal → localhost für Host-Check
    local check_url="${server_url//host.docker.internal/localhost}"
    if curl -sf "${check_url}/v1/models" >/dev/null 2>&1; then
        ok "LLM-Server erreichbar: ${server_url}"
    else
        local mock_mode
        mock_mode=$(grep MOCK_MODE "${SCRIPT_DIR}/.env" | cut -d= -f2-)
        if [ "$mock_mode" = "true" ]; then
            warn "LLM-Server nicht erreichbar, aber Mock-Modus ist aktiv."
        else
            warn "LLM-Server nicht erreichbar: ${check_url}"
            warn "Starte trotzdem. Setze MOCK_MODE=true in .env zum Testen ohne Server."
        fi
    fi

    info "Starte mkdocsOnSteroids..."
    $COMPOSE_CMD -f "${SCRIPT_DIR}/docker-compose.yml" --env-file "${SCRIPT_DIR}/.env" up

    echo ""
    ok "Fertig."
}

# ── 6. Weitere Befehle ────────────────────────────────────────────────────

usage() {
    echo "Verwendung: $0 [BEFEHL]"
    echo ""
    echo "Befehle:"
    echo "  (ohne)      Ersteinrichtung: Konfiguration + Build + Start"
    echo "  start       Container starten (nach vorheriger Einrichtung)"
    echo "  build       Docker-Image neu bauen"
    echo "  stop        Container stoppen"
    echo "  serve       Nur MkDocs-Server starten (Doku muss existieren)"
    echo "  clean       Generierte Dokumentation löschen"
    echo "  status      Status anzeigen"
    echo ""
}

# ── Main ───────────────────────────────────────────────────────────────────

main() {
    cd "$SCRIPT_DIR"

    case "${1:-}" in
        start)
            if [ ! -f "${SCRIPT_DIR}/.env" ]; then
                error "Keine .env gefunden. Bitte zuerst ./bootstrap.sh ohne Argumente ausführen."
                exit 1
            fi
            $COMPOSE_CMD -f docker-compose.yml --env-file .env up
            ;;
        build)
            $COMPOSE_CMD -f docker-compose.yml --env-file .env build
            ;;
        stop)
            $COMPOSE_CMD -f docker-compose.yml --env-file .env down
            ;;
        serve)
            $COMPOSE_CMD -f docker-compose.yml --env-file .env run --rm \
                -p "${SERVE_PORT:-8000}:8000" mkdocs-steroids serve
            ;;
        clean)
            local output_dir
            output_dir=$(grep OUTPUT_DIR .env 2>/dev/null | cut -d= -f2-)
            if [ -n "$output_dir" ] && [ -d "${output_dir}/docs/generated" ]; then
                rm -rf "${output_dir}/docs/generated" "${output_dir}/mkdocs.yml" "${output_dir}/generation_report.md"
                ok "Generierte Doku gelöscht."
            else
                warn "Nichts zu löschen."
            fi
            ;;
        status)
            echo -e "${BOLD}mkdocsOnSteroids Status${NC}"
            echo ""
            if [ -f .env ]; then
                ok ".env vorhanden"
                grep -v "^#" .env | grep -v "^$" | while read -r line; do
                    echo "  $line"
                done
            else
                warn "Keine .env - ./bootstrap.sh ausführen"
            fi
            echo ""
            $COMPOSE_CMD -f docker-compose.yml ps 2>/dev/null || true
            ;;
        help|--help|-h)
            usage
            ;;
        "")
            banner
            check_prerequisites
            fetch_source
            configure
            build_image
            start
            ;;
        *)
            error "Unbekannter Befehl: $1"
            usage
            exit 1
            ;;
    esac
}

main "$@"
