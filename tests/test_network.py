from fastapi.testclient import TestClient

from app.core.dependencies import get_current_user
from app.main import app
from app.services.network_service import NetworkService


def _build_client(monkeypatch):
    async def fake_connect():
        return None

    async def fake_close():
        return None

    monkeypatch.setattr("app.main.connect_to_mongo", fake_connect)
    monkeypatch.setattr("app.main.close_mongo_connection", fake_close)
    app.dependency_overrides = {}
    return TestClient(app)


def _set_user(user_id: str, role: str):
    async def fake_current_user():
        return {"id": user_id, "role": role, "is_active": True}

    app.dependency_overrides[get_current_user] = fake_current_user


def test_create_network_node_route(monkeypatch):
    async def fake_create_node(self, payload):
        return {
            "id": "node-1",
            "tower_id": payload.tower_id,
            "location": payload.location,
            "status": payload.status,
        }

    monkeypatch.setattr(NetworkService, "create_node", fake_create_node)

    with _build_client(monkeypatch) as client:
        _set_user("admin-1", "admin")
        response = client.post(
            "/network",
            json={"tower_id": "TWR-100", "location": "Metro", "status": "active"},
        )

    assert response.status_code == 200
    assert response.json()["tower_id"] == "TWR-100"


def test_update_network_node_route(monkeypatch):
    async def fake_update_node_status(self, network_id, payload):
        return {
            "id": network_id,
            "tower_id": "TWR-200",
            "location": "Suburb",
            "status": payload.status,
        }

    monkeypatch.setattr(NetworkService, "update_node_status", fake_update_node_status)

    with _build_client(monkeypatch) as client:
        _set_user("admin-2", "admin")
        response = client.put("/network/node-2", json={"status": "maintenance"})

    assert response.status_code == 200
    assert response.json()["status"] == "maintenance"
