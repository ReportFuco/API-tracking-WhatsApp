from pydantic import BaseModel


class BancoSchema(BaseModel):
    nombre_banco:str

class BancoSchemaCreate(BancoSchema):
    pass

# Cuentas Bancarias

class CuentaBancariaCreate(BaseModel):
    id_usuario: int
    id_banco: int
    nombre_cuenta: str
    tipo_cuenta: str