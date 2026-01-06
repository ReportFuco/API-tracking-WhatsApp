from fastapi_users import schemas


class UsuarioAuthRead(schemas.BaseUser[int]):
    id: int
    email: str
    is_active: bool
    is_superuser: bool


class UsuarioAuthCreate(schemas.BaseUserCreate):
    email: str
    password: str
