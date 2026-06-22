"""Bond Search Agent -- finds candidate bonds matching the user's goal.

The real "Tool Layer -> Bond APIs" piece from your production architecture
diagram isn't built yet, so search_bonds is a stub. Swap its body for a real
HTTP call once you have a Bond API client (e.g. app/core/tools/bond_api.py).
"""

from google.adk.agents import LlmAgent
from app.core.agents.googleADK.model_config import get_model

from app.core.agents.googleADK.web_search_tool import web_search


def search_bonds(risk_appetite: str, investment_horizon_years: int, income_need: str) -> dict:
    """Search for bonds matching the given criteria.

    TODO: replace this stub with a real call into the Bond API tool layer.
    Returning a fixed shape for now so downstream agents have something
    consistent to parse.
    """
    return {
        "bonds": [],
        "note": "stub data -- wire this up to the real Bond API client",
    }


BOND_SEARCH_INSTRUCTION = """
You are the Bond Search Agent in a bond investment advisory pipeline.

Given the user's risk appetite, investment horizon, and income need, call
the search_bonds tool to fetch candidate bonds. Return the candidate list
plus a one-line rationale per bond (yield, tenure match, credit rating).

Don't filter further or build a portfolio here -- that's the Portfolio
Construction Agent's job.
"""

bond_search_agent = LlmAgent(
    name="bond_search_agent",
    model=get_model(),
    description=(
        "Searches for candidate bonds matching the user's risk appetite, "
        "horizon, and income need."
    ),
    instruction=BOND_SEARCH_INSTRUCTION,
    tools=[web_search],
)