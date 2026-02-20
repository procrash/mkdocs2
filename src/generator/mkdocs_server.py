"""Background MkDocs development server management."""
from __future__ import annotations
import asyncio
import logging
import signal
import socket
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


def is_port_available(port: int, host: str = "0.0.0.0") -> bool:
    """Check if a TCP port is available."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            sock.bind((host, port))
            return True
    except OSError:
        return False


def find_available_port(start: int = 8000, max_tries: int = 20) -> int:
    """Find the first available port starting from `start`."""
    for offset in range(max_tries):
        port = start + offset
        if is_port_available(port):
            return port
    raise RuntimeError(f"No available port found in range {start}-{start + max_tries - 1}")


class MkDocsServer:
    """Manage a background MkDocs development server."""

    def __init__(self, docs_dir: Path, port: int = 8000, host: str = "0.0.0.0"):
        self.docs_dir = docs_dir
        self.port = port
        self.host = host
        self._process: subprocess.Popen | None = None
        self._url: str = ""

    @property
    def url(self) -> str:
        return self._url

    @property
    def running(self) -> bool:
        return self._process is not None and self._process.poll() is None

    def start(self) -> str:
        """Start MkDocs dev server in background. Returns the URL."""
        if self.running:
            logger.warning("MkDocs server already running at %s", self._url)
            return self._url

        mkdocs_yml = self.docs_dir / "mkdocs.yml"
        if not mkdocs_yml.exists():
            raise FileNotFoundError(f"mkdocs.yml not found at {mkdocs_yml}")

        # Find available port
        if not is_port_available(self.port):
            old_port = self.port
            self.port = find_available_port(self.port)
            logger.info("Port %d occupied, using %d instead", old_port, self.port)

        addr = f"{self.host}:{self.port}"
        cmd = [
            sys.executable, "-m", "mkdocs",
            "serve",
            "--dev-addr", addr,
            "--quiet",
        ]

        logger.info("Starting MkDocs server: %s", " ".join(cmd))
        self._process = subprocess.Popen(
            cmd,
            cwd=str(self.docs_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=lambda: signal.signal(signal.SIGINT, signal.SIG_IGN),
        )

        self._url = f"http://localhost:{self.port}"
        logger.info("MkDocs server started at %s (PID %d)", self._url, self._process.pid)
        return self._url

    def stop(self) -> None:
        """Stop the MkDocs server."""
        if self._process is None:
            return

        if self._process.poll() is None:
            logger.info("Stopping MkDocs server (PID %d)...", self._process.pid)
            self._process.terminate()
            try:
                self._process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._process.kill()
                self._process.wait(timeout=2)

        self._process = None
        self._url = ""
        logger.info("MkDocs server stopped")

    async def wait_ready(self, timeout: float = 10.0) -> bool:
        """Wait until the server responds to HTTP requests."""
        import httpx

        deadline = asyncio.get_event_loop().time() + timeout
        while asyncio.get_event_loop().time() < deadline:
            if not self.running:
                return False
            try:
                async with httpx.AsyncClient(timeout=2) as client:
                    resp = await client.get(self._url)
                    if resp.status_code == 200:
                        return True
            except Exception:
                pass
            await asyncio.sleep(0.5)
        return False

    def __del__(self) -> None:
        self.stop()
