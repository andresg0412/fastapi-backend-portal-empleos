from pydantic import BaseModel, EmailStr
from typing import Optional

class AspiranteBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    cv_url: Optional[str] = None

class AspiranteCreate(AspiranteBase):
    pass

class AspiranteUpdate(AspiranteBase):
    pass

class Aspirante(AspiranteBase):
    id: int

    class Config:
        orm_mode = True
