from fastapi import HTTPException, status
import logging

from app.repositories.network_repository import NetworkRepository
from app.schemas.network_schema import NetworkCreateRequest, NetworkUpdateRequest
from app.utils.constants import NETWORK_STATUS_ACTIVE, NETWORK_STATUS_DOWN, NETWORK_STATUS_MAINTENANCE

logger = logging.getLogger(__name__)


class NetworkService:
    def __init__(self):
        self.network_repository = NetworkRepository()

    async def create_node(self, payload: NetworkCreateRequest) -> dict:
        try:
            logger.info(f"Creating network node with payload: {payload}")
            
            if not payload.tower_id or not str(payload.tower_id).strip():
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="tower_id is required and cannot be empty")
            if not payload.location or not str(payload.location).strip():
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="location is required and cannot be empty")
            if not payload.status or not str(payload.status).strip():
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="status is required and cannot be empty")
            
            node_status = str(payload.status).strip().lower()
            valid_statuses = {NETWORK_STATUS_ACTIVE, NETWORK_STATUS_DOWN, NETWORK_STATUS_MAINTENANCE}
            if node_status not in valid_statuses:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                    detail=f"Invalid network status '{node_status}'. Must be one of: {', '.join(sorted(valid_statuses))}"
                )
            node_doc = {
                "tower_id": str(payload.tower_id).strip(),
                "location": str(payload.location).strip(),
                "status": node_status,
            }
            logger.info(f"Network node document: {node_doc}")
            return await self.network_repository.create(node_doc)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating network node: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating network node: {str(e)}"
            )

    async def update_node_status(self, network_id: str, payload: NetworkUpdateRequest) -> dict:
        try:
            logger.info(f"Updating network node {network_id} with payload: {payload}")
            
            if not any([payload.tower_id, payload.location, payload.status]):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="At least one field (tower_id, location, or status) is required"
                )
            
            update_data = {}
            
            if payload.tower_id:
                update_data["tower_id"] = str(payload.tower_id).strip()
            
            if payload.location:
                update_data["location"] = str(payload.location).strip()
            
            if payload.status:
                node_status = str(payload.status).strip().lower()
                valid_statuses = {NETWORK_STATUS_ACTIVE, NETWORK_STATUS_DOWN, NETWORK_STATUS_MAINTENANCE}
                if node_status not in valid_statuses:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail=f"Invalid network status '{node_status}'. Must be one of: {', '.join(sorted(valid_statuses))}"
                    )
                update_data["status"] = node_status
            
            updated = await self.network_repository.update(network_id, update_data)
            if not updated:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Network node not found")
            logger.info(f"Successfully updated network node {network_id}")
            return updated
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating network node: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating network node: {str(e)}"
            )

    async def get_all_nodes(self) -> list:
        try:
            return await self.network_repository.get_all()
        except Exception as e:
            logger.error(f"Error fetching network nodes: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching network nodes: {str(e)}"
            )

    async def get_node(self, network_id: str) -> dict:
        try:
            node = await self.network_repository.get_by_id(network_id)
            if not node:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Network node not found")
            return node
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error fetching network node: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching network node: {str(e)}"
            )
