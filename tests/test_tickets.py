from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.core.dependencies import get_current_user
from app.main import app
from app.services.ticket_service import TicketService


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


def test_create_ticket_route(monkeypatch):
    async def fake_create_ticket(self, payload, user_id):
        return {
            "id": "ticket-1",
            "user_id": user_id,
            "issue_type": payload.issue_type,
            "description": payload.description,
            "location": payload.location,
            "status": "open",
            "created_at": datetime.now(timezone.utc),
        }

    monkeypatch.setattr(TicketService, "create_ticket", fake_create_ticket)

    with _build_client(monkeypatch) as client:
        _set_user("customer-1", "customer")
        response = client.post(
            "/tickets",
            json={
                "issue_type": "no_signal",
                "description": "No coverage in block A",
                "location": "Block A",
            },
        )

    assert response.status_code == 200
    assert response.json()["status"] == "open"


def test_get_my_tickets_route(monkeypatch):
    async def fake_get_my_tickets(self, user_id):
        return [
            {
                "id": "ticket-2",
                "user_id": user_id,
                "issue_type": "slow_internet",
                "description": "Very slow speed",
                "location": "Zone B",
                "status": "open",
                "created_at": datetime.now(timezone.utc),
            }
        ]

    monkeypatch.setattr(TicketService, "get_my_tickets", fake_get_my_tickets)

    with _build_client(monkeypatch) as client:
        _set_user("customer-2", "customer")
        response = client.get("/tickets/my")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_all_tickets_admin_route(monkeypatch):
    async def fake_get_all_tickets(self):
        return [
            {
                "id": "ticket-3",
                "user_id": "customer-3",
                "issue_type": "no_signal",
                "description": "Signal drop",
                "location": "Zone C",
                "status": "assigned",
                "created_at": datetime.now(timezone.utc),
            }
        ]

    monkeypatch.setattr(TicketService, "get_all_tickets", fake_get_all_tickets)

    with _build_client(monkeypatch) as client:
        _set_user("admin-1", "admin")
        response = client.get("/tickets")

    assert response.status_code == 200
    assert response.json()[0]["status"] == "assigned"


def test_resolve_ticket_engineer_route(monkeypatch):
    async def fake_resolve_ticket(self, ticket_id, engineer_id):
        return {
            "id": ticket_id,
            "user_id": "customer-4",
            "issue_type": "slow_internet",
            "description": "Issue resolved",
            "location": "Zone D",
            "status": "resolved",
            "created_at": datetime.now(timezone.utc),
        }

    monkeypatch.setattr(TicketService, "resolve_ticket", fake_resolve_ticket)

    with _build_client(monkeypatch) as client:
        _set_user("engineer-1", "engineer")
        response = client.put("/tickets/ticket-4/resolve")

    assert response.status_code == 200
    assert response.json()["status"] == "resolved"
