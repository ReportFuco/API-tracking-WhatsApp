from fastapi import APIRouter

from .banco import router as banco_router
from .cuentas import router as cuentas_router
from .movimientos import router as movimientos_router
from .categoria import router as categoria_router

router = APIRouter(prefix="/finanzas")

router.include_router(banco_router)
router.include_router(movimientos_router)
router.include_router(cuentas_router)
router.include_router(categoria_router)


__all__ = ["router"]