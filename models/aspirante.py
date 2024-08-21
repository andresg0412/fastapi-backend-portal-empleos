from sqlalchemy import Table, Column, Integer, String, Text
from config.db import meta, engine

aspirantes = Table(
    "aspirantes",
    meta,
    Column("id", Integer, primary_key=True),
    Column("nombre", String(100), nullable=False),
    Column("email", String(100), nullable=False),
    Column("telefono", String(20), nullable=True),
    Column("cv_url", String(200), nullable=True),
)

meta.create_all(engine)
