from pydantic import BaseModel


class CuentaBancariaCreate(BaseModel):
    id_usuario: int
    id_banco: int
    nombre_cuenta: str
    tipo_cuenta: str

class CuentaBancariaResponse(BaseModel):
    id:int
    usuario:str
    banco: str
    nombre_cuenta: str
    tipo_cuenta:str