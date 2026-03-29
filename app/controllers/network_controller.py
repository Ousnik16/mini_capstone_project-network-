from fastapi import APIRouter, Depends

from app.core.dependencies import require_admin
from app.schemas.network_schema import NetworkCreateRequest, NetworkResponse, NetworkUpdateRequest
from app.services.network_service import NetworkService

router = APIRouter(tags=["Network"])


@router.post("/network", response_model=NetworkResponse)
async def create_network_node(payload: NetworkCreateRequest, _: dict = Depends(require_admin())):
    return await NetworkService().create_node(payload)


@router.put("/network/{network_id}", response_model=NetworkResponse)
async def update_network_node(network_id: str, payload: NetworkUpdateRequest, _: dict = Depends(require_admin())):
    return await NetworkService().update_node_status(network_id, payload)
