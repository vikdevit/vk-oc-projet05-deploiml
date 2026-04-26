from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_login_success():
    response = client.post("/auth/login", json={
        "username": "admin",
        "password": "Test123!"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_username():
    response = client.post("/auth/login", json={
        "username": "wrong",
        "password": "Test123!"
    })
    assert response.status_code == 401


def test_login_wrong_password():
    response = client.post("/auth/login", json={
        "username": "admin",
        "password": "wrong"
    })
    assert response.status_code == 401
