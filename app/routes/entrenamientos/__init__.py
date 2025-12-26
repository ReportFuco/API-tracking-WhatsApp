from fastapi import APIRouter
from .gimnasio import router as gimnasio_router
from .fuerza import router as fuerza_router


router = APIRouter(prefix="/entrenamientos")

router.include_router(gimnasio_router)
router.include_router(fuerza_router)