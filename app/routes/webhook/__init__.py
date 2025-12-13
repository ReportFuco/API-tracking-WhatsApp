from fastapi import APIRouter

from .webhook import router as wenhook_router


router = APIRouter(prefix="/wh")

router.include_router(wenhook_router)