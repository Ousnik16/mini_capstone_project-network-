from bson import ObjectId

from app.services.assignment_service import AssignmentService
from app.utils.constants import (
    ASSIGNMENT_STATUS_ASSIGNED,
    TICKET_STATUS_ASSIGNED,
    TICKET_STATUS_OPEN,
    TICKET_STATUS_RESOLVED,
)


class FakeAssignmentRepository:
    def __init__(self, existing_assignment=None, engineer_assignments=None, average_seconds=0.0):
        self.existing_assignment = existing_assignment
        self.engineer_assignments = engineer_assignments or []
        self.average_seconds = average_seconds
        self.created_payload = None

    async def get_by_ticket_id(self, ticket_id):
        return self.existing_assignment

    async def create(self, payload):
        self.created_payload = payload
        return {
            "id": "assignment-123",
            "ticket_id": str(payload["ticket_id"]),
            "engineer_id": str(payload["engineer_id"]),
            "assigned_at": payload["assigned_at"],
            "status": payload["status"],
        }

    async def list_by_engineer(self, engineer_id):
        return list(self.engineer_assignments)

    async def aggregate_resolution_avg_seconds(self):
        return self.average_seconds


class FakeTicketRepository:
    def __init__(self, found_ticket=None, all_tickets=None):
        self.found_ticket = found_ticket
        self.all_tickets = all_tickets or []
        self.update_call = None

    async def get_by_id(self, ticket_id):
        return self.found_ticket

    async def update_status(self, ticket_id, status, resolved_at=None):
        self.update_call = {"ticket_id": ticket_id, "status": status, "resolved_at": resolved_at}
        return {"id": ticket_id, "status": status}

    async def list_all(self):
        return list(self.all_tickets)


class FakeUserRepository:
    def __init__(self, engineer_exists=True):
        self.engineer_exists = engineer_exists

    async def exists_engineer(self, engineer_id):
        return self.engineer_exists


def test_assign_ticket_creates_assignment(run_async):
    service = AssignmentService()
    ticket_id = str(ObjectId())
    engineer_id = str(ObjectId())
    service.ticket_repository = FakeTicketRepository(found_ticket={"id": ticket_id, "status": TICKET_STATUS_OPEN})
    service.assignment_repository = FakeAssignmentRepository()
    service.user_repository = FakeUserRepository(engineer_exists=True)

    result = run_async(service.assign_ticket(ticket_id, engineer_id))

    assert result["status"] == ASSIGNMENT_STATUS_ASSIGNED
    assert result["ticket_id"] == ticket_id
    assert result["engineer_id"] == engineer_id
    assert service.ticket_repository.update_call == {
        "ticket_id": ticket_id,
        "status": TICKET_STATUS_ASSIGNED,
        "resolved_at": None,
    }


def test_assign_ticket_rejects_missing_ticket(get_error):
    service = AssignmentService()
    service.ticket_repository = FakeTicketRepository(found_ticket=None)
    service.assignment_repository = FakeAssignmentRepository()
    service.user_repository = FakeUserRepository()

    error = get_error(service.assign_ticket(str(ObjectId()), str(ObjectId())))

    assert error.status_code == 404
    assert error.detail == "Ticket not found"


def test_assign_ticket_rejects_ticket_that_is_not_open(get_error):
    service = AssignmentService()
    service.ticket_repository = FakeTicketRepository(
        found_ticket={"id": str(ObjectId()), "status": TICKET_STATUS_ASSIGNED}
    )
    service.assignment_repository = FakeAssignmentRepository()
    service.user_repository = FakeUserRepository()

    error = get_error(service.assign_ticket(str(ObjectId()), str(ObjectId())))

    assert error.status_code == 409
    assert error.detail == "Ticket is not open"


def test_assign_ticket_rejects_missing_engineer(get_error):
    service = AssignmentService()
    service.ticket_repository = FakeTicketRepository(
        found_ticket={"id": str(ObjectId()), "status": TICKET_STATUS_OPEN}
    )
    service.assignment_repository = FakeAssignmentRepository()
    service.user_repository = FakeUserRepository(engineer_exists=False)

    error = get_error(service.assign_ticket(str(ObjectId()), str(ObjectId())))

    assert error.status_code == 404
    assert error.detail == "Engineer not found"


def test_assign_ticket_rejects_duplicate_assignment(get_error):
    service = AssignmentService()
    service.ticket_repository = FakeTicketRepository(
        found_ticket={"id": str(ObjectId()), "status": TICKET_STATUS_OPEN}
    )
    service.assignment_repository = FakeAssignmentRepository(existing_assignment={"id": "assignment-1"})
    service.user_repository = FakeUserRepository(engineer_exists=True)

    error = get_error(service.assign_ticket(str(ObjectId()), str(ObjectId())))

    assert error.status_code == 409
    assert error.detail == "Ticket already assigned"


def test_get_engineer_tickets_returns_ticket_details(run_async):
    service = AssignmentService()
    service.assignment_repository = FakeAssignmentRepository(
        engineer_assignments=[
            {"ticket_id": "ticket-1", "status": ASSIGNMENT_STATUS_ASSIGNED},
            {"ticket_id": "ticket-2", "status": ASSIGNMENT_STATUS_ASSIGNED},
        ]
    )

    class EngineerTicketRepository:
        async def get_by_id(self, ticket_id):
            if ticket_id == "ticket-1":
                return {"id": "ticket-1", "status": TICKET_STATUS_ASSIGNED, "description": "Router issue"}
            return None

    service.ticket_repository = EngineerTicketRepository()

    result = run_async(service.get_engineer_tickets("engineer-1"))

    assert result == [
        {
            "id": "ticket-1",
            "status": TICKET_STATUS_ASSIGNED,
            "description": "Router issue",
            "assignment_status": ASSIGNMENT_STATUS_ASSIGNED,
        }
    ]


def test_get_admin_report_counts_tickets_by_status(run_async):
    service = AssignmentService()
    service.ticket_repository = FakeTicketRepository(
        all_tickets=[
            {"id": "1", "status": TICKET_STATUS_OPEN},
            {"id": "2", "status": TICKET_STATUS_ASSIGNED},
            {"id": "3", "status": TICKET_STATUS_RESOLVED},
            {"id": "4", "status": TICKET_STATUS_RESOLVED},
        ]
    )
    service.assignment_repository = FakeAssignmentRepository(average_seconds=123.5)

    result = run_async(service.get_admin_report())

    assert result == {
        "total_tickets": 4,
        "open_tickets": 1,
        "assigned_tickets": 1,
        "resolved_tickets": 2,
        "avg_resolution_seconds": 123.5,
    }
