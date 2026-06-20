from google.adk.agents import LlmAgent


# ROOT_AGNET_DESCRIPTION="""

# """

# ROOT_INSTRUCTIONS= '''
# '''

# # Free  gemini-3.5-flash or gemini-3.1-flash-lite 
# MODEL = "gemini-3.5-flash"
 
# root_agent = LlmAgent(
#     name='root_agent',
#     model=MODEL,
#     description="Root Agent",
#     instruction="Act as a Financial Assistent that Does the curretn market research Finds the Best bond According to user needs.",
#     # tools=[get_current_time],
# )

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from app.core.agents.googleADK.model_config import get_model
from app.core.agents.googleADK.goal_agent import goal_agent
from app.core.agents.googleADK.bond_search_agent import bond_search_agent
from app.core.agents.googleADK.risk_agent import risk_agent
from app.core.agents.googleADK.portfolio_agent import portfolio_agent
from app.core.agents.googleADK.recommendation_agent import recommendation_agent


ROOT_AGNET_DESCRIPTION = """
Orchestrates the bond investment advisory pipeline: goal analysis, bond
search, risk scoring, portfolio construction, and final recommendation.
"""

ROOT_INSTRUCTIONS = """
You are the Agent Orchestrator for a bond investment advisory system.

Call your tools in this order for a new request:
  1. goal_agent     -- confirm investment_amount, risk_appetite,
                        investment_horizon, income_need are all known.
                        If goal_agent says info is missing, relay its
                        follow-up question to the user and STOP -- wait
                        for their answer before continuing.
  2. bond_search_agent -- once the goal is complete, find candidate bonds.
  3. risk_agent        -- score those candidates against risk_appetite.
  4. portfolio_agent   -- build the concrete allocation.
  5. recommendation_agent -- explain the final recommendation to the user.

After the first full pass, route any user follow-up questions about the
recommendation straight to recommendation_agent rather than re-running the
whole pipeline.
"""

root_agent = LlmAgent(
    name='root_agent',
    model=get_model(),
    description=ROOT_AGNET_DESCRIPTION,
    instruction=ROOT_INSTRUCTIONS,
    tools=[
        AgentTool(agent=goal_agent),
        AgentTool(agent=bond_search_agent),
        AgentTool(agent=risk_agent),
        AgentTool(agent=portfolio_agent),
        AgentTool(agent=recommendation_agent),
    ],
)