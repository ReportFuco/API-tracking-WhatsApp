from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from . import settings

from app.routes.finanzas import router as router_finanzas
from app.routes.usuarios import router as usuario_router
from app.routes.entrenamientos import router as entrenamientos_router
from app.core.logging import setup_logging
from app.core.middleware import logging_middleware


setup_logging()

app = FastAPI(
    title=settings.TITLE_API,
    version=settings.VERSION_API,
    description="API encargada de realizar registros a áreas como finanzas, deportes, hábitos entre otros."
)

app.middleware("http")(logging_middleware)

# Rutas de la App
app.include_router(usuario_router)
app.include_router(router_finanzas)
app.include_router(entrenamientos_router)


@app.get(
    path="/", 
    include_in_schema=False
)
def bienvenida():
    return RedirectResponse("/docs")


if __name__=="__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=settings.PORT, 
        reload=True,
        access_log=False
    )