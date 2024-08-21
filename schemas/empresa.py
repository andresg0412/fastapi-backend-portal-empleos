from pydantic import BaseModel
from typing import Optional

class EmpresaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    ubicacion: Optional[str] = None

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaUpdate(EmpresaBase):
    pass

class Empresa(EmpresaBase):
    id: int

    class Config:
        orm_mode = True
