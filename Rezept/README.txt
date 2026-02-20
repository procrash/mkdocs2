mkdocsOnSteroids - Minimales Setup
====================================

Voraussetzungen: docker, docker compose, curl

Schnellstart:
  chmod +x bootstrap.sh
  ./bootstrap.sh

Das Script fragt interaktiv ab:
  - Pfad zum mkdocsOnSteroids-Quellcode (oder Git-URL)
  - Pfad zum zu dokumentierenden Quellcode
  - LLM-Server URL (Ollama, vLLM, LM Studio, ...)
  - Ausgabe-Verzeichnis, Port, Mock-Modus

Danach: docker build + docker compose up (automatisch).

Weitere Befehle:
  ./bootstrap.sh start    Container starten
  ./bootstrap.sh stop     Container stoppen
  ./bootstrap.sh build    Image neu bauen
  ./bootstrap.sh serve    Nur MkDocs-Server starten
  ./bootstrap.sh clean    Generierte Doku loeschen
  ./bootstrap.sh status   Status anzeigen

Dokumentation: http://localhost:8000 (nach Generierung)
