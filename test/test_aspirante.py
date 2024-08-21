import sys
import os
import pytest
from httpx import AsyncClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

client = AsyncClient(app=app, base_url="http://test")

@pytest.mark.asyncio
async def test_create_aspirante():
    response = await client.post("/aspirantes/", json={
        "nombre": "Juan Pérez",
        "email": "juan.perez@example.com",
        "telefono": "+123456789",
        "cv_url": "http://example.com/cv.pdf"
    })
    assert response.status_code == 200
    assert response.json()["nombre"] == "Juan Pérez"

@pytest.mark.asyncio
async def test_get_aspirantes():
    response = await client.get("/aspirantes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_aspirante():
    # Assumes an aspirante with ID 1 exists
    response = await client.get("/aspirantes/1/")
    assert response.status_code == 200
    assert response.json()["id"] == 1

@pytest.mark.asyncio
async def test_update_aspirante():
    response = await client.put("/aspirantes/1/", json={
        "nombre": "Juan Pérez Actualizado",
        "email": "juan.perez.updated@example.com",
        "telefono": "+987654321",
        "cv_url": "http://example.com/cv_updated.pdf"
    })
    assert response.status_code == 200
    assert response.json()["nombre"] == "Juan Pérez Actualizado"

@pytest.mark.asyncio
async def test_delete_aspirante():
    response = await client.delete("/aspirantes/1/")
    assert response.status_code == 200
    assert response.json() == {"detail": "Aspirante eliminado exitosamente"}
