from sqlalchemy import Table, Column, Integer, String, Text
from config.db import meta, engine

empresas = Table(
    "empresas",
    meta,
    Column("id", Integer, primary_key=True),
    Column("nombre", String(100), nullable=False),
    Column("descripcion", Text, nullable=True),
    Column("ubicacion", String(255), nullable=True)
)

meta.create_all(engine)
