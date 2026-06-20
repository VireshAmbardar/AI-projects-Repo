"""Recommendation Agent -- explains the portfolio and answers follow-ups.

This is the final, user-facing voice of the pipeline ("Explain
Recommendation" + "Answer Follow-up Questions" in your diagram).
"""

from google.adk.agents import LlmAgent

from app.core.agents.googleADK.model_config import get_model

RECOMMENDATION_AGENT_INSTRUCTION = """
You are the Recommendation Agent in a bond investment advisory pipeline --
the final, user-facing voice of the system.

Given the constructed portfolio allocation, explain it in plain language:
why this mix, how it meets the user's income need and risk appetite, and
what the expected income/return profile looks like over the investment
horizon. Then stay available to answer the user's follow-up questions
about the recommendation.
"""

recommendation_agent = LlmAgent(
    name="recommendation_agent",
    model=get_model(),
    description=(
        "Explains the constructed bond portfolio in plain language and "
        "answers user follow-up questions."
    ),
    instruction=RECOMMENDATION_AGENT_INSTRUCTION,
)