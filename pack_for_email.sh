#!/bin/bash
# Pack mkdocsOnSteroids for email transport (bypasses Gmail attachment filters)
# Creates a base64-encoded .txt file that Gmail won't block
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_NAME="mkdocsOnSteroids"
OUTPUT_DIR="${SCRIPT_DIR}"
ARCHIVE="${OUTPUT_DIR}/${PROJECT_NAME}.tar.gz"
TXT_FILE="${OUTPUT_DIR}/${PROJECT_NAME}_email.txt"

echo "=== Packing ${PROJECT_NAME} for email ==="

# Create tar.gz excluding unnecessary files
cd "${SCRIPT_DIR}/.."
# tar exit code 1 = "file changed as we read it" is harmless on live filesystems
tar czf "${ARCHIVE}" \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='node_modules' \
    --exclude='.venv' \
    --exclude='*.pyc' \
    --exclude="${PROJECT_NAME}/pack_for_email.sh" \
    --exclude="${PROJECT_NAME}/unpack_from_email.sh" \
    --exclude="${PROJECT_NAME}/${PROJECT_NAME}_email.txt" \
    "${PROJECT_NAME}/" || [ $? -eq 1 ]

echo "Archive: $(du -h "${ARCHIVE}" | cut -f1)"

# Base64 encode and wrap in a self-describing text file
{
    echo "==== mkdocsOnSteroids – Email Transport Package ===="
    echo "==== Erstellt: $(date '+%Y-%m-%d %H:%M') ===="
    echo "==== Zum Entpacken: unpack_from_email.sh oder siehe Anleitung unten ===="
    echo ""
    echo "ANLEITUNG:"
    echo "  1) Alles zwischen den BASE64-Markern in eine Datei 'payload.b64' kopieren"
    echo "  2) base64 -d payload.b64 > mkdocsOnSteroids.tar.gz"
    echo "  3) tar xzf mkdocsOnSteroids.tar.gz"
    echo "  Oder einfach: bash unpack_from_email.sh ${PROJECT_NAME}_email.txt"
    echo ""
    echo "==== BASE64 START ===="
    base64 "${ARCHIVE}"
    echo "==== BASE64 END ===="
} > "${TXT_FILE}"

# Clean up intermediate archive
rm -f "${ARCHIVE}"

SIZE=$(du -h "${TXT_FILE}" | cut -f1)
echo ""
echo "Fertig! Datei zum Versenden:"
echo "  ${TXT_FILE} (${SIZE})"
echo ""
echo "Diese .txt Datei als Email-Anhang versenden."
echo "Zum Entpacken: bash unpack_from_email.sh ${PROJECT_NAME}_email.txt"
