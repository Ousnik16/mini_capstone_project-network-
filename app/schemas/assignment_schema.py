from datetime import datetime

from pydantic import BaseModel


class AssignmentRequest(BaseModel):
    engineer_id: str


class AssignmentResponse(BaseModel):
    id: str
    ticket_id: str
    engineer_id: str
    assigned_at: datetime
    status: str


class AdminReportResponse(BaseModel):
    total_tickets: int
    open_tickets: int
    assigned_tickets: int
    resolved_tickets: int
    avg_resolution_seconds: float
