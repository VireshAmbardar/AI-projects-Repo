"""Risk Agent -- scores candidate bonds against the user's risk appetite."""

from google.adk.agents import LlmAgent

from app.core.agents.googleADK.model_config import get_model

RISK_AGENT_INSTRUCTION = """
You are the Risk Agent in a bond investment advisory pipeline.

Given a list of candidate bonds and the user's stated risk appetite
(Low / Medium / High), score each bond's risk (credit rating, duration,
issuer type) and flag any that don't match the user's appetite. Output a
risk-annotated version of the candidate list.

Don't decide the final portfolio -- that's the Portfolio Construction
Agent's job.
"""

risk_agent = LlmAgent(
    name="risk_agent",
    model=get_model(),
    description=(
        "Scores candidate bonds' risk and flags mismatches against the "
        "user's stated risk appetite."
    ),
    instruction=RISK_AGENT_INSTRUCTION,
)