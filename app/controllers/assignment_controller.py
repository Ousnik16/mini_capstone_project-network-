from fastapi import APIRouter, Depends

from app.core.dependencies import require_engineer
from app.schemas.ticket_schema import TicketResponse
from app.services.assignment_service import AssignmentService

router = APIRouter(tags=["Engineer"])


@router.get("/engineer/tickets", response_model=list[TicketResponse])
async def get_engineer_tickets(current_user: dict = Depends(require_engineer())):
    return await AssignmentService().get_engineer_tickets(current_user["id"])
