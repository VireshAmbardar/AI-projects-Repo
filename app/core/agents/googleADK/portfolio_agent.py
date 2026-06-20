"""Portfolio Construction Agent -- allocates capital across risk-scored bonds."""

from google.adk.agents import LlmAgent

from app.core.agents.googleADK.model_config import MODEL

PORTFOLIO_AGENT_INSTRUCTION = """
You are the Portfolio Construction Agent in a bond investment advisory
pipeline.

Given the user's investment amount, the risk-annotated candidate bonds,
and their income need (e.g. Monthly Income), build a concrete allocation:
which bonds, how much in each (INR and %), and why that mix satisfies the
income need and risk appetite within the stated horizon. Output a
structured allocation table.

Don't write the user-facing explanation -- that's the Recommendation
Agent's job.
"""

portfolio_agent = LlmAgent(
    name="portfolio_agent",
    model=MODEL,
    description=(
        "Builds a concrete bond allocation (which bonds, how much in each) "
        "from risk-scored candidates and the user's goal."
    ),
    instruction=PORTFOLIO_AGENT_INSTRUCTION,
)