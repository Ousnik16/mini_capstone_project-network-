from types import SimpleNamespace

from app.controllers import ticket_controller


def test_create_ticket_success(client, override_customer):
    async def fake_create_ticket(payload, user_id):
        return {
            "id": "ticket-1",
            "user_id": user_id,
            "issue_type": payload.issue_type,
            "description": payload.description,
            "location": payload.location,
            "status": "open",
            "created_at": "2026-01-01T10:00:00",
        }

    original_service = ticket_controller.TicketService
    ticket_controller.TicketService = lambda: SimpleNamespace(create_ticket=fake_create_ticket)

    response = client.post(
        "/tickets",
        json={
            "issue_type": "no_signal",
            "description": "Router issue",
            "location": "Apia",
        },
    )

    ticket_controller.TicketService = original_service

    assert response.status_code == 200
    assert response.json()["status"] == "open"


def test_get_my_tickets_success(client, override_customer):
    async def fake_get_my_tickets(user_id):
        return [
            {
                "id": "ticket-1",
                "user_id": user_id,
                "issue_type": "no_signal",
                "description": "Router issue",
                "location": "Apia",
                "status": "open",
                "created_at": "2026-01-01T10:00:00",
            }
        ]

    original_service = ticket_controller.TicketService
    ticket_controller.TicketService = lambda: SimpleNamespace(get_my_tickets=fake_get_my_tickets)

    response = client.get("/tickets/my")

    ticket_controller.TicketService = original_service

    assert response.status_code == 200
    assert response.json()[0]["id"] == "ticket-1"
