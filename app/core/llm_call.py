"""LLM chat flow for human-in-the-loop idea evaluation."""

import asyncio
import os
from typing import Dict, List

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from typing_extensions import TypedDict

load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    raise ValueError("GROQ_API_KEY is not set in environment variables.")


class State(TypedDict):
    """State used by the idea evaluation flow."""

    idea: str
    messages: List[BaseMessage]
    advisor_reports: Dict[str, str]
    final_report: str


BASE_SYSTEM_MSG = SystemMessage(
    content=(
        "You are a startup idea evaluator. "
        "Your first job is to decide whether you have enough information about the startup idea. "
        "If you do not have enough information, ask exactly ONE precise follow-up question. "
        "If you do have enough information, reply with exactly: DONE"
    )
)


def get_chat_model(model_name: str) -> ChatGroq:
    """Create and return a Groq chat model instance.

    Args:
        model_name: Name of the model to initialize.

    Returns:
        Configured ChatGroq instance.
    """
    return ChatGroq(
        model=model_name,
        api_key=groq_key,
        temperature=0,
    )


async def _invoke_model(messages: List[BaseMessage], model_name: str) -> AIMessage:
    """Invoke the selected model with the provided messages.

    Args:
        messages: Messages to send to the model.
        model_name: Name of the LLM model.

    Returns:
        AI response message.
    """
    chat = get_chat_model(model_name)
    response = await chat.ainvoke(messages)
    return AIMessage(content=response.content)


async def _advisor_report(role_prompt: str, state: State, model_name: str) -> str:
    """Generate a single advisor report.

    Args:
        role_prompt: Advisor role instructions.
        state: Current workflow state.
        model_name: Name of the LLM model.

    Returns:
        Advisor report text.
    """
    chat = get_chat_model(model_name)
    prompt = f"""
You are a helpful senior advisor.

{role_prompt}

Evaluate this startup idea conversation:
{[msg.content for msg in state["messages"]]}
"""
    response = await chat.ainvoke([SystemMessage(content=prompt)])
    return str(response.content)


async def llm_chat(user_query: str, conversation_id: str, model_name: str) -> dict:
    """Process one step of the human-in-the-loop chat flow.

    Args:
        user_query: Latest user message.
        conversation_id: Unique conversation identifier.
        model_name: Selected model name.

    Returns:
        Dictionary containing response text and status.

    Raises:
        ValueError: If required inputs are invalid.
    """
    if not user_query or not user_query.strip():
        raise ValueError("user_query cannot be empty.")

    if not conversation_id or not conversation_id.strip():
        raise ValueError("conversation_id cannot be empty.")

    # For now, this handles one request step at a time.
    # True persistent multi-turn memory should be added through a database or checkpoint store.
    state: State = {
        "idea": user_query.strip(),
        "messages": [HumanMessage(content=user_query.strip())],
        "advisor_reports": {},
        "final_report": "",
    }

    decision_response = await _invoke_model(
        [BASE_SYSTEM_MSG] + state["messages"],
        model_name=model_name,
    )

    decision_text = decision_response.content.strip()

    # Case 1: Need follow-up question from user
    if not decision_text.upper().startswith("DONE"):
        return {
            "response": decision_text,
            "status": "follow_up",
        }

    # Case 2: Enough info, run advisor evaluations
    results = await asyncio.gather(
        _advisor_report(
            role_prompt=(
                "Evaluate market potential, competition, target demographics, and trends. "
                "Conduct market sizing and competitor research. "
                "Identify target customers and segments. "
                "Assess timing, trends, and macroeconomic influences."
            ),
            state=state,
            model_name=model_name,
        ),
        _advisor_report(
            role_prompt=(
                "Identify IP, licensing, and trademark needs. "
                "Spot compliance issues such as GDPR or industry-specific regulations. "
                "Evaluate contract and partnership considerations."
            ),
            state=state,
            model_name=model_name,
        ),
        _advisor_report(
            role_prompt=(
                "Estimate development complexity and time. "
                "Recommend tech stacks or platforms. "
                "Evaluate infrastructure, scalability, and cost risks."
            ),
            state=state,
            model_name=model_name,
        ),
        _advisor_report(
            role_prompt=(
                "Define launch milestones. "
                "Select distribution channels and positioning strategies. "
                "Craft early traction tactics such as community, influencers, or PR."
            ),
            state=state,
            model_name=model_name,
        )
    )

    state["advisor_reports"]["Market Analyst"] = results[0]
    state["advisor_reports"]["Legal Advisor"] = results[1]
    state["advisor_reports"]["Technical Advisor"] = results[2]
    state["advisor_reports"]["Strategist Advisor"] = results[3]

    report_chat = get_chat_model(model_name)
    final_prompt = f"""
You are a senior consultant.

Combine these advisor notes into one clear, structured startup evaluation report
for the founder.

Advisor notes:
{state["advisor_reports"]}
"""
    final_response = await report_chat.ainvoke([SystemMessage(content=final_prompt)])
    final_report = str(final_response.content)
    state["final_report"] = final_report

    return {
        "response": final_report,
        "status": "completed",
    }