"""Probe OpenAI-compatible servers for available models and their context lengths."""
from __future__ import annotations
import logging
from dataclasses import dataclass, field

import httpx

logger = logging.getLogger(__name__)


@dataclass
class DiscoveredModel:
    """A model discovered from an OpenAI-compatible API."""
    id: str
    owned_by: str = ""
    object_type: str = "model"
    context_length: int = 0        # 0 = unknown, will be detected
    raw: dict = field(default_factory=dict)


async def probe_server(base_url: str, api_key: str = "", timeout: int = 10) -> list[DiscoveredModel]:
    """Query /v1/models endpoint and return discovered models with context lengths."""
    url = base_url.rstrip("/")
    if not url.endswith("/v1"):
        url += "/v1"
    models_url = f"{url}/models"

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.get(models_url, headers=headers)
            resp.raise_for_status()
            data = resp.json()
    except httpx.ConnectError:
        logger.error("Cannot connect to %s", models_url)
        return []
    except httpx.HTTPStatusError as exc:
        logger.error("HTTP error from %s: %s", models_url, exc.response.status_code)
        return []
    except Exception as exc:
        logger.error("Error probing %s: %s", models_url, exc)
        return []

    models_list = data.get("data", [])
    result = []
    for m in models_list:
        # Try to extract context length from API response
        ctx = _extract_context_length(m)
        result.append(DiscoveredModel(
            id=m.get("id", ""),
            owned_by=m.get("owned_by", ""),
            object_type=m.get("object", "model"),
            context_length=ctx,
            raw=m,
        ))

    # For models without context length: try Ollama /api/show endpoint
    base_no_v1 = base_url.rstrip("/")
    if base_no_v1.endswith("/v1"):
        base_no_v1 = base_no_v1[:-3]

    for model in result:
        if model.context_length == 0:
            model.context_length = await _probe_ollama_context(
                base_no_v1, model.id, api_key, timeout
            )

    logger.info("Discovered %d models at %s", len(result), models_url)
    return result


def _extract_context_length(model_data: dict) -> int:
    """Extract context length from various API response formats.

    Different servers (OpenAI, vLLM, Ollama, llama.cpp) return this
    in different fields.
    """
    # OpenAI / vLLM
    if "context_length" in model_data:
        return int(model_data["context_length"])
    if "max_model_len" in model_data:
        return int(model_data["max_model_len"])

    # llama.cpp server
    if "meta" in model_data and isinstance(model_data["meta"], dict):
        meta = model_data["meta"]
        for key in ("n_ctx_train", "context_length", "max_seq_len"):
            if key in meta:
                return int(meta[key])

    # Ollama-style (sometimes in details)
    details = model_data.get("details", {})
    if isinstance(details, dict):
        for key in ("context_length", "parameter_size"):
            if key in details:
                try:
                    return int(details[key])
                except (ValueError, TypeError):
                    pass

    return 0


async def _probe_ollama_context(
    base_url: str, model_id: str, api_key: str = "", timeout: int = 5,
) -> int:
    """Try Ollama's /api/show endpoint to get context length for a model."""
    show_url = f"{base_url}/api/show"
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(
                show_url,
                json={"name": model_id},
                headers=headers,
            )
            if resp.status_code != 200:
                return 0
            data = resp.json()

            # Ollama returns model_info with context length keys
            model_info = data.get("model_info", {})
            for key, value in model_info.items():
                if "context_length" in key.lower():
                    return int(value)

            # Also check parameters string for num_ctx
            params_str = data.get("parameters", "")
            if isinstance(params_str, str):
                for line in params_str.splitlines():
                    if "num_ctx" in line:
                        parts = line.split()
                        for p in parts:
                            try:
                                val = int(p)
                                if val > 512:
                                    return val
                            except ValueError:
                                continue

    except Exception:
        pass  # Ollama endpoint not available, that's fine

    return 0


async def probe_ollama_template(
    base_url: str, model_id: str, api_key: str = "", timeout: int = 5,
) -> dict[str, bool]:
    """Check Ollama /api/show for chat template (indicates instruct model)."""
    show_url = f"{base_url}/api/show"
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    result = {"has_template": False, "has_tools_tag": False}
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(show_url, json={"name": model_id}, headers=headers)
            if resp.status_code != 200:
                return result
            data = resp.json()
            template = data.get("template", "")
            if template:
                result["has_template"] = True
                # Check if template contains tool-related tags
                if any(kw in template.lower() for kw in ("<tool", "function", "{tools}", "<tools>")):
                    result["has_tools_tag"] = True
    except Exception:
        pass
    return result


async def probe_context_length(
    base_url: str,
    model_id: str,
    api_key: str = "",
    timeout: int = 30,
    progress_callback=None,
) -> int:
    """Actively probe the real context window of a model via chat completions.

    Sends requests with increasing token counts using a binary search approach.
    Returns the maximum number of tokens the model accepted, or 0 on failure.

    *progress_callback(model_id, current_test, status_msg)* is called on each step.
    """
    url = base_url.rstrip("/")
    if not url.endswith("/v1"):
        url += "/v1"
    completions_url = f"{url}/chat/completions"

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    # The "filler" word we repeat to consume tokens (~1 token per word)
    filler_word = "test "

    async def _try_tokens(n_tokens: int) -> bool:
        """Send a request that consumes roughly *n_tokens* and return success."""
        # Build a long user message.  Most tokenizers average ~4 chars/token,
        # but "test " is reliably 1 token in most BPE tokenizers.
        content = filler_word * n_tokens
        payload = {
            "model": model_id,
            "messages": [{"role": "user", "content": content}],
            "max_tokens": 1,          # We don't need a long answer
            "temperature": 0,
        }
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                resp = await client.post(completions_url, json=payload, headers=headers)
                if resp.status_code == 200:
                    return True
                # Many servers return 400/413/422 when context is exceeded
                body = resp.text.lower()
                if any(kw in body for kw in ("context", "too long", "too many tokens",
                                              "maximum", "exceed", "length")):
                    return False
                # Other errors (rate limit, server error) – treat as inconclusive
                if resp.status_code >= 500:
                    return False
                return False
        except httpx.ReadTimeout:
            # Timeout might mean the server accepted but is slow – treat as success
            return True
        except Exception:
            return False

    # Binary search between low and high
    low = 512
    high = 262144  # Start high – 256k
    last_success = 0

    # First: quick check if the model accepts anything at all
    if progress_callback:
        progress_callback(model_id, low, "Starte Kontextfenster-Diagnose...")
    ok = await _try_tokens(low)
    if not ok:
        logger.warning("Model %s cannot even accept %d tokens", model_id, low)
        return 0
    last_success = low

    # Quick geometric probes: 1k, 2k, 4k, 8k, 16k, 32k, 64k, 128k, 256k
    probes = [1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144]
    upper_bound = None
    for p in probes:
        if progress_callback:
            progress_callback(model_id, p, f"Teste {p:,} tokens...")
        ok = await _try_tokens(p)
        if ok:
            last_success = p
            logger.debug("Model %s accepted %d tokens", model_id, p)
        else:
            upper_bound = p
            logger.debug("Model %s rejected %d tokens", model_id, p)
            break

    if upper_bound is None:
        # Model accepted everything up to 256k
        if progress_callback:
            progress_callback(model_id, last_success, f"Kontextfenster ≥ {last_success:,}")
        return last_success

    # Binary search between last_success and upper_bound
    low = last_success
    high = upper_bound
    while high - low > 1024:
        mid = (low + high) // 2
        # Round to nearest 512 for cleaner results
        mid = (mid // 512) * 512
        if mid == low:
            break
        if progress_callback:
            progress_callback(model_id, mid, f"Binäre Suche: {low:,}-{high:,}, teste {mid:,}...")
        ok = await _try_tokens(mid)
        if ok:
            low = mid
            last_success = mid
        else:
            high = mid

    if progress_callback:
        progress_callback(model_id, last_success, f"Kontextfenster: {last_success:,} tokens")
    logger.info("Model %s: probed context length = %d tokens", model_id, last_success)
    return last_success


async def probe_all_context_lengths(
    base_url: str,
    models: list[DiscoveredModel],
    api_key: str = "",
    timeout: int = 30,
    progress_callback=None,
) -> dict[str, int]:
    """Actively probe context lengths for all models that don't have one yet.

    Returns a dict mapping model_id → detected context length.
    """
    results: dict[str, int] = {}
    for model in models:
        if model.context_length > 0:
            results[model.id] = model.context_length
            continue
        ctx = await probe_context_length(
            base_url, model.id, api_key, timeout, progress_callback
        )
        if ctx > 0:
            results[model.id] = ctx
            model.context_length = ctx
    return results


async def probe_tool_support(
    base_url: str,
    model_id: str,
    api_key: str = "",
    timeout: int = 15,
) -> dict[str, bool]:
    """Probe whether a model supports tool/function calling and is instruct-tuned.

    Returns {"tool_use": bool, "instruct": bool}.
    """
    url = base_url.rstrip("/")
    if not url.endswith("/v1"):
        url += "/v1"
    completions_url = f"{url}/chat/completions"

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    result = {"tool_use": False, "instruct": False}

    # 1. Check instruct: does it follow a simple instruction?
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(completions_url, json={
                "model": model_id,
                "messages": [{"role": "user", "content": "Reply with exactly the word HELLO and nothing else."}],
                "max_tokens": 10,
                "temperature": 0,
            }, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                content = (data.get("choices", [{}])[0]
                           .get("message", {}).get("content", ""))
                # If the model follows instructions, it's instruct-tuned
                if "hello" in content.lower():
                    result["instruct"] = True
                elif content.strip():
                    # Got a coherent response at all → likely instruct
                    result["instruct"] = True
    except Exception:
        pass

    # 2. Check tool use: send a request with tools parameter
    test_tool = {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"},
                },
                "required": ["city"],
            },
        },
    }
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(completions_url, json={
                "model": model_id,
                "messages": [{"role": "user", "content": "What is the weather in Berlin?"}],
                "tools": [test_tool],
                "max_tokens": 100,
                "temperature": 0,
            }, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                msg = data.get("choices", [{}])[0].get("message", {})
                # Check if model returned tool calls
                tool_calls = msg.get("tool_calls", [])
                if tool_calls:
                    result["tool_use"] = True
                else:
                    # Some models put function_call at message level
                    if msg.get("function_call"):
                        result["tool_use"] = True
                    # Even if no tool call, server accepted the request → basic support
                    elif resp.status_code == 200:
                        result["tool_use"] = True
            elif resp.status_code in (400, 422):
                # Server explicitly rejected tools → no support
                result["tool_use"] = False
    except Exception:
        pass

    # 3. Fallback: check Ollama template for instruct/tool hints
    if not result["instruct"] or not result["tool_use"]:
        base_no_v1 = base_url.rstrip("/")
        if base_no_v1.endswith("/v1"):
            base_no_v1 = base_no_v1[:-3]
        tpl = await probe_ollama_template(base_no_v1, model_id, api_key, timeout)
        if tpl["has_template"] and not result["instruct"]:
            result["instruct"] = True
        if tpl["has_tools_tag"] and not result["tool_use"]:
            result["tool_use"] = True

    logger.info("Model %s: instruct=%s, tool_use=%s", model_id, result["instruct"], result["tool_use"])
    return result


async def probe_all_capabilities(
    base_url: str,
    models: list[DiscoveredModel],
    api_key: str = "",
    timeout: int = 15,
    progress_callback=None,
) -> dict[str, set[str]]:
    """Probe instruct/tool capabilities for all models.

    Returns a dict mapping model_id → set of capability strings.
    """
    results: dict[str, set[str]] = {}
    for model in models:
        if progress_callback:
            progress_callback(model.id, 0, f"Prüfe Capabilities: {model.id}...")
        probed = await probe_tool_support(base_url, model.id, api_key, timeout)
        caps: set[str] = set()
        if probed["tool_use"]:
            caps.add("tool_use")
        if probed["instruct"]:
            caps.add("instruct")
        if caps:
            results[model.id] = caps
    return results


async def check_server_health(base_url: str, api_key: str = "", timeout: int = 5) -> bool:
    """Quick health check - can we reach the server?"""
    try:
        models = await probe_server(base_url, api_key, timeout)
        return len(models) > 0
    except Exception:
        return False
