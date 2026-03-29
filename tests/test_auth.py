from fastapi.testclient import TestClient

from app.main import app
from app.services.auth_service import AuthService


def _build_client(monkeypatch):
    async def fake_connect():
        return None

    async def fake_close():
        return None

    monkeypatch.setattr("app.main.connect_to_mongo", fake_connect)
    monkeypatch.setattr("app.main.close_mongo_connection", fake_close)
    app.dependency_overrides = {}
    return TestClient(app)


def test_register_route(monkeypatch):
    async def fake_register(self, payload):
        return {
            "id": "user-1",
            "name": payload.name,
            "email": payload.email,
            "role": payload.role,
            "is_active": True,
        }

    monkeypatch.setattr(AuthService, "register", fake_register)

    with _build_client(monkeypatch) as client:
        response = client.post(
            "/auth/register",
            json={
                "name": "Admin",
                "email": "admin@telecom.com",
                "password": "Admin@123",
                "role": "admin",
            },
        )

    assert response.status_code == 200
    assert response.json()["role"] == "admin"


def test_login_route_json(monkeypatch):
    async def fake_login(self, payload):
        assert payload.email == "admin@telecom.com"
        assert payload.password == "Admin@123"
        return {"access_token": "token-json", "token_type": "bearer"}

    monkeypatch.setattr(AuthService, "login", fake_login)

    with _build_client(monkeypatch) as client:
        response = client.post(
            "/auth/login",
            json={"email": "admin@telecom.com", "password": "Admin@123"},
        )

    assert response.status_code == 200
    assert response.json()["access_token"] == "token-json"


def test_login_route_form(monkeypatch):
    async def fake_login(self, payload):
        assert payload.email == "engineer@telecom.com"
        assert payload.password == "Engineer@123"
        return {"access_token": "token-form", "token_type": "bearer"}

    monkeypatch.setattr(AuthService, "login", fake_login)

    with _build_client(monkeypatch) as client:
        response = client.post(
            "/auth/login",
            data={"username": "engineer@telecom.com", "password": "Engineer@123"},
        )

    assert response.status_code == 200
    assert response.json()["access_token"] == "token-form"
