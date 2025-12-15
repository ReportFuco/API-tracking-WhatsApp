from pydantic import BaseModel


class CuentaBancariaCreate(BaseModel):
    id_usuario: int
    id_banco: int
    nombre_cuenta: str
    tipo_cuenta: str