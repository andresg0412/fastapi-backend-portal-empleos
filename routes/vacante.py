from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from config.db import engine, SessionLocal
from models.vacante import vacantes
from schemas.vacante import Vacante, VacanteCreate, VacanteUpdate
from auth.auth import get_current_user, get_current_active_user, get_current_active_aspirante, get_current_active_empresa
SessionLocal = sessionmaker(bind=engine)

vacante_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#CREAR VACANTES

@vacante_router.post("/vacantes/", response_model=Vacante)
def create_vacante(vacante: VacanteCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_active_empresa)):
    new_vacante = {
        "titulo": vacante.titulo,
        "subtitulo": vacante.subtitulo,
        "modo": vacante.modo,
        "salario": vacante.salario,
        "fecha": vacante.fecha,
        "descripcion": vacante.descripcion,
        "estado": vacante.estado,
        "empresa_id": vacante.empresa_id
    }
    result = db.execute(vacantes.insert().values(new_vacante))
    db.commit()
    new_id = result.inserted_primary_key[0]
    query = vacantes.select().where(vacantes.c.id == new_id)
    created_vacante = db.execute(query).fetchone()
    return dict(created_vacante._mapping)


#OBTENER VACANTES

@vacante_router.get("/vacantes/", response_model=list[Vacante])
def get_vacantes(db: Session = Depends(get_db)):
    query = vacantes.select()
    vacantes_list = db.execute(query).fetchall()
    return [dict(vacante._mapping) for vacante in vacantes_list]


#OBTENER VACANTE POR ID

@vacante_router.get("/vacantes/{id}", response_model=Vacante)
def get_vacante(id: int, db: Session = Depends(get_db)):
    query = vacantes.select().where(vacantes.c.id == id)
    vacante = db.execute(query).fetchone()
    if vacante is None:
        raise HTTPException(status_code=404, detail="Vacante no encontrada")
    return dict(vacante._mapping)


#VACANTES POR EMPRESA
@vacante_router.get("/empresas/{empresa_id}/vacantes/", response_model=list[Vacante])
def get_vacantes_by_empresa(empresa_id: int, db: Session = Depends(get_db)):
    query = vacantes.select().where(vacantes.c.empresa_id == empresa_id)
    vacantes_list = db.execute(query).fetchall()
    return [dict(vacante._mapping) for vacante in vacantes_list]


#ACTUALIZAR VACANTE

@vacante_router.put("/vacantes/{id}", response_model=Vacante)
def update_vacante(id: int, vacante_update: VacanteUpdate, db: Session = Depends(get_db)):
    query = vacantes.select().where(vacantes.c.id == id)
    existing_vacante = db.execute(query).fetchone()
    if existing_vacante is None:
        raise HTTPException(status_code=404, detail="Vacante no encontrada")

    updated_vacante = {
        "titulo": vacante_update.titulo,
        "subtitulo": vacante_update.subtitulo,
        "modo": vacante_update.modo,
        "salario": vacante_update.salario,
        "fecha": vacante_update.fecha,
        "descripcion": vacante_update.descripcion,
        "estado": vacante_update.estado,
        "empresa_id": vacante_update.empresa_id
    }
    update_query = vacantes.update().where(vacantes.c.id == id).values(updated_vacante)
    db.execute(update_query)
    db.commit()
    query = vacantes.select().where(vacantes.c.id == id)
    updated_vacante = db.execute(query).fetchone()
    return dict(updated_vacante._mapping)


#ELIMINAR UNA VACANTE POR ID

@vacante_router.delete("/vacantes/{id}")
def delete_vacante(id: int, db: Session = Depends(get_db)):
    query = vacantes.select().where(vacantes.c.id == id)
    vacante = db.execute(query).fetchone()
    if vacante is None:
        raise HTTPException(status_code=404, detail="Vacante no encontrada")

    delete_query = vacantes.delete().where(vacantes.c.id == id)
    db.execute(delete_query)
    db.commit()
    return {"detail": "Vacante eliminada exitosamente"}


#FINALIZAR VACANTE

@vacante_router.put("/vacantes/{id}/finalizar/")
def finalizar_vacante(id: int, db: Session = Depends(get_db)):
    query = vacantes.select().where(vacantes.c.id == id)
    vacante = db.execute(query).fetchone()
    if vacante is None:
        raise HTTPException(status_code=404, detail="Vacante no encontrada")

    update_query = vacantes.update().where(vacantes.c.id == id).values(estado="Finalizada")
    db.execute(update_query)
    db.commit()
    return {"detail": "Vacante marcada como finalizada"}
