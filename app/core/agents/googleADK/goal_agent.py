"""Goal Agent -- extracts and validates the user's investment goal.

Covers the "Analyze Goals" + "checks if it has all the basic information,
if not asks follow up questions" steps from your pipeline diagram.
"""

from google.adk.agents import LlmAgent

from app.core.agents.googleADK.model_config import MODEL

GOAL_AGENT_INSTRUCTION = """
You are the Goal Agent in a bond investment advisory pipeline.

Your job: extract these four fields from the conversation so far:
  - investment_amount (numeric, in INR)
  - risk_appetite (Low / Medium / High)
  - investment_horizon (in years)
  - income_need (Monthly Income / Lump Sum / Growth)

If any field is missing or ambiguous, ask ONE short, specific follow-up
question for the single most important missing field -- don't ask for
everything at once. Once all four are present, summarize them back to the
user in one line.

Never recommend specific bonds yourself -- that's a different agent's job.
"""

goal_agent = LlmAgent(
    name="goal_agent",
    model=MODEL,
    description=(
        "Extracts and validates the user's investment goal (amount, risk "
        "appetite, horizon, income need); asks a follow-up question if "
        "information is missing."
    ),
    instruction=GOAL_AGENT_INSTRUCTION,
)