from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from config.db import engine, SessionLocal
from models.postulacion import postulaciones
from schemas.postulacion import Postulacion, PostulacionCreate, PostulacionUpdate

SessionLocal = sessionmaker(bind=engine)

postulacion_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@postulacion_router.post("/postulaciones/", response_model=Postulacion)
def create_postulacion(postulacion: PostulacionCreate, db: Session = Depends(get_db)):
    new_postulacion = {
        "aspirante_id": postulacion.aspirante_id,
        "vacante_id": postulacion.vacante_id,
        "estado": postulacion.estado,
        "fecha_postulacion": postulacion.fecha_postulacion,
    }
    result = db.execute(postulaciones.insert().values(new_postulacion))
    db.commit()
    new_id = result.inserted_primary_key[0]
    query = postulaciones.select().where(postulaciones.c.id == new_id)
    created_postulacion = db.execute(query).fetchone()
    return dict(created_postulacion._mapping)



@postulacion_router.get("/postulaciones/", response_model=list[Postulacion])
def get_postulaciones(db: Session = Depends(get_db)):
    query = postulaciones.select()
    postulaciones_list = db.execute(query).fetchall()
    return [dict(postulacion._mapping) for postulacion in postulaciones_list]



@postulacion_router.get("/postulaciones/{id}", response_model=Postulacion)
def get_postulacion(id: int, db: Session = Depends(get_db)):
    query = postulaciones.select().where(postulaciones.c.id == id)
    postulacion = db.execute(query).fetchone()
    if postulacion is None:
        raise HTTPException(status_code=404, detail="Postulación no encontrada")
    return dict(postulacion._mapping)



@postulacion_router.get("/aspirantes/{aspirante_id}/postulaciones/", response_model=list[Postulacion])
def get_postulaciones_by_aspirante(aspirante_id: int, db: Session = Depends(get_db)):
    query = postulaciones.select().where(postulaciones.c.aspirante_id == aspirante_id)
    postulaciones_list = db.execute(query).fetchall()
    return [dict(postulacion._mapping) for postulacion in postulaciones_list]



@postulacion_router.get("/vacantes/{vacante_id}/postulaciones/", response_model=list[Postulacion])
def get_postulaciones_by_vacante(vacante_id: int, db: Session = Depends(get_db)):
    query = postulaciones.select().where(postulaciones.c.vacante_id == vacante_id)
    postulaciones_list = db.execute(query).fetchall()
    return [dict(postulacion._mapping) for postulacion in postulaciones_list]



@postulacion_router.put("/postulaciones/{id}", response_model=Postulacion)
def update_postulacion(id: int, postulacion_update: PostulacionUpdate, db: Session = Depends(get_db)):
    query = postulaciones.select().where(postulaciones.c.id == id)
    existing_postulacion = db.execute(query).fetchone()
    if existing_postulacion is None:
        raise HTTPException(status_code=404, detail="Postulación no encontrada")

    update_data = {
        "estado": postulacion_update.estado,
    }
    update_query = postulaciones.update().where(postulaciones.c.id == id).values(update_data)
    db.execute(update_query)
    db.commit()
    query = postulaciones.select().where(postulaciones.c.id == id)
    updated_postulacion = db.execute(query).fetchone()
    return dict(updated_postulacion._mapping)


@postulacion_router.delete("/postulaciones/{id}")
def delete_postulacion(id: int, db: Session = Depends(get_db)):
    query = postulaciones.select().where(postulaciones.c.id == id)
    postulacion = db.execute(query).fetchone()
    if postulacion is None:
        raise HTTPException(status_code=404, detail="Postulación no encontrada")

    delete_query = postulaciones.delete().where(postulaciones.c.id == id)
    db.execute(delete_query)
    db.commit()
    return {"detail": "Postulación eliminada exitosamente"}
