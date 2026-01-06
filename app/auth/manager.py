from fastapi import Depends
from fastapi_users import BaseUserManager
from app.models.usuario import Usuario
from app.auth.dependencies import get_user_db
from app.settings import SECRET


class UserManager(BaseUserManager[Usuario, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET


async def get_user_manager(
    user_db=Depends(get_user_db),
):
    yield UserManager(user_db)