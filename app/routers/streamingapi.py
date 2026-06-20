from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()

# @router.post("/chat/stream")
# async def stream_chat(query: str):

#     async def event_generator():

#         async for event in agent.run_stream(query):

#             yield f"data: {event}\n\n"

#     return StreamingResponse(
#         event_generator(),
#         media_type="text/event-stream"
#     )