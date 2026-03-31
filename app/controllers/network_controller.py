from fastapi import APIRouter, Depends, HTTPException, status
import logging

from app.core.dependencies import require_admin
from app.schemas.network_schema import NetworkCreateRequest, NetworkResponse, NetworkUpdateRequest
from app.services.network_service import NetworkService

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Network"])


@router.get("/network", response_model=list)
async def get_network_nodes(_: dict = Depends(require_admin())):
    try:
        logger.info("Fetching all network nodes")
        return await NetworkService().get_all_nodes()
    except Exception as e:
        logger.error(f"Error in get_network_nodes: {str(e)}", exc_info=True)
        raise


@router.get("/network/{network_id}", response_model=NetworkResponse)
async def get_network_node(network_id: str, _: dict = Depends(require_admin())):
    try:
        logger.info(f"GET /network/{network_id}")
        return await NetworkService().get_node(network_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_network_node: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching network node: {str(e)}"
        )


@router.post("/network", response_model=NetworkResponse)
async def create_network_node(payload: NetworkCreateRequest, _: dict = Depends(require_admin())):
    try:
        logger.info(f"POST /network - Received payload: {payload}")
        return await NetworkService().create_node(payload)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in create_network_node: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating network node: {str(e)}"
        )


@router.put("/network/{network_id}", response_model=NetworkResponse)
async def update_network_node(network_id: str, payload: NetworkUpdateRequest, _: dict = Depends(require_admin())):
    try:
        logger.info(f"PUT /network/{network_id} - Received payload: {payload}")
        return await NetworkService().update_node_status(network_id, payload)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_network_node: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating network node: {str(e)}"
        )
