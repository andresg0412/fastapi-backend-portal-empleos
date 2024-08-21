from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from routes.user import user
from routes.empresa import empresa_router
from routes.vacante import vacante_router
from routes.aspirante import aspirante_router
from routes.postulacion import postulacion_router
from pydantic import BaseModel
from typing import Optional
import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from config.db import engine, SessionLocal
from models.user import users
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, OAuthFlowPassword as OAuthFlowPasswordModel, SecuritySchemeType
from fastapi.openapi.models import OAuth2 as OAuth2Model
from fastapi.middleware.cors import CORSMiddleware


SessionLocal = sessionmaker(bind=engine)

from datetime import datetime, timedelta



app = FastAPI(
    title="My API",
    description="This is my API",
    version="1.0",
    openapi_tags=[{
        "name": "auth",
        "description": "Authentication related endpoints"
    }],
    openapi_security=[
        OAuth2Model(
            type=SecuritySchemeType.oauth2,
            flows=OAuthFlowsModel(
                password=OAuthFlowPasswordModel(
                    tokenUrl="/token",
                )
            )
        )
    ]
)

# Configuración de CORS
orig_origins = [
    "http://localhost:3000",  # URL de tu frontend en desarrollo
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=orig_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user, prefix="/api")
app.include_router(empresa_router)
app.include_router(vacante_router)
app.include_router(aspirante_router)
app.include_router(postulacion_router)
