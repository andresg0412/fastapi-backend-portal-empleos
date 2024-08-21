from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.db import meta, engine

postulaciones = Table(
    "postulaciones",
    meta,
    Column("id", Integer, primary_key=True),
    Column("aspirante_id", Integer, ForeignKey("aspirantes.id"), nullable=False),
    Column("vacante_id", Integer, ForeignKey("vacantes.id"), nullable=False),
    Column("estado", String(20), nullable=False),
    Column("fecha_postulacion", Date, nullable=False),
)

meta.create_all(engine)
