from fastapi import APIRouter
from .gimnasio import router as gimnasio_router


router = APIRouter(prefix="/entrenamientos")

router.include_router(gimnasio_router)