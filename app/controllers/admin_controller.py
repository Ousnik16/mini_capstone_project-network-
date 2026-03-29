from fastapi import APIRouter, Depends

from app.core.dependencies import require_admin
from app.schemas.assignment_schema import AdminReportResponse, AssignmentRequest, AssignmentResponse
from app.services.assignment_service import AssignmentService

router = APIRouter(tags=["Admin"])


@router.put("/tickets/{ticket_id}/assign", response_model=AssignmentResponse)
async def assign_ticket(ticket_id: str, payload: AssignmentRequest, _: dict = Depends(require_admin())):
    return await AssignmentService().assign_ticket(ticket_id, payload.engineer_id)


@router.get("/admin/reports", response_model=AdminReportResponse)
async def admin_reports(_: dict = Depends(require_admin())):
    return await AssignmentService().get_admin_report()
