from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from config.db import engine, SessionLocal
from models.aspirante import aspirantes
from schemas.aspirante import Aspirante, AspiranteCreate, AspiranteUpdate

SessionLocal = sessionmaker(bind=engine)

aspirante_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@aspirante_router.post("/aspirantes/", response_model=Aspirante)
def create_aspirante(aspirante: AspiranteCreate, db: Session = Depends(get_db)):
    new_aspirante = {
        "nombre": aspirante.nombre,
        "email": aspirante.email,
        "telefono": aspirante.telefono,
        "cv_url": aspirante.cv_url
    }
    result = db.execute(aspirantes.insert().values(new_aspirante))
    db.commit()
    new_id = result.inserted_primary_key[0]
    query = aspirantes.select().where(aspirantes.c.id == new_id)
    created_aspirante = db.execute(query).fetchone()
    return dict(created_aspirante._mapping)


@aspirante_router.get("/aspirantes/", response_model=list[Aspirante])
def get_aspirantes(db: Session = Depends(get_db)):
    query = aspirantes.select()
    aspirantes_list = db.execute(query).fetchall()
    return [dict(aspirante._mapping) for aspirante in aspirantes_list]


@aspirante_router.get("/aspirantes/{id}", response_model=Aspirante)
def get_aspirante(id: int, db: Session = Depends(get_db)):
    query = aspirantes.select().where(aspirantes.c.id == id)
    aspirante = db.execute(query).fetchone()
    if aspirante is None:
        raise HTTPException(status_code=404, detail="Aspirante no encontrado")
    return dict(aspirante._mapping)


@aspirante_router.put("/aspirantes/{id}", response_model=Aspirante)
def update_aspirante(id: int, aspirante_update: AspiranteUpdate, db: Session = Depends(get_db)):
    query = aspirantes.select().where(aspirantes.c.id == id)
    existing_aspirante = db.execute(query).fetchone()
    if existing_aspirante is None:
        raise HTTPException(status_code=404, detail="Aspirante no encontrado")

    updated_aspirante = {
        "nombre": aspirante_update.nombre,
        "email": aspirante_update.email,
        "telefono": aspirante_update.telefono,
        "cv_url": aspirante_update.cv_url
    }
    update_query = aspirantes.update().where(aspirantes.c.id == id).values(updated_aspirante)
    db.execute(update_query)
    db.commit()
    query = aspirantes.select().where(aspirantes.c.id == id)
    updated_aspirante = db.execute(query).fetchone()
    return dict(updated_aspirante._mapping)


@aspirante_router.delete("/aspirantes/{id}")
def delete_aspirante(id: int, db: Session = Depends(get_db)):
    query = aspirantes.select().where(aspirantes.c.id == id)
    aspirante = db.execute(query).fetchone()
    if aspirante is None:
        raise HTTPException(status_code=404, detail="Aspirante no encontrado")

    delete_query = aspirantes.delete().where(aspirantes.c.id == id)
    db.execute(delete_query)
    db.commit()
    return {"detail": "Aspirante eliminado exitosamente"}
