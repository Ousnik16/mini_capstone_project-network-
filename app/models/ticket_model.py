from datetime import datetime

from pydantic import BaseModel, Field


class TicketModel(BaseModel):
    user_id: str
    issue_type: str
    description: str
    location: str
    status: str
    created_at: datetime


class TicketInDB(TicketModel):
    id: str = Field(alias="_id")
