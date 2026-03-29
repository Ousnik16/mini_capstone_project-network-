from pydantic import BaseModel


class NetworkCreateRequest(BaseModel):
    tower_id: str
    location: str
    status: str


class NetworkUpdateRequest(BaseModel):
    status: str


class NetworkResponse(BaseModel):
    id: str
    tower_id: str
    location: str
    status: str
