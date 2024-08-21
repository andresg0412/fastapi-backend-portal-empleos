import sys
import os
import pytest
from httpx import AsyncClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from app.main import app

client = AsyncClient(app=app, base_url="http://test")

@pytest.mark.asyncio
async def test_create_empresa():
    response = await client.post("/empresas/", json={
        "nombre": "Tech Corp",
        "descripcion": "Empresa de tecnología",
        "ubicacion": "Ciudad X"
    })
    assert response.status_code == 200
    assert response.json()["nombre"] == "Tech Corp"

@pytest.mark.asyncio
async def test_get_empresas():
    response = await client.get("/empresas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_empresa():
    # Assumes an empresa with ID 1 exists
    response = await client.get("/empresas/1/")
    assert response.status_code == 200
    assert response.json()["id"] == 1

@pytest.mark.asyncio
async def test_update_empresa():
    response = await client.put("/empresas/1/", json={
        "nombre": "Tech Corp Updated",
        "descripcion": "Actualización de la empresa",
        "ubicacion": "Ciudad Y"
    })
    assert response.status_code == 200
    assert response.json()["nombre"] == "Tech Corp Updated"

@pytest.mark.asyncio
async def test_delete_empresa():
    response = await client.delete("/empresas/1/")
    assert response.status_code == 200
    assert response.json() == {"detail": "Empresa eliminada exitosamente"}
