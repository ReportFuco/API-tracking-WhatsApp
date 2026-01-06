from fastapi_users import FastAPIUsers
from app.auth.manager import get_user_manager
from app.auth.backend import jwt_auth_backend


fastapi_users = FastAPIUsers(
    get_user_manager,
    [jwt_auth_backend],
)

current_user = fastapi_users.current_user(active=True)
