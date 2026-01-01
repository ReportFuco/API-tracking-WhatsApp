from fastapi import APIRouter
from .entrenamientos import router as entrenamientos_router
from .finanzas import router as finanzas_router
from .lecturas import router as lecturas_router
from .usuarios import router as usuario_router


router = APIRouter(prefix="/api")

router.include_router(entrenamientos_router)
router.include_router(finanzas_router)
router.include_router(lecturas_router)
router.include_router(usuario_router)

__all__ = ["router"]
