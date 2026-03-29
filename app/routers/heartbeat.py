"Test file"

import os

import psutil
from fastapi import APIRouter
from starlette.responses import HTMLResponse

router = APIRouter()

@router.get("/")
def heartbeat() -> HTMLResponse:
    """Template function.

    Returns:
        HTMLResponse: Response
    """
    # Getting loadover15 minutes
    load1, load5, load15 = psutil.getloadavg()
    cpu_count = os.cpu_count()
    if cpu_count is None:
        cpu_count = 1
    """Basic HTML response."""
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Hello from MS Azure Openai server!</h1>"
        "<div>"
        "Check the docs: <a href='/api/docs'>here</a>"
        "</div>"
        "<div>"
        f"Memory: {psutil.virtual_memory()}"
        "</div>"
        "<div>"
        f"CPU: {(load1 / cpu_count) * 100}"
        "</div>"
        "</body>"
        "</html>"
    )
    return HTMLResponse(content=body)