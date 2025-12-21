from fastapi import APIRouter
from app.routes.lecturas.libros import router as libros_router
from app.routes.lecturas.registro_lectura import router as lecturas_router


router = APIRouter(prefix="/lecturas")

router.include_router(libros_router)
router.include_router(lecturas_router)