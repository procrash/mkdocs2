#!/bin/bash
# mkdocsOnSteroids - Host setup script (outside Docker)
set -e

echo "=== mkdocsOnSteroids Setup ==="

# Check Python version
PYTHON_CMD=""
for cmd in python3.11 python3 python; do
    if command -v "$cmd" &>/dev/null; then
        version=$("$cmd" --version 2>&1 | grep -oP '\d+\.\d+')
        major=$(echo "$version" | cut -d. -f1)
        minor=$(echo "$version" | cut -d. -f2)
        if [ "$major" -ge 3 ] && [ "$minor" -ge 11 ]; then
            PYTHON_CMD="$cmd"
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "[ERROR] Python 3.11+ required but not found."
    exit 1
fi
echo "[OK] Python: $($PYTHON_CMD --version)"

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "[INFO] Creating virtual environment..."
    $PYTHON_CMD -m venv .venv
fi
source .venv/bin/activate
echo "[OK] Virtual environment activated"

# Install dependencies
echo "[INFO] Installing Python dependencies..."
pip install -r requirements.txt --quiet

# Check for opencode
if command -v opencode &>/dev/null; then
    echo "[OK] opencode found: $(which opencode)"
else
    echo "[INFO] Installing opencode..."
    if command -v npm &>/dev/null; then
        npm install -g opencode 2>/dev/null || echo "[WARN] opencode install via npm failed"
    else
        echo "[WARN] npm not found. Install Node.js and run: npm install -g opencode"
    fi
fi

# Interactive setup
read -p "Run interactive setup wizard? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python -m src.main setup --interactive
else
    echo "[INFO] Skipping wizard. Edit config.yaml manually."
fi

echo ""
echo "=== Setup Complete ==="
echo "Usage:"
echo "  source .venv/bin/activate"
echo "  python -m src.main generate --cli    # Generate docs"
echo "  python -m src.main serve             # Serve docs"
echo "  python -m src.main --help            # Show all commands"
