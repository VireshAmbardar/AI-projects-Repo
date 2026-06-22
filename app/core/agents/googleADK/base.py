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

On a brand-new conversation, transfer immediately to goal_agent -- it owns
collecting investment_amount, risk_appetite, investment_horizon, and
income_need from the user, including asking follow-up questions and
waiting across multiple turns if needed. You will not see those follow-up
turns; goal_agent handles them directly with the user.

goal_agent will transfer back to you only once all four fields are
confirmed. When that happens, run the rest of the pipeline in order, in a
single pass, without asking the user anything in between:
  1. bond_search_agent -- find candidate bonds.
  2. risk_agent         -- score those candidates against risk_appetite.
  3. portfolio_agent    -- build the concrete allocation.
  4. recommendation_agent -- explain the final recommendation to the user.

After the first full pass, route any user follow-up questions about the
recommendation straight to recommendation_agent rather than re-running the
whole pipeline.
"""

root_agent = LlmAgent(
    name='root_agent',
    model=get_model(),
    description=ROOT_AGNET_DESCRIPTION,
    instruction=ROOT_INSTRUCTIONS,
    sub_agents=[goal_agent],
    tools=[
        AgentTool(agent=bond_search_agent),
        AgentTool(agent=risk_agent),
        AgentTool(agent=portfolio_agent),
        AgentTool(agent=recommendation_agent),
    ],
)