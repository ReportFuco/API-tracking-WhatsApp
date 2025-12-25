from pydantic import BaseModel


class Ejemplo(BaseModel):
    nombre: str
    edad: int | None = None
    activo: str | None


ejemplo1 = Ejemplo(nombre="Francsico", activo=None)


print(ejemplo1.model_dump())
print(ejemplo1.model_dump(exclude_unset=True))
print(ejemplo1.model_dump(exclude_none=True))