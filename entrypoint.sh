#!/bin/bash
set -e

echo "=== mkdocsOnSteroids Entrypoint ==="

# 1. Check if opencode is available
if command -v opencode &>/dev/null; then
    echo "[OK] opencode found: $(which opencode)"
else
    echo "[WARN] opencode not found in PATH, attempting install..."
    npm install -g opencode 2>/dev/null || echo "[WARN] opencode install failed, continuing without it"
fi

# 2. Check server connectivity
SERVER_URL="${OPENAPI_SERVER_URL:-http://host.docker.internal:11434}"
echo "[INFO] Testing server: ${SERVER_URL}"
if curl -sf "${SERVER_URL}/v1/models" >/dev/null 2>&1; then
    echo "[OK] Server is reachable"
else
    echo "[WARN] Server at ${SERVER_URL} is not reachable"
    if [ "${MOCK_MODE}" = "true" ]; then
        echo "[INFO] Mock mode enabled, continuing..."
    else
        echo "[INFO] Set MOCK_MODE=true to run without a server"
    fi
fi

# 3. Generate config.yaml if not present
if [ ! -f /app/config.yaml ] || [ "${FORCE_CONFIG:-false}" = "true" ]; then
    echo "[INFO] Generating config.yaml..."
    cat > /app/config.yaml <<EOF
project:
  name: "${PROJECT_NAME:-Documentation}"
  source_dir: "/src"
  output_dir: "/docs"
  repo_url: "${REPO_URL:-}"
  languages:
    - cpp
    - python
  ignore_patterns:
    - "*/test/*"
    - "*/build/*"
    - "*/__pycache__/*"

server:
  url: "${SERVER_URL}"
  api_key: "${OPENAPI_KEY:-}"
  timeout_connect: 10
  timeout_read: 60

system:
  global_timeout_seconds: 120
  max_retries: 3
  retry_base_delay: 2
  parallel_workers: ${PARALLEL_WORKERS:-3}
  mock_mode: ${MOCK_MODE:-false}

models:
  analysts: []
  judge: null

stakeholders:
  developer:
    enabled: true
    models: "analysts"
    doc_types: [classes, modules, functions, architecture, diagrams]
  api:
    enabled: true
    models: "analysts"
    doc_types: [endpoints, schemas, examples]
  user:
    enabled: true
    models: "analysts"
    doc_types: [features, tutorials]

output:
  mkdocs_theme: "material"
  latex_enabled: true
  mermaid_enabled: true
  code_copy_enabled: true
  serve_port: 8000
EOF
    echo "[OK] config.yaml generated"
fi

# 4. Run the requested command
CMD="${1:-generate}"
shift 2>/dev/null || true

case "$CMD" in
    setup)
        echo "[INFO] Running setup..."
        python -m src.main setup "$@"
        ;;
    discover)
        echo "[INFO] Running discovery..."
        python -m src.main discover "$@"
        ;;
    generate)
        echo "[INFO] Running documentation generation..."
        python -m src.main generate "$@"
        # Optionally serve after generation
        if [ "${AUTO_SERVE:-false}" = "true" ]; then
            echo "[INFO] Starting MkDocs server..."
            python -m src.main serve --port 8000
        fi
        ;;
    run)
        echo "[INFO] Starting TUI workflow..."
        EXTRA_ARGS=""
        if [ "${AUTOMATION_MODE:-false}" = "true" ]; then
            EXTRA_ARGS="--auto"
        fi
        python -m src.main run $EXTRA_ARGS "$@"
        ;;
    serve)
        echo "[INFO] Starting MkDocs server..."
        python -m src.main serve --port 8000
        ;;
    *)
        echo "[INFO] Running: python -m src.main $CMD $@"
        python -m src.main "$CMD" "$@"
        ;;
esac
