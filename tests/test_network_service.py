from types import SimpleNamespace

from app.controllers import network_controller


def test_create_network_node_success(client, override_admin):
    async def fake_create_node(payload):
        return {
            "id": "node-1",
            "tower_id": payload.tower_id,
            "location": payload.location,
            "status": payload.status,
        }

    original_service = network_controller.NetworkService
    network_controller.NetworkService = lambda: SimpleNamespace(create_node=fake_create_node)

    response = client.post(
        "/network",
        json={"tower_id": "T-001", "location": "Apia", "status": "active"},
    )

    network_controller.NetworkService = original_service

    assert response.status_code == 200
    assert response.json()["tower_id"] == "T-001"


def test_get_network_node_success(client, override_admin):
    async def fake_get_node(network_id):
        return {
            "id": network_id,
            "tower_id": "T-001",
            "location": "Apia",
            "status": "active",
        }

    original_service = network_controller.NetworkService
    network_controller.NetworkService = lambda: SimpleNamespace(get_node=fake_get_node)

    response = client.get("/network/node-1")

    network_controller.NetworkService = original_service

    assert response.status_code == 200
    assert response.json()["id"] == "node-1"
