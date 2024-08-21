from sqlalchemy import Table, Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.db import meta, engine

vacantes = Table(
    "vacantes",
    meta,
    Column("id", Integer, primary_key=True),
    Column("titulo", String(100), nullable=False),
    Column("subtitulo", String(100), nullable=True),
    Column("modo", String(50), nullable=False),
    Column("salario", String(50), nullable=True),
    Column("fecha", Date, nullable=False),
    Column("descripcion", Text, nullable=True),
    Column("estado", String(50), default="Activo"),
    Column("empresa_id", Integer, ForeignKey("empresas.id"), nullable=False),
)

meta.create_all(engine)
