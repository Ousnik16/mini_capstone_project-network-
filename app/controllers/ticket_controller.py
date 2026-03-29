from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user, require_admin, require_customer, require_engineer
from app.schemas.ticket_schema import TicketCreateRequest, TicketResponse
from app.services.ticket_service import TicketService

router = APIRouter(tags=["Tickets"])


@router.post("/tickets", response_model=TicketResponse)
async def create_ticket(payload: TicketCreateRequest, current_user: dict = Depends(require_customer())):
    return await TicketService().create_ticket(payload, current_user["id"])


@router.get("/tickets/my", response_model=list[TicketResponse])
async def get_my_tickets(current_user: dict = Depends(require_customer())):
    return await TicketService().get_my_tickets(current_user["id"])


@router.get("/tickets", response_model=list[TicketResponse])
async def get_all_tickets(_: dict = Depends(require_admin())):
    return await TicketService().get_all_tickets()


@router.put("/tickets/{ticket_id}/resolve", response_model=TicketResponse)
async def resolve_ticket(ticket_id: str, current_user: dict = Depends(require_engineer() or require_admin())):
    return await TicketService().resolve_ticket(ticket_id, current_user["id"])
