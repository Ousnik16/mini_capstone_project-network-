from app.services.network_service import NetworkService
from app.utils.constants import NETWORK_STATUS_ACTIVE, NETWORK_STATUS_DOWN


class FakeNetworkRepository:
    def __init__(self, updated_node=None, all_nodes=None, single_node=None):
        self.create_payload = None
        self.update_call = None
        self.updated_node = updated_node
        self.all_nodes = all_nodes or []
        self.single_node = single_node

    async def create(self, payload):
        self.create_payload = payload
        return {
            "id": "node-1",
            "tower_id": payload["tower_id"],
            "location": payload["location"],
            "status": payload["status"],
        }

    async def update(self, network_id, update_data):
        self.update_call = {"network_id": network_id, "update_data": update_data}
        return self.updated_node

    async def get_all(self):
        return list(self.all_nodes)

    async def get_by_id(self, network_id):
        return self.single_node


def test_create_node_cleans_input_before_saving(run_async, payload):
    service = NetworkService()
    service.network_repository = FakeNetworkRepository()

    result = run_async(
        service.create_node(payload(tower_id="  T-001  ", location="  Apia  ", status="  ACTIVE  "))
    )

    assert result["id"] == "node-1"
    assert service.network_repository.create_payload == {
        "tower_id": "T-001",
        "location": "Apia",
        "status": NETWORK_STATUS_ACTIVE,
    }


def test_create_node_rejects_invalid_status(get_error, payload):
    service = NetworkService()
    service.network_repository = FakeNetworkRepository()

    error = get_error(service.create_node(payload(tower_id="T-001", location="Apia", status="offline")))

    assert error.status_code == 422
    assert "Invalid network status" in error.detail


def test_update_node_status_requires_some_input(get_error, payload):
    service = NetworkService()
    service.network_repository = FakeNetworkRepository()

    error = get_error(service.update_node_status("node-1", payload(tower_id=None, location=None, status=None)))

    assert error.status_code == 422
    assert error.detail == "At least one field (tower_id, location, or status) is required"


def test_update_node_status_only_sends_changed_fields(run_async, payload):
    service = NetworkService()
    service.network_repository = FakeNetworkRepository(
        updated_node={"id": "node-1", "tower_id": "T-001", "location": "Savai'i", "status": NETWORK_STATUS_DOWN}
    )

    result = run_async(
        service.update_node_status("node-1", payload(tower_id=None, location="  Savai'i  ", status="  DOWN  "))
    )

    assert result["status"] == NETWORK_STATUS_DOWN
    assert service.network_repository.update_call == {
        "network_id": "node-1",
        "update_data": {"location": "Savai'i", "status": NETWORK_STATUS_DOWN},
    }


def test_update_node_status_returns_404_when_node_is_missing(get_error, payload):
    service = NetworkService()
    service.network_repository = FakeNetworkRepository(updated_node=None)

    error = get_error(
        service.update_node_status("missing-node", payload(tower_id="T-002", location=None, status=None))
    )

    assert error.status_code == 404
    assert error.detail == "Network node not found"


def test_get_all_nodes_returns_every_saved_node(run_async):
    service = NetworkService()
    service.network_repository = FakeNetworkRepository(
        all_nodes=[
            {"id": "node-1", "tower_id": "T-001", "location": "Apia", "status": NETWORK_STATUS_ACTIVE},
            {"id": "node-2", "tower_id": "T-002", "location": "Savai'i", "status": NETWORK_STATUS_DOWN},
        ]
    )

    result = run_async(service.get_all_nodes())

    assert len(result) == 2
    assert result[0]["tower_id"] == "T-001"
    assert result[1]["status"] == NETWORK_STATUS_DOWN


def test_get_node_returns_a_single_node(run_async):
    service = NetworkService()
    service.network_repository = FakeNetworkRepository(
        single_node={"id": "node-1", "tower_id": "T-001", "location": "Apia", "status": NETWORK_STATUS_ACTIVE}
    )

    result = run_async(service.get_node("node-1"))

    assert result["id"] == "node-1"
    assert result["location"] == "Apia"


def test_get_node_returns_404_for_missing_node(get_error):
    service = NetworkService()
    service.network_repository = FakeNetworkRepository(single_node=None)

    error = get_error(service.get_node("missing-node"))

    assert error.status_code == 404
    assert error.detail == "Network node not found"
