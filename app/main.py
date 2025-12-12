from fastapi import FastAPI
from app import settings
from app.routes import (
    webhook,
    finanzas,
    usuario
)

app = FastAPI()

# Rutas de la App
app.include_router(usuario.router)
app.include_router(webhook.router)
app.include_router(finanzas.router)


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
        reload=True
    )