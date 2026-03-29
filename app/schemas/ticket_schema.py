from datetime import datetime

from pydantic import BaseModel


class TicketCreateRequest(BaseModel):
    issue_type: str
    description: str
    location: str


class TicketResponse(BaseModel):
    id: str
    user_id: str
    issue_type: str
    description: str
    location: str
    status: str
    created_at: datetime
