import sys
import os
import pytest
from httpx import AsyncClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

client = AsyncClient(app=app, base_url="http://test")

@pytest.mark.asyncio
async def test_create_postulacion():
    response = await client.post("/postulaciones/", json={
        "aspirante_id": 1,
        "vacante_id": 1,
        "estado": "Pendiente",
        "fecha_postulacion": "2024-08-09"
    })
    assert response.status_code == 200
    assert response.json()["estado"] == "Pendiente"

@pytest.mark.asyncio
async def test_get_postulaciones():
    response = await client.get("/postulaciones/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_postulacion():
    # Assumes a postulacion with ID 1 exists
    response = await client.get("/postulaciones/1/")
    assert response.status_code == 200
    assert response.json()["id"] == 1

@pytest.mark.asyncio
async def test_update_postulacion():
    response = await client.put("/postulaciones/1/", json={
        "estado": "Aceptada"
    })
    assert response.status_code == 200
    assert response.json()["estado"] == "Aceptada"

@pytest.mark.asyncio
async def test_delete_postulacion():
    response = await client.delete("/postulaciones/1/")
    assert response.status_code == 200
    assert response.json() == {"detail": "Postulación eliminada exitosamente"}
