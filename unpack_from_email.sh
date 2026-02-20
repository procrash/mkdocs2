#!/bin/bash
# Unpack mkdocsOnSteroids from email transport .txt file
# Usage: bash unpack_from_email.sh mkdocsOnSteroids_email.txt
set -e

if [ -z "$1" ]; then
    echo "Usage: bash unpack_from_email.sh <txt-file>"
    echo "  z.B.: bash unpack_from_email.sh mkdocsOnSteroids_email.txt"
    exit 1
fi

TXT_FILE="$1"

if [ ! -f "${TXT_FILE}" ]; then
    echo "Fehler: Datei '${TXT_FILE}' nicht gefunden."
    exit 1
fi

echo "=== Entpacke mkdocsOnSteroids aus ${TXT_FILE} ==="

# Extract base64 content between markers
ARCHIVE="mkdocsOnSteroids.tar.gz"
sed -n '/^==== BASE64 START ====/,/^==== BASE64 END ====/p' "${TXT_FILE}" \
    | grep -v '==== BASE64' \
    | base64 -d > "${ARCHIVE}"

echo "Archive extrahiert: $(du -h "${ARCHIVE}" | cut -f1)"

# Extract tar.gz
tar xzf "${ARCHIVE}"
rm -f "${ARCHIVE}"

echo ""
echo "Fertig! Projekt entpackt nach: mkdocsOnSteroids/"
echo ""
echo "Zum Starten:"
echo "  cd mkdocsOnSteroids"
echo "  docker compose up --build"
