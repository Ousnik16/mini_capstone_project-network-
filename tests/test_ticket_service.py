from bson import ObjectId

from app.services.ticket_service import TicketService
from app.utils.constants import (
    ASSIGNMENT_STATUS_COMPLETED,
    TICKET_STATUS_ASSIGNED,
    TICKET_STATUS_OPEN,
    TICKET_STATUS_RESOLVED,
)


class FakeTicketRepository:
    def __init__(self, found_ticket=None, updated_ticket=None):
        self.found_ticket = found_ticket
        self.updated_ticket = updated_ticket
        self.created_payload = None
        self.update_call = None

    async def create(self, payload):
        self.created_payload = payload
        return {
            "id": "ticket-123",
            "user_id": str(payload["user_id"]),
            "issue_type": payload["issue_type"],
            "description": payload["description"],
            "location": payload["location"],
            "status": payload["status"],
            "created_at": payload["created_at"],
            "resolved_at": payload["resolved_at"],
        }

    async def get_by_id(self, ticket_id):
        return self.found_ticket

    async def update_status(self, ticket_id, status, resolved_at=None):
        self.update_call = {"ticket_id": ticket_id, "status": status, "resolved_at": resolved_at}
        return self.updated_ticket


class FakeAssignmentRepository:
    def __init__(self, found_assignment=None):
        self.found_assignment = found_assignment
        self.update_call = None

    async def get_by_ticket_id(self, ticket_id):
        return self.found_assignment

    async def update_status_by_ticket(self, ticket_id, status):
        self.update_call = {"ticket_id": ticket_id, "status": status}
        return self.update_call


def test_create_ticket_builds_open_ticket(run_async, payload):
    service = TicketService()
    service.ticket_repository = FakeTicketRepository()

    result = run_async(
        service.create_ticket(
            payload(issue_type="  NO_SIGNAL  ", description="Router has no lights", location="Apia"),
            str(ObjectId()),
        )
    )

    assert result["status"] == TICKET_STATUS_OPEN
    assert result["issue_type"] == "no_signal"
    assert service.ticket_repository.created_payload["description"] == "Router has no lights"


def test_create_ticket_rejects_unknown_issue_type(get_error, payload):
    service = TicketService()

    error = get_error(
        service.create_ticket(
            payload(issue_type="billing", description="Wrong charge", location="Apia"),
            str(ObjectId()),
        )
    )

    assert error.status_code == 422
    assert error.detail == "Invalid issue type"


def test_resolve_ticket_rejects_missing_ticket(get_error):
    service = TicketService()
    service.ticket_repository = FakeTicketRepository(found_ticket=None)
    service.assignment_repository = FakeAssignmentRepository()

    error = get_error(service.resolve_ticket(str(ObjectId()), str(ObjectId())))

    assert error.status_code == 404
    assert error.detail == "Ticket not found"


def test_resolve_ticket_rejects_ticket_that_is_not_assigned(get_error):
    service = TicketService()
    service.ticket_repository = FakeTicketRepository(found_ticket={"id": "ticket-1", "status": TICKET_STATUS_OPEN})
    service.assignment_repository = FakeAssignmentRepository()

    error = get_error(service.resolve_ticket(str(ObjectId()), str(ObjectId())))

    assert error.status_code == 409
    assert error.detail == "Ticket is not assigned"


def test_resolve_ticket_rejects_wrong_engineer(get_error):
    service = TicketService()
    service.ticket_repository = FakeTicketRepository(
        found_ticket={"id": "ticket-1", "status": TICKET_STATUS_ASSIGNED}
    )
    service.assignment_repository = FakeAssignmentRepository(
        found_assignment={"ticket_id": "ticket-1", "engineer_id": str(ObjectId())}
    )

    error = get_error(service.resolve_ticket(str(ObjectId()), str(ObjectId())))

    assert error.status_code == 403
    assert error.detail == "Ticket not assigned to this engineer"


def test_resolve_ticket_marks_ticket_and_assignment_complete(run_async):
    service = TicketService()
    ticket_id = str(ObjectId())
    engineer_id = str(ObjectId())
    service.ticket_repository = FakeTicketRepository(
        found_ticket={"id": ticket_id, "status": TICKET_STATUS_ASSIGNED},
        updated_ticket={"id": ticket_id, "status": TICKET_STATUS_RESOLVED},
    )
    service.assignment_repository = FakeAssignmentRepository(
        found_assignment={"ticket_id": ticket_id, "engineer_id": engineer_id}
    )

    result = run_async(service.resolve_ticket(ticket_id, engineer_id))

    assert result["status"] == TICKET_STATUS_RESOLVED
    assert service.ticket_repository.update_call["status"] == TICKET_STATUS_RESOLVED
    assert service.ticket_repository.update_call["resolved_at"] is not None
    assert service.assignment_repository.update_call == {
        "ticket_id": ticket_id,
        "status": ASSIGNMENT_STATUS_COMPLETED,
    }
