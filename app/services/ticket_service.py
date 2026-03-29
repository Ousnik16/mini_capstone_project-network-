from datetime import datetime, timezone

from bson import ObjectId
from fastapi import HTTPException, status

from app.repositories.assignment_repository import AssignmentRepository
from app.repositories.ticket_repository import TicketRepository
from app.schemas.ticket_schema import TicketCreateRequest
from app.utils.constants import (
    ASSIGNMENT_STATUS_COMPLETED,
    ISSUE_TYPE_NO_SIGNAL,
    ISSUE_TYPE_SLOW_INTERNET,
    TICKET_STATUS_ASSIGNED,
    TICKET_STATUS_OPEN,
    TICKET_STATUS_RESOLVED,
)


class TicketService:
    def __init__(self):
        self.ticket_repository = TicketRepository()
        self.assignment_repository = AssignmentRepository()

    async def create_ticket(self, payload: TicketCreateRequest, user_id: str) -> dict:
        issue_type = payload.issue_type.strip().lower()
        if issue_type not in {ISSUE_TYPE_NO_SIGNAL, ISSUE_TYPE_SLOW_INTERNET}:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid issue type")

        ticket_doc = {
            "user_id": ObjectId(user_id),
            "issue_type": issue_type,
            "description": payload.description,
            "location": payload.location,
            "status": TICKET_STATUS_OPEN,
            "created_at": datetime.now(timezone.utc),
            "resolved_at": None,
        }
        return await self.ticket_repository.create(ticket_doc)

    async def get_my_tickets(self, user_id: str) -> list[dict]:
        return await self.ticket_repository.list_by_user(user_id)

    async def get_all_tickets(self) -> list[dict]:
        return await self.ticket_repository.list_all()

    async def resolve_ticket(self, ticket_id: str, engineer_id: str) -> dict:
        ticket = await self.ticket_repository.get_by_id(ticket_id)
        if not ticket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
        if ticket["status"] != TICKET_STATUS_ASSIGNED:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ticket is not assigned")

        assignment = await self.assignment_repository.get_by_ticket_id(ticket_id)
        if not assignment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
        if assignment["engineer_id"] != engineer_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ticket not assigned to this engineer")

        updated = await self.ticket_repository.update_status(
            ticket_id,
            TICKET_STATUS_RESOLVED,
            resolved_at=datetime.now(timezone.utc),
        )
        await self.assignment_repository.update_status_by_ticket(ticket_id, ASSIGNMENT_STATUS_COMPLETED)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
        return updated
