from pydantic import BaseModel
from typing import Optional
from datetime import date

class VacanteBase(BaseModel):
    titulo: str
    subtitulo: Optional[str] = None
    modo: str
    salario: Optional[str] = None
    fecha: date
    descripcion: Optional[str] = None
    estado: Optional[str] = "Activo"
    empresa_id: int

class VacanteCreate(VacanteBase):
    pass

class VacanteUpdate(VacanteBase):
    pass

class Vacante(VacanteBase):
    id: int

    class Config:
        orm_mode = True
