import pytest
from httpx import AsyncClient
from user_management.main import app
from user_management.dependencies import get_db

@pytest.mark.asyncio
async def test_create_weather(db_session):
    async for session in db_session:
        async def override_get_db():
            yield session
        app.dependency_overrides[get_db] = override_get_db
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/weather/", json={
                "city": "Test City",
                "temperature": 25.5,
                "humidity": 60,
                "description": "Sunny"
            })
        assert response.status_code == 200
        assert response.json()["city"] == "Test City"
        break

@pytest.mark.asyncio
async def test_get_weather(db_session):
    async for session in db_session:
        async def override_get_db():
            yield session
        app.dependency_overrides[get_db] = override_get_db
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
        break