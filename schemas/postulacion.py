from pydantic import BaseModel
from typing import Optional
from datetime import date

class PostulacionBase(BaseModel):
    aspirante_id: int
    vacante_id: int
    estado: str
    fecha_postulacion: date

class PostulacionCreate(PostulacionBase):
    pass

class PostulacionUpdate(BaseModel):
    estado: Optional[str] = None

class Postulacion(PostulacionBase):
    id: int

    class Config:
        orm_mode = True
