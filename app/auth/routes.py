from app.auth.schemas import UsuarioAuthRead, UsuarioAuthCreate
from fastapi import APIRouter
from fastapi_users.authentication import AuthenticationBackend, BearerTransport

from app.auth.fastapi_users import fastapi_users
from app.auth.jwt import get_jwt_strategy


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

jwt_auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

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
