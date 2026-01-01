from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from app import settings

from app.routes import router
from app.core.logging import setup_logging
from app.core.middleware import logging_middleware


setup_logging()

app = FastAPI(
    title=settings.TITLE_API,
    version=settings.VERSION_API,
    description="API encargada de realizar registros a áreas como finanzas, deportes, hábitos entre otros."
)

app.middleware("http")(logging_middleware)
app.include_router(router)


@app.get(
    path="/", 
    include_in_schema=False,
    status_code=status.HTTP_307_TEMPORARY_REDIRECT
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