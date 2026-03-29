from pydantic import BaseModel
from app.models import EnumCuentas


class CuentaBancariaCreate(BaseModel):
    id_usuario: int
    id_banco: int
    nombre_cuenta: str
    tipo_cuenta: EnumCuentas
