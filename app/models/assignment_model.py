from datetime import datetime

from pydantic import BaseModel, Field


class AssignmentModel(BaseModel):
    ticket_id: str
    engineer_id: str
    assigned_at: datetime
    status: str


class AssignmentInDB(AssignmentModel):
    id: str = Field(alias="_id")
