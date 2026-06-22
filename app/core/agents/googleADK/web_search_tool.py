"""Provider-agnostic web search tool.

ADK's built-in `google_search` tool only works with native Gemini models --
it raises ValueError against anything routed through LiteLLM (Groq included),
even when Gemini is just the fallback model. A plain function tool sidesteps
that entirely: tool-calling itself works the same regardless of which
provider (Groq or Gemini) ends up handling the request.

Tries Tavily first (https://www.tavily.com -- generous free tier, built for
LLM agents), falls back to Google Custom Search JSON API if Tavily fails or
isn't configured.
"""

import os

import httpx

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
GOOGLE_CSE_API_KEY = os.environ.get("GOOGLE_CSE_API_KEY")
GOOGLE_CSE_ENGINE_ID = os.environ.get("GOOGLE_CSE_ENGINE_ID")


def _tavily_search(query: str, max_results: int = 5) -> list[dict]:
    resp = httpx.post(
        "https://api.tavily.com/search",
        json={"api_key": TAVILY_API_KEY, "query": query, "max_results": max_results},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    return [
        {"title": r.get("title", ""), "url": r.get("url", ""), "snippet": r.get("content", "")}
        for r in data.get("results", [])
    ]


def _google_cse_search(query: str, max_results: int = 5) -> list[dict]:
    resp = httpx.get(
        "https://www.googleapis.com/customsearch/v1",
        params={
            "key": GOOGLE_CSE_API_KEY,
            "cx": GOOGLE_CSE_ENGINE_ID,
            "q": query,
            "num": max_results,
        },
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    return [
        {"title": i.get("title", ""), "url": i.get("link", ""), "snippet": i.get("snippet", "")}
        for i in data.get("items", [])
    ]


def web_search(query: str) -> dict:
    """Search the web and return a list of {title, url, snippet} results.

    Tries Tavily first; automatically falls back to Google Custom Search if
    Tavily fails (rate limit, network error, missing API key) or isn't
    configured at all.
    """
    if TAVILY_API_KEY:
        try:
            return {"source": "tavily", "results": _tavily_search(query)}
        except Exception as exc:  # noqa: BLE001 -- any failure triggers fallback
            tavily_error = str(exc)
    else:
        tavily_error = "TAVILY_API_KEY not set"

    if GOOGLE_CSE_API_KEY and GOOGLE_CSE_ENGINE_ID:
        try:
            return {"source": "google_cse", "results": _google_cse_search(query)}
        except Exception as exc:  # noqa: BLE001
            return {"source": "none", "results": [], "error": f"tavily: {tavily_error}; google_cse: {exc}"}

    return {"source": "none", "results": [], "error": f"tavily: {tavily_error}; google_cse not configured"}