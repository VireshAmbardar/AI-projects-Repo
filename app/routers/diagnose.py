"Diagnosis Endpoint"
from app.schemas.chat import ChatInput
from app.schemas.chat import ChatResponse
from app.schemas.chat import Models
from fastapi import APIRouter,status
from app.core.llm_call import llm_chat


router = APIRouter(prefix="/diagnose", tags=["Chat"])

@router.post('', response_model=ChatResponse, status_code=status.HTTP_200_OK)
def chat_llm(
    chat_input:ChatInput,   
    model :Models
    )->ChatResponse:

    # user_query_1 = "I have been experiencing fever, dry cough, and mild chest pain for the past 3 days. I also feel tired and have slight difficulty breathing. I don’t have any major medical history, but I recently traveled in crowded public transport."
    # user_query_2 = "So for the past 4–5 days, I’ve been having this constant cough along with chest tightness. Initially, I thought it was just a cold, but now I also feel short of breath sometimes, especially at night. I don’t have any major illness history, but I do smoke occasionally."
    # user_query_3 = "For the past week, I have been dealing with stomach pain, bloating, and occasional diarrhea. I recently ate a lot of outside food. No prior history of digestive issues."
    # user_query_4 = "I’ve been feeling anxious, having trouble sleeping, and experiencing a fast heartbeat for about 10 days. I recently went through a stressful situation at work."
    # user_query_5 = "Fever, chills, headache since 2 days."
    
    # text =  llm_chat(user_query_1) 
    # print(text)
    conversation_id = "1"

    return ChatResponse(
        conversation_id=chat_input.conversation_id,

        response=llm_chat(chat_input.user_message,
        conversation_id=chat_input.conversation_id,
        model_name=model.value),
    )