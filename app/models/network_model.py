from pydantic import BaseModel, Field


class NetworkNodeModel(BaseModel):
    tower_id: str
    location: str
    status: str


class NetworkNodeInDB(NetworkNodeModel):
    id: str = Field(alias="_id")
