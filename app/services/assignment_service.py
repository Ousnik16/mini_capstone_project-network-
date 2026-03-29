from datetime import datetime, timezone

from bson import ObjectId
from fastapi import HTTPException, status

from app.repositories.assignment_repository import AssignmentRepository
from app.repositories.ticket_repository import TicketRepository
from app.repositories.user_repository import UserRepository
from app.utils.constants import ASSIGNMENT_STATUS_ASSIGNED, TICKET_STATUS_ASSIGNED, TICKET_STATUS_OPEN, TICKET_STATUS_RESOLVED


class AssignmentService:
    def __init__(self):
        self.assignment_repository = AssignmentRepository()
        self.ticket_repository = TicketRepository()
        self.user_repository = UserRepository()

    async def assign_ticket(self, ticket_id: str, engineer_id: str) -> dict:
        ticket = await self.ticket_repository.get_by_id(ticket_id)
        if not ticket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
        if ticket["status"] != TICKET_STATUS_OPEN:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ticket is not open")
        if not await self.user_repository.exists_engineer(engineer_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Engineer not found")
        existing = await self.assignment_repository.get_by_ticket_id(ticket_id)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ticket already assigned")

        assignment_doc = {
            "ticket_id": ObjectId(ticket_id),
            "engineer_id": ObjectId(engineer_id),
            "assigned_at": datetime.now(timezone.utc),
            "status": ASSIGNMENT_STATUS_ASSIGNED,
        }
        assignment = await self.assignment_repository.create(assignment_doc)
        await self.ticket_repository.update_status(ticket_id, TICKET_STATUS_ASSIGNED)
        return assignment

    async def get_engineer_tickets(self, engineer_id: str) -> list[dict]:
        assignments = await self.assignment_repository.list_by_engineer(engineer_id)
        tickets: list[dict] = []
        for assignment in assignments:
            ticket = await self.ticket_repository.get_by_id(assignment["ticket_id"])
            if ticket:
                ticket["assignment_status"] = assignment["status"]
                tickets.append(ticket)
        return tickets

    async def get_admin_report(self) -> dict:
        tickets = await self.ticket_repository.list_all()
        total = len(tickets)
        open_tickets = len([t for t in tickets if t["status"] == TICKET_STATUS_OPEN])
        assigned_tickets = len([t for t in tickets if t["status"] == TICKET_STATUS_ASSIGNED])
        resolved_tickets = len([t for t in tickets if t["status"] == TICKET_STATUS_RESOLVED])
        avg_resolution_seconds = await self.assignment_repository.aggregate_resolution_avg_seconds()
        return {
            "total_tickets": total,
            "open_tickets": open_tickets,
            "assigned_tickets": assigned_tickets,
            "resolved_tickets": resolved_tickets,
            "avg_resolution_seconds": avg_resolution_seconds,
        }
