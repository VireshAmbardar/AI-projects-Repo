"main.py"
import os

os.environ["CHROMA_ANONYMIZED_TELEMETRY"] = "FALSE"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

from fastapi import FastAPI, File, UploadFile,APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from typing import Optional
from app.settings import settings
from app.routers import hbrouter,evarouter

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

app.include_router(
        hbrouter, prefix=f"{PREFIX}/{VERSION}"
    )

app.include_router(
        evarouter, prefix=f"{PREFIX}/{VERSION}"
    )

def main():
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=True
    )

if __name__ == "__main__":
    main()