from fastapi import APIRouter, HTTPException, Request, status
from pydantic import ValidationError

from app.schemas.auth_schema import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user_schema import UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
async def register(payload: RegisterRequest):
    return await AuthService().register(payload)


@router.post("/login", response_model=TokenResponse)
async def login(request: Request):
    content_type = request.headers.get("content-type", "")
    payload_data: dict

    if "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
        form_data = await request.form()
        payload_data = {
            "email": form_data.get("email") or form_data.get("username"),
            "password": form_data.get("password"),
        }
    else:
        payload_data = await request.json()
        if "email" not in payload_data and "username" in payload_data:
            payload_data["email"] = payload_data.get("username")

    try:
        payload = LoginRequest(**payload_data)
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.errors())

    return await AuthService().login(payload)
