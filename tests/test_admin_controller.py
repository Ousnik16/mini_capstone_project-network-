from datetime import datetime

from fastapi import HTTPException

from app.controllers import admin_controller


def test_assign_ticket_endpoint_calls_service(run_async, payload, monkeypatch):
    class FakeAssignmentService:
        async def assign_ticket(self, ticket_id, engineer_id):
            return {
                "id": "assignment-1",
                "ticket_id": ticket_id,
                "engineer_id": engineer_id,
                "assigned_at": datetime(2026, 1, 1),
                "status": "assigned",
            }

    monkeypatch.setattr(admin_controller, "AssignmentService", lambda: FakeAssignmentService())

    result = run_async(
        admin_controller.assign_ticket(
            "ticket-123",
            payload(engineer_id="engineer-456"),
            {"role": "admin"},
        )
    )

    assert result["ticket_id"] == "ticket-123"
    assert result["engineer_id"] == "engineer-456"
    assert result["status"] == "assigned"


def test_admin_reports_endpoint_returns_report(run_async, monkeypatch):
    class FakeAssignmentService:
        async def get_admin_report(self):
            return {
                "total_tickets": 10,
                "open_tickets": 3,
                "assigned_tickets": 4,
                "resolved_tickets": 3,
                "avg_resolution_seconds": 120.5,
            }

    monkeypatch.setattr(admin_controller, "AssignmentService", lambda: FakeAssignmentService())

    result = run_async(admin_controller.admin_reports({"role": "admin"}))

    assert result["total_tickets"] == 10
    assert result["open_tickets"] == 3
    assert result["assigned_tickets"] == 4
    assert result["resolved_tickets"] == 3
    assert result["avg_resolution_seconds"] == 120.5


def test_assign_ticket_endpoint_passes_through_service_errors(get_error, payload, monkeypatch):
    class FakeAssignmentService:
        async def assign_ticket(self, ticket_id, engineer_id):
            raise HTTPException(status_code=404, detail="Ticket not found")

    monkeypatch.setattr(admin_controller, "AssignmentService", lambda: FakeAssignmentService())

    error = get_error(
        admin_controller.assign_ticket(
            "missing-ticket",
            payload(engineer_id="engineer-456"),
            {"role": "admin"},
        )
    )

    assert error.status_code == 404
    assert error.detail == "Ticket not found"
