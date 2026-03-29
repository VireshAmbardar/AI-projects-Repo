import os

from app.core.retriver import hybrid_retrieve

os.environ["CHROMA_ANONYMIZED_TELEMETRY"] = "FALSE"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

from fastapi import FastAPI, File, UploadFile,APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from typing import Optional

from app.settings import settings
from app.core.ingest import ingest_pdfs
from app.schemas.chat import ChatInput

PREFIX = "/api"
VERSION = "v1"



docs_url: Optional[str] = f"{PREFIX}/docs"
openapi_url: Optional[str] = f"{PREFIX}/{VERSION}/openapi.json"

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url=docs_url,
    openapi_url=openapi_url,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# upload_file_router = APIRouter(tags=["File Upload"])
# chat_router = APIRouter(tags=["Chat"])


# @upload_file_router.post("/upload-pdfs")
# async def upload_pdfs(files: List[UploadFile] = File(...)):
#     """
#     Upload multiple PDF files.

#     This endpoint accepts a list of files and returns
#     their filenames and content types.
#     """
#     report  = ingest_pdfs(
#         files
#     )

#     return JSONResponse(
#         content={
#             "report": report,
#         }
#     )



# @chat_router.post("/chat")
# async def chat_with_pdfs(chat_input: ChatInput):
#     """
#     Chat with the ingested PDF documents.

#     This endpoint accepts a user message and returns
#     a placeholder response.
#     """
#     # Placeholder response # to be made functional
#     # response = f"Received your message: {chat_input.user_message}"

#     retrieved  =  hybrid_retrieve(query_text = chat_input.user_message)
    
#     return JSONResponse(
#         content={
#             "response": retrieved ,
#         }
#     )
   
    

app.include_router(upload_file_router)
app.include_router(chat_router)