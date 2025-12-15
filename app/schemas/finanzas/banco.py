from pydantic import BaseModel


class BancoSchema(BaseModel):
    nombre_banco:str

class BancoSchemaCreate(BancoSchema):
    pass

class BancoResponse(BaseModel):
    nombre:str
    id:int