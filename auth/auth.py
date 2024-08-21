from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from models.user import users
from config.db import engine, SessionLocal
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Contexto de hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración de JWT
SECRET_KEY = "clave_secreta_prueba"
ALGORITHM = "HS256"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        print(email, role)
        if email is None or role is None:
            raise credentials_exception
        user = db.execute(users.select().where(users.c.email == email)).fetchone()
        if user is None:
            raise credentials_exception
        return {"email": email, "role": role}
    except jwt.PyJWTError:
        raise credentials_exception

def get_current_active_user(current_user: dict = Depends(get_current_user)):
    return current_user

def get_current_active_aspirante(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "aspirante":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

def get_current_active_empresa(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "empresa":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user
