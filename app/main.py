from fastapi import FastAPI
from app import settings
from app.routes import (
    webhook,
    finanzas
)


app = FastAPI()

# Rutas de la App
app.include_router(webhook.router)
app.include_router(finanzas.router)

@app.get("/", tags=["Inicio"])
def bienvenida() -> dict[str, str]:
    return {
        "info": "Bienvenido a la API de automatización",
        "docs": f"Puedes consultar la documentación a través del siguiente link: {settings.URL_SITE}/docs"
    }

if __name__=="__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=settings.PORT, 
        reload=True
    )