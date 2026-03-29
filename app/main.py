from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from app import settings
from app.auth.routes import router as auth_router
from app.routes import router
from app.core.logging import setup_logging
from app.core.middleware import logging_middleware


setup_logging()

app = FastAPI(
    title=settings.TITLE_API,
    version=settings.VERSION_API,
    description="API encargada de realizar registros a áreas como finanzas, deportes, hábitos entre otros.",
    docs_url="/docs",
    redoc_url="/redoc",
)

# -------------------------
# CORS
# -------------------------

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://100.124.185.116:3000",
    "http://100.107.250.78:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Middleware
# -------------------------

app.middleware("http")(logging_middleware)

# -------------------------
# Routers
# -------------------------

app.include_router(router)
app.include_router(auth_router)

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