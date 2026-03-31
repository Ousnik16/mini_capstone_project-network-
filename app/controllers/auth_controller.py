from fastapi import APIRouter

from app.schemas.auth_schema import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user_schema import UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
async def register(payload: RegisterRequest):
    return await AuthService().register(payload)


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest):
    return await AuthService().login(payload)
