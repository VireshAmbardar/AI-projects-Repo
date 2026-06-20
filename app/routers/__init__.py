from fastapi import APIRouter

from .heartbeat import router as hbrouter
from .googeadkrouter import router as adkrouter
from .langraph import router as lgrouter
from .sse_router import router as sserouter

router = APIRouter()

router.include_router(hbrouter)
router.include_router(adkrouter)
router.include_router(lgrouter)
router.include_router(sserouter)

__all__ = ["router"]