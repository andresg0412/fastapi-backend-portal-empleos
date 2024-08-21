from sqlalchemy import Table, Column, Enum
from config.db import meta, engine
from sqlalchemy.types import Integer, String
import enum

class RolesEnum(enum.Enum):
    aspirante = "aspirante"
    empresa = "empresa"


users = Table(
    "users",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("email", String(250), unique=True),
    Column("password", String(250)),
    Column("role", String(50))
)

meta.create_all(engine)