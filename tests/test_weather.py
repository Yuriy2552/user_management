import pytest
from httpx import AsyncClient
from user_management.main import app

@pytest.mark.asyncio
async def test_create_weather():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/weather/", json={
            "city": "Test City",
            "temperature": 25.5,
            "humidity": 60,
            "description": "Sunny"
        })
    assert response.status_code == 200
    assert response.json()["city"] == "Test City"

@pytest.mark.asyncio
async def test_get_weather():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/weather/", json={
            "city": "Test City",
            "temperature": 25.5,
            "humidity": 60,
            "description": "Sunny"
        })
        response = await ac.get("/weather/Test City")
    assert response.status_code == 200
    assert response.json()["city"] == "Test City"