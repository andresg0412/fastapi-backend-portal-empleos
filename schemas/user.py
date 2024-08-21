from typing import List, Optional
from pydantic import BaseModel
import enum

class User(BaseModel):
    email: str
    password: str

class UserCreate(User):
    name: str
    email: str
    password: str
    role: str


class UserInDB(User):
    id: Optional[int] = None
    hashed_password: str