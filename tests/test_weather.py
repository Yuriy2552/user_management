import pytest
from fastapi.testclient import TestClient
from user_management.main import app

def test_create_weather():
    client = TestClient(app)
    response = client.post("/weather/", json={
        "city": "Test City",
        "temperature": 25.5,
        "humidity": 60,
        "description": "Sunny"
    })
    assert response.status_code == 200
    assert response.json()["city"] == "Test City"

def test_get_weather():
    client = TestClient(app)
    # Create a weather entry first
    client.post("/weather/", json={
        "city": "Test City",
        "temperature": 25.5,
        "humidity": 60,
        "description": "Sunny"
    })
    # Fetch the weather entry
    response = client.get("/weather/Test City")
    assert response.status_code == 200
    assert response.json()["city"] == "Test City"