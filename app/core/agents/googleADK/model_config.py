"""Shared model id for every ADK agent in this app.

Pulled out of base.py so sub-agent files can import MODEL without creating
a circular import (base.py imports the sub-agents to wire them into
root_agent's tools).
"""

# TODO verify this against Google's current Gemini model list before relying
# on it -- can't confirm "gemini-3.5-flash" is a real/available model id.
MODEL = "gemini-3.5-flash"