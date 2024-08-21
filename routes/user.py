from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import conn
from models.user import users
from schemas.user import User, UserCreate, UserInDB
from sqlalchemy.orm import sessionmaker
from config.db import engine, SessionLocal
from fastapi import HTTPException
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from typing import Union
import jwt
from datetime import datetime, timedelta


SessionLocal = sessionmaker(bind=engine)
#from cryptography.fernet import Fernet

#key = Fernet.generate_key()
#f = Fernet(key)

user = APIRouter()

# Contexto de hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración de JWT
SECRET_KEY = "clave_secreta_prueba"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_jwt_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        
        if user is None or role is None:
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

@user.post("/token")
def login(user: User, db: Session = Depends(get_db)):
    try:
        db_user = db.execute(users.select().where(users.c.email == user.email)).fetchone()

        # Verifica si se encontró el usuario
        if db_user is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")        


        print(db_user._mapping)
        # Accede a los datos de la tupla usando índices
        db_user_email = db_user[2]  # Cambia el índice según la posición de 'email' en la tupla
        db_user_password = db_user[3]
        db_user_role = db_user[4]  # Cambia el índice según la posición de 'password' en la tupla

        if not verify_password(user.password, db_user_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = create_jwt_token({"sub": db_user_email, "role": db_user_role})
        print(db_user_email, db_user_password, db_user_role)
        return {"access_token": access_token, "token_type": "bearer", "role": db_user_role, "email": db_user_email}


    except Exception as e:
        print(f"Error: {e}")

    #db_user = db.execute(users.select().where(users.c.email == user.email)).fetchone()
    #if db_user is None or not verify_password(user.password, db_user["password"]):
    #    raise HTTPException(status_code=401, detail="Invalid credentials")
    #access_token = create_jwt_token({"sub": db_user["email"]})
    #return {"access_token": access_token, "token_type": "bearer"}



@user.get("/users")
def get_users(db: Session = Depends(get_db)):
    result = db.execute(users.select()).fetchall()
    return [dict(row._mapping) for row in result]

@user.post("/users")
def create_user(user: User, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    new_user = {"name": user.name, "email": user.email, "password": hashed_password, "role": user.role}
    #new_user["password"] = f.encrypt(user.password.encode("utf-8"))
    
    result = db.execute(users.insert().values(new_user))
    db.commit()

    created_user = db.execute(users.select().where(users.c.id == result.lastrowid)).first()
    if not created_user:
        raise HTTPException(status_code=404, detail="User not found after creation")
    
    return dict(created_user._mapping)


# Obtener un usuario específico por ID
@user.get("/users/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    query = users.select().where(users.c.id == id)
    user = db.execute(query).fetchone()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return dict(user._mapping)

@user.put("/users/{id}")
def update_user(id: int, user_update: UserCreate, db: Session = Depends(get_db)):
    query = users.select().where(users.c.id == id)
    existing_user = db.execute(query).fetchone()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    updated_user = {
        "name": user_update.name,
        "email": user_update.email,
        "password": hash_password(user_update.password),
        "role": user_update.role
    }
    update_query = users.update().where(users.c.id == id).values(updated_user)
    db.execute(update_query)
    db.commit()
    return dict({**existing_user._mapping, **updated_user})

@user.delete("/users/{id}")
def delete_user(id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    query = users.select().where(users.c.id == id)
    user = db.execute(query).fetchone()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    delete_query = users.delete().where(users.c.id == id)
    db.execute(delete_query)
    db.commit()
    return {"detail": "Usuario eliminado exitosamente"}