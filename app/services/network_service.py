from fastapi import HTTPException, status

from app.repositories.network_repository import NetworkRepository
from app.schemas.network_schema import NetworkCreateRequest, NetworkUpdateRequest
from app.utils.constants import NETWORK_STATUS_ACTIVE, NETWORK_STATUS_DOWN, NETWORK_STATUS_MAINTENANCE


class NetworkService:
    def __init__(self):
        self.network_repository = NetworkRepository()

    async def create_node(self, payload: NetworkCreateRequest) -> dict:
        node_status = payload.status.strip().lower()
        if node_status not in {NETWORK_STATUS_ACTIVE, NETWORK_STATUS_DOWN, NETWORK_STATUS_MAINTENANCE}:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid network status")
        node_doc = {
            "tower_id": payload.tower_id,
            "location": payload.location,
            "status": node_status,
        }
        return await self.network_repository.create(node_doc)

    async def update_node_status(self, network_id: str, payload: NetworkUpdateRequest) -> dict:
        node_status = payload.status.strip().lower()
        if node_status not in {NETWORK_STATUS_ACTIVE, NETWORK_STATUS_DOWN, NETWORK_STATUS_MAINTENANCE}:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid network status")
        updated = await self.network_repository.update_status(network_id, node_status)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Network node not found")
        return updated
