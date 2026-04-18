from fastapi import APIRouter

from .marca import router as marca_router
from .producto import router as producto_router

router = APIRouter(prefix="/catalogo")
router.include_router(marca_router)
router.include_router(producto_router)

__all__ = ["router"]
