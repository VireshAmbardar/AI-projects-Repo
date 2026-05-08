from google.adk.models.lite_llm import LiteLlm

import os
from dotenv import load_dotenv
load_dotenv()

ollama_llm = LiteLlm(
    model=f"ollama_chat/{os.getenv('DATABASE_URL')}",
    api_base= {os.getenv('OLLAMA_API_BASE')},
)