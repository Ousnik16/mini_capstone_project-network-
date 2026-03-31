from pydantic import BaseModel
from typing import Optional


class NetworkCreateRequest(BaseModel):
    tower_id: str
    location: str
    status: str


class NetworkUpdateRequest(BaseModel):
    tower_id: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None

    class Config:
        pass


class NetworkResponse(BaseModel):
    id: str
    tower_id: str
    location: str
    status: str
