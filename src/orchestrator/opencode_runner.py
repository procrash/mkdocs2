"""Wrapper for running LLM queries via opencode CLI or direct HTTP API."""
from __future__ import annotations
import asyncio
import logging
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

# Module-level config for direct API fallback (set by engine before first call)
_server_url: str = ""
_api_key: str = ""
_timeout_read: int = 120


def configure_http_fallback(server_url: str, api_key: str = "", timeout_read: int = 120) -> None:
    """Configure the direct HTTP API fallback."""
    global _server_url, _api_key, _timeout_read
    _server_url = server_url.rstrip("/")
    _api_key = api_key
    _timeout_read = timeout_read


@dataclass
class OpenCodeResult:
    """Result of an LLM invocation."""
    success: bool
    output: str
    error: str = ""
    model_id: str = ""
    duration_seconds: float = 0.0
    retries: int = 0


def find_opencode_binary() -> str | None:
    """Find opencode binary in PATH."""
    return shutil.which("opencode")


async def run_opencode(
    prompt: str,
    model_id: str,
    timeout: int = 120,
    max_retries: int = 3,
    retry_delay: int = 2,
    working_dir: str | None = None,
    mock_mode: bool = False,
    max_tokens: int = 4096,
) -> OpenCodeResult:
    """Run an LLM query and return the result.

    Tries opencode CLI first, falls back to direct HTTP API if unavailable.
    """
    if mock_mode:
        return _mock_response(prompt, model_id)

    # Prefer direct HTTP API (faster, no subprocess overhead, handles long prompts)
    if _server_url:
        return await _run_via_http(
            prompt, model_id, timeout, max_retries, retry_delay, max_tokens
        )

    # Fallback: opencode CLI
    binary = find_opencode_binary()
    if binary:
        return await _run_via_opencode(
            binary, prompt, model_id, timeout, max_retries, retry_delay, working_dir
        )

    return OpenCodeResult(
        success=False,
        output="",
        error="Neither HTTP server nor opencode binary configured",
        model_id=model_id,
    )


async def _run_via_opencode(
    binary: str,
    prompt: str,
    model_id: str,
    timeout: int,
    max_retries: int,
    retry_delay: int,
    working_dir: str | None,
) -> OpenCodeResult:
    """Run via opencode CLI subprocess."""
    prompt_file = Path(tempfile.mktemp(suffix=".txt", prefix="oc_prompt_"))
    prompt_file.write_text(prompt, encoding="utf-8")

    cmd = [binary, "run", "--model", model_id, "--input", str(prompt_file)]

    last_error = ""
    for attempt in range(max_retries):
        import time
        start = time.monotonic()
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=working_dir,
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            duration = time.monotonic() - start
            stdout_text = stdout.decode("utf-8", errors="replace")
            stderr_text = stderr.decode("utf-8", errors="replace")

            if proc.returncode == 0:
                prompt_file.unlink(missing_ok=True)
                return OpenCodeResult(
                    success=True, output=stdout_text,
                    error=stderr_text if stderr_text else "",
                    model_id=model_id, duration_seconds=duration, retries=attempt,
                )
            else:
                last_error = stderr_text or f"Exit code: {proc.returncode}"
                logger.warning("opencode attempt %d/%d failed for %s: %s",
                               attempt + 1, max_retries, model_id, last_error)

        except asyncio.TimeoutError:
            last_error = f"Timeout after {timeout}s"
            logger.warning("opencode attempt %d/%d timed out for %s",
                           attempt + 1, max_retries, model_id)
        except Exception as exc:
            last_error = str(exc)
            logger.error("opencode attempt %d/%d error for %s: %s",
                         attempt + 1, max_retries, model_id, exc)

        if attempt < max_retries - 1:
            delay = retry_delay * (2 ** attempt)
            await asyncio.sleep(delay)

    prompt_file.unlink(missing_ok=True)
    return OpenCodeResult(
        success=False, output="", error=last_error,
        model_id=model_id, retries=max_retries,
    )


async def _run_via_http(
    prompt: str,
    model_id: str,
    timeout: int,
    max_retries: int,
    retry_delay: int,
    max_tokens: int = 4096,
) -> OpenCodeResult:
    """Run via direct OpenAI-compatible HTTP API."""
    import httpx
    import time

    # Strip provider prefix (e.g. "local-server/model-name" -> "model-name")
    raw_model = model_id.split("/", 1)[-1] if "/" in model_id else model_id

    headers = {"Content-Type": "application/json"}
    if _api_key:
        headers["Authorization"] = f"Bearer {_api_key}"

    payload = {
        "model": raw_model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": max_tokens,
    }

    url = f"{_server_url}/v1/chat/completions"
    last_error = ""

    for attempt in range(max_retries):
        start = time.monotonic()
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(
                connect=10.0, read=float(timeout), write=10.0, pool=10.0
            )) as client:
                response = await client.post(url, json=payload, headers=headers)
                duration = time.monotonic() - start

                if response.status_code == 200:
                    data = response.json()
                    content = ""
                    choices = data.get("choices", [])
                    if choices:
                        message = choices[0].get("message", {})
                        content = message.get("content", "")

                    if content:
                        return OpenCodeResult(
                            success=True, output=content,
                            model_id=model_id, duration_seconds=duration,
                            retries=attempt,
                        )
                    else:
                        last_error = "Empty response from API"
                        logger.warning("HTTP attempt %d/%d: empty response for %s",
                                       attempt + 1, max_retries, model_id)
                else:
                    last_error = f"HTTP {response.status_code}: {response.text[:200]}"
                    logger.warning("HTTP attempt %d/%d failed for %s: %s",
                                   attempt + 1, max_retries, model_id, last_error)

        except httpx.TimeoutException:
            duration = time.monotonic() - start
            last_error = f"HTTP timeout after {duration:.0f}s"
            logger.warning("HTTP attempt %d/%d timed out for %s",
                           attempt + 1, max_retries, model_id)
        except Exception as exc:
            duration = time.monotonic() - start
            last_error = str(exc)
            logger.error("HTTP attempt %d/%d error for %s: %s",
                         attempt + 1, max_retries, model_id, exc)

        if attempt < max_retries - 1:
            delay = retry_delay * (2 ** attempt)
            await asyncio.sleep(delay)

    return OpenCodeResult(
        success=False, output="", error=last_error,
        model_id=model_id, retries=max_retries,
    )


def _mock_response(prompt: str, model_id: str) -> OpenCodeResult:
    """Generate a mock response for testing."""
    mock_output = f"""# Mock Documentation

This is a mock response from model `{model_id}`.

## Overview
Mock documentation generated for testing purposes.

## Details
The prompt contained {len(prompt)} characters.

```mermaid
classDiagram
    class MockClass {{
        +mockMethod() void
    }}
```

Formula example: $E = mc^2$
"""
    return OpenCodeResult(
        success=True, output=mock_output,
        model_id=model_id, duration_seconds=0.1,
    )
