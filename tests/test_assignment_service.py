from types import SimpleNamespace

from app.controllers import assignment_controller


def test_get_engineer_tickets_success(client, override_engineer):
    async def fake_get_engineer_tickets(engineer_id):
        return [
            {
                "id": "ticket-1",
                "user_id": "customer-1",
                "issue_type": "no_signal",
                "description": "Router issue",
                "location": "Apia",
                "status": "assigned",
                "created_at": "2026-01-01T10:00:00",
            }
        ]

    original_service = assignment_controller.AssignmentService
    assignment_controller.AssignmentService = lambda: SimpleNamespace(get_engineer_tickets=fake_get_engineer_tickets)

    response = client.get("/engineer/tickets")

    assignment_controller.AssignmentService = original_service

    assert response.status_code == 200
    assert response.json()[0]["status"] == "assigned"
