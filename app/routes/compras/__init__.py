from fastapi import APIRouter

from .cadena import router as cadena_router
from .compra import router as compra_router
from .compra_detalle import router as compra_detalle_router
from .local import router as local_router

router = APIRouter(prefix="/compras")
router.include_router(cadena_router)
router.include_router(local_router)
router.include_router(compra_router)
router.include_router(compra_detalle_router)

__all__ = ["router"]
