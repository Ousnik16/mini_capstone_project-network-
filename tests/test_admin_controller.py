from types import SimpleNamespace

from app.controllers import admin_controller


def test_assign_ticket_success(client, override_admin):
    async def fake_assign_ticket(ticket_id, engineer_id):
        return {
            "id": "assignment-1",
            "ticket_id": ticket_id,
            "engineer_id": engineer_id,
            "assigned_at": "2026-01-01T10:00:00",
            "status": "assigned",
        }

    original_service = admin_controller.AssignmentService
    admin_controller.AssignmentService = lambda: SimpleNamespace(assign_ticket=fake_assign_ticket)

    response = client.put("/tickets/ticket-1/assign", json={"engineer_id": "engineer-1"})

    admin_controller.AssignmentService = original_service

    assert response.status_code == 200
    assert response.json()["status"] == "assigned"


def test_admin_report_success(client, override_admin):
    async def fake_get_admin_report():
        return {
            "total_tickets": 5,
            "open_tickets": 2,
            "assigned_tickets": 1,
            "resolved_tickets": 2,
            "avg_resolution_seconds": 100.0,
        }

    original_service = admin_controller.AssignmentService
    admin_controller.AssignmentService = lambda: SimpleNamespace(get_admin_report=fake_get_admin_report)

    response = client.get("/admin/reports")

    admin_controller.AssignmentService = original_service

    assert response.status_code == 200
    assert response.json()["total_tickets"] == 5
