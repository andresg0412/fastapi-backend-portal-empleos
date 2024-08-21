import sys
import os
import pytest
from httpx import AsyncClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app



client = AsyncClient(app=app, base_url="http://test")

@pytest.mark.asyncio
async def test_create_vacante():
    response = await client.post("/vacantes/", json={
        "titulo": "Desarrollador Backend",
        "subtitulo": "Python",
        "modo": "Remoto",
        "salario": "3000-4000 USD",
        "fecha": "2024-08-09",
        "descripcion": "Desarrollador Backend con experiencia en Python",
        "estado": "Activo",
        "empresa_id": 1
    })
    assert response.status_code == 200
    assert response.json()["titulo"] == "Desarrollador Backend"

@pytest.mark.asyncio
async def test_get_vacantes():
    response = await client.get("/vacantes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_vacante():
    # Assumes a vacante with ID 1 exists
    response = await client.get("/vacantes/1/")
    assert response.status_code == 200
    assert response.json()["id"] == 1

@pytest.mark.asyncio
async def test_update_vacante():
    response = await client.put("/vacantes/1/", json={
        "titulo": "Desarrollador Full Stack",
        "subtitulo": "React, Node",
        "modo": "Híbrido",
        "salario": "3500-4500 USD",
        "fecha": "2024-08-09",
        "descripcion": "Desarrollador Full Stack con experiencia en React y Node",
        "estado": "Activo",
        "empresa_id": 1
    })
    assert response.status_code == 200
    assert response.json()["titulo"] == "Desarrollador Full Stack"

@pytest.mark.asyncio
async def test_delete_vacante():
    response = await client.delete("/vacantes/1/")
    assert response.status_code == 200
    assert response.json() == {"detail": "Vacante eliminada exitosamente"}
