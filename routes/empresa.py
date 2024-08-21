
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from config.db import engine, SessionLocal
from models.empresa import empresas
from schemas.empresa import Empresa, EmpresaCreate, EmpresaUpdate

SessionLocal = sessionmaker(bind=engine)
empresa_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@empresa_router.post("/empresas/", response_model=Empresa)
def create_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    new_empresa = {
        "nombre": empresa.nombre,
        "descripcion": empresa.descripcion,
        "ubicacion": empresa.ubicacion
    }
    result = db.execute(empresas.insert().values(new_empresa))
    db.commit()
    new_id = result.inserted_primary_key[0]
    query = empresas.select().where(empresas.c.id == new_id)
    created_empresa = db.execute(query).fetchone()
    return dict(created_empresa._mapping)

@empresa_router.get("/empresas/", response_model=list[Empresa])
def get_empresas(db: Session = Depends(get_db)):
    query = empresas.select()
    empresas_list = db.execute(query).fetchall()
    return [dict(empresa._mapping) for empresa in empresas_list]

@empresa_router.get("/empresas/{id}", response_model=Empresa)
def get_empresa(id: int, db: Session = Depends(get_db)):
    query = empresas.select().where(empresas.c.id == id)
    empresa = db.execute(query).fetchone()
    if empresa is None:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return dict(empresa._mapping)

@empresa_router.put("/empresas/{id}", response_model=Empresa)
def update_empresa(id: int, empresa_update: EmpresaUpdate, db: Session = Depends(get_db)):
    query = empresas.select().where(empresas.c.id == id)
    existing_empresa = db.execute(query).fetchone()
    if existing_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    updated_empresa = {
        "nombre": empresa_update.nombre,
        "descripcion": empresa_update.descripcion,
        "ubicacion": empresa_update.ubicacion
    }
    update_query = empresas.update().where(empresas.c.id == id).values(updated_empresa)
    db.execute(update_query)
    db.commit()
    query = empresas.select().where(empresas.c.id == id)
    updated_empresa = db.execute(query).fetchone()
    return dict(updated_empresa._mapping)

@empresa_router.delete("/empresas/{id}")
def delete_empresa(id: int, db: Session = Depends(get_db)):
    query = empresas.select().where(empresas.c.id == id)
    empresa = db.execute(query).fetchone()
    if empresa is None:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    delete_query = empresas.delete().where(empresas.c.id == id)
    db.execute(delete_query)
    db.commit()
    return {"detail": "Empresa eliminada exitosamente"}
