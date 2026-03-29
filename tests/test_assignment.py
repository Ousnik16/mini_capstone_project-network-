from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.core.dependencies import get_current_user
from app.main import app
from app.services.assignment_service import AssignmentService


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


def test_engineer_tickets_route(monkeypatch):
    async def fake_get_engineer_tickets(self, engineer_id):
        return [
            {
                "id": "ticket-10",
                "user_id": "customer-10",
                "issue_type": "no_signal",
                "description": "Tower outage",
                "location": "Area 10",
                "status": "assigned",
                "created_at": datetime.now(timezone.utc),
            }
        ]

    monkeypatch.setattr(AssignmentService, "get_engineer_tickets", fake_get_engineer_tickets)

    with _build_client(monkeypatch) as client:
        _set_user("engineer-10", "engineer")
        response = client.get("/engineer/tickets")

    assert response.status_code == 200
    assert response.json()[0]["status"] == "assigned"


def test_assign_ticket_admin_route(monkeypatch):
    async def fake_assign_ticket(self, ticket_id, engineer_id):
        return {
            "id": "assignment-11",
            "ticket_id": ticket_id,
            "engineer_id": engineer_id,
            "assigned_at": datetime.now(timezone.utc),
            "status": "assigned",
        }

    monkeypatch.setattr(AssignmentService, "assign_ticket", fake_assign_ticket)

    with _build_client(monkeypatch) as client:
        _set_user("admin-11", "admin")
        response = client.put(
            "/tickets/ticket-11/assign",
            json={"engineer_id": "engineer-11"},
        )

    assert response.status_code == 200
    assert response.json()["engineer_id"] == "engineer-11"


def test_admin_reports_route(monkeypatch):
    async def fake_get_admin_report(self):
        return {
            "total_tickets": 12,
            "open_tickets": 3,
            "assigned_tickets": 4,
            "resolved_tickets": 5,
            "avg_resolution_seconds": 3600.0,
        }

    monkeypatch.setattr(AssignmentService, "get_admin_report", fake_get_admin_report)

    with _build_client(monkeypatch) as client:
        _set_user("admin-12", "admin")
        response = client.get("/admin/reports")

    assert response.status_code == 200
    assert response.json()["total_tickets"] == 12
