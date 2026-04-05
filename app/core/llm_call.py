from dotenv import load_dotenv
import os
from typing import Dict

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.chat_history import InMemoryChatMessageHistory

load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    raise ValueError("GROQ_API_KEY is not set in environment variables.")

SYSTEM_PROMPT = """
You are an AI-powered medical assistant designed to analyze user-reported symptoms and provide possible health insights. Your role is to assist, not to replace professional medical advice.

Given a user's symptoms and context, generate 2 to 3 possible medical conditions.

For each condition, provide:
1. Condition name
2. Probability (in percentage, realistic and relative, total does not need to be exactly 100%)
3. Brief explanation (1–2 lines connecting symptoms to the condition)
4. Suggested next steps (e.g., diagnostic tests, precautions, or type of doctor to consult)

Guidelines:
- Base your reasoning only on the symptoms and context provided.
- Keep responses clear, structured, and concise.
- Avoid extreme or rare conditions unless strongly justified.
- Do not provide definitive diagnoses; present possibilities only.
- Always include a safety note if symptoms could indicate something serious.
- If symptoms are vague, acknowledge uncertainty and suggest general next steps.
- Maintain a professional and calm tone.

Output Format (STRICT JSON):
{
  "possible_conditions": [
    {
      "condition": "Condition Name",
      "probability": "XX%",
      "explanation": "Short reasoning",
      "next_steps": "Tests or doctor recommendation"
    }
  ],
  "general_advice": "Overall guidance for the user"
}
"""

# In-memory store: one history per conversation
chat_sessions: Dict[str, InMemoryChatMessageHistory] = {}


def get_chat_history(conversation_id: str) -> InMemoryChatMessageHistory:
    """Return the chat history for a conversation, creating it if needed."""
    if conversation_id not in chat_sessions:
        chat_sessions[conversation_id] = InMemoryChatMessageHistory()
    return chat_sessions[conversation_id]


def llm_chat(user_query: str, conversation_id: str, model_name: str) -> str:
    """Call the LLM with per-conversation history."""
    chat = ChatGroq(
        model=model_name,
        api_key=groq_key,
        temperature=0
    )

    history = get_chat_history(conversation_id)

    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    messages.extend(history.messages)
    messages.append(HumanMessage(content=user_query))

    response = chat.invoke(messages)

    history.add_message(HumanMessage(content=user_query))
    history.add_message(AIMessage(content=response.content))

    return response.content


def clear_chat(conversation_id: str) -> None:
    """Clear a conversation history."""
    if conversation_id in chat_sessions:
        del chat_sessions[conversation_id]