"""Shared model config for every ADK agent in this app.

Pulled out of base.py so sub-agent files can import it without creating
a circular import (base.py imports the sub-agents to wire them into
root_agent's tools).

Groq is now the primary provider (fast + generous free-tier rate limits
compared to Gemini's 20 RPM). Gemini is kept as an automatic fallback if
Groq fails for any reason (quota, auth, network).
"""

import logging

from google.adk.models import Gemini
from google.adk.models.base_llm import BaseLlm
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

logger = logging.getLogger(__name__)

# LiteLLM model id format is "<provider>/<model>". Swap GROQ_MODEL for any
# of the other Groq options if you want more speed vs. more reasoning power:
#   "groq/llama-3.1-8b-instant"        -- fastest, lowest cost
#   "groq/llama-3.3-70b-versatile"     -- best balance (default below)
#   "groq/openai/gpt-oss-120b"         -- strongest reasoning
GROQ_MODEL = "groq/llama-3.3-70b-versatile"

# TODO verify this against Google's current Gemini model list before relying
# on it -- can't confirm "gemini-3.5-flash" is a real/available model id.
GEMINI_FALLBACK_MODEL = "gemini-3.5-flash"


class FallbackLlm(BaseLlm):
    """Tries `primary` first; on any exception, retries the same request on `fallback`.

    NOTE: this subclasses ADK's BaseLlm directly to intercept failures per
    LLM call (not per pipeline run, so a Groq hiccup on one sub-agent call
    doesn't restart the whole pipeline). ADK's internal BaseLlm interface
    isn't fully documented publicly -- if this breaks against your installed
    adk version, the traceback will point at generate_content_async; the fix
    is almost always just adjusting that method's signature to match.
    """

    primary: BaseLlm
    fallback: BaseLlm

    model_config = {"arbitrary_types_allowed": True}

    async def generate_content_async(self, llm_request, stream: bool = False):
        try:
            async for response in self.primary.generate_content_async(llm_request, stream):
                yield response
        except Exception as exc:  # noqa: BLE001 -- any failure triggers fallback
            logger.warning(
                "Primary model (%s) failed: %s -- falling back to %s",
                self.primary.model, exc, self.fallback.model,
            )
            async for response in self.fallback.generate_content_async(llm_request, stream):
                yield response


def get_model() -> FallbackLlm:
    groq_model = LiteLlm(model=GROQ_MODEL)
    gemini_model = Gemini(
        model=GEMINI_FALLBACK_MODEL,
        retry_options=types.HttpRetryOptions(
            attempts=3, initial_delay=2.0, max_delay=20.0,
            http_status_codes=[429, 500, 502, 503, 504],
        ),
    )
    return FallbackLlm(model=GROQ_MODEL, primary=groq_model, fallback=gemini_model)