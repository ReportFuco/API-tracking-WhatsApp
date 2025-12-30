from fastapi import FastAPI
from app import settings
# from app.routes.webhook import router as webhook_router
from app.routes.finanzas import router as router_finanzas
from app.routes.usuarios import router as usuario_router
from app.routes.entrenamientos import router as entrenamientos_router
from app.core.logging import setup_logging
from app.core.middleware import logging_middleware


setup_logging()

app = FastAPI()
app.middleware("http")(logging_middleware)
# Rutas de la App
app.include_router(usuario_router)
# app.include_router(webhook_router)
app.include_router(router_finanzas)
app.include_router(entrenamientos_router)


@app.get("/", tags=["Inicio"], include_in_schema=False)
def bienvenida() -> dict[str, str | list[str]]:
    return {
        "info": "Bienvenido a la API de automatización",
        "docs": f"Puedes consultar la documentación a través del siguiente link: {settings.URL_SITE}/docs",
        "Instrucciones":
            [
                "Debes tener desplegado el servicio de Evolution API en un servidor para interactuar WhatsApp",
                "Debes iniciar el proyecto (python -m app.main) con la IP visible o usando Ngrok para que Evolution API detecte la App",
                "Debes ingresar las KEYS importantes dentro del archivo .env"
            ]
    }

if __name__=="__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=settings.PORT, 
        reload=True,
        access_log=False
    )