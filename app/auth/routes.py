from fastapi import APIRouter

from app.auth.schemas import UsuarioAuthRead, UsuarioAuthCreate
from app.auth.fastapi_users import fastapi_users
from app.auth.backend import jwt_auth_backend

router = APIRouter(prefix="/auth", tags=["Auth"])

router.include_router(
    fastapi_users.get_auth_router(jwt_auth_backend),
    prefix="/jwt",
)

router.include_router(
    fastapi_users.get_register_router(
        UsuarioAuthRead,
        UsuarioAuthCreate,
    ),
)
