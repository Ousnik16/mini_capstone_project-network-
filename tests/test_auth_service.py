from types import SimpleNamespace

from app.controllers import auth_controller


def test_register_success(client):
    async def fake_register(payload):
        return {
            "id": "user-1",
            "name": payload.name,
            "email": payload.email,
            "role": payload.role,
            "is_active": True,
        }

    original_service = auth_controller.AuthService
    auth_controller.AuthService = lambda: SimpleNamespace(register=fake_register)

    response = client.post(
        "/auth/register",
        json={
            "name": "Jane",
            "email": "jane@example.com",
            "password": "secret123",
            "role": "customer",
        },
    )

    auth_controller.AuthService = original_service

    assert response.status_code == 200
    assert response.json()["email"] == "jane@example.com"


def test_login_success(client):
    async def fake_login(payload):
        return {"access_token": "test-token", "token_type": "bearer"}

    original_service = auth_controller.AuthService
    auth_controller.AuthService = lambda: SimpleNamespace(login=fake_login)

    response = client.post(
        "/auth/login",
        json={"email": "jane@example.com", "password": "secret123"},
    )

    auth_controller.AuthService = original_service

    assert response.status_code == 200
    assert response.json()["access_token"] == "test-token"
