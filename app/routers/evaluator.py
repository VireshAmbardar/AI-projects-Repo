"Evaluator Endpoint"
from app.schemas.chat import ChatInput
from app.schemas.chat import ChatResponse
from app.schemas.chat import Models
from fastapi import APIRouter,status, HTTPException
from app.core.llm_call import llm_chat


router = APIRouter(prefix="/idea-chat", tags=["Idea Chat"])

@router.post('', response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat_llm(
    chat_input:ChatInput,   
    model :Models
    )->ChatResponse:

    """Run the human-in-the-loop idea chat flow."""

    try:
        result = await llm_chat(
            user_query=chat_input.user_message,
            conversation_id=chat_input.conversation_id,
            model_name=model.value,
        )

        return ChatResponse(
            conversation_id=chat_input.conversation_id,
            response=result["response"],
            status=result["status"],
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process idea chat request.",
        ) from exc