from fastapi import HTTPException, status

from app.core.security import create_access_token, get_password_hash, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import LoginRequest, RegisterRequest, TokenResponse
from app.utils.constants import ROLE_ADMIN, ROLE_CUSTOMER, ROLE_ENGINEER
from app.utils.validators import normalize_email


class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()

    async def register(self, payload: RegisterRequest) -> dict:
        role = payload.role.strip().lower()
        if role not in {ROLE_CUSTOMER, ROLE_ENGINEER, ROLE_ADMIN}:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid role")

        email = normalize_email(payload.email)
        existing = await self.user_repository.get_by_email(email)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

        user_doc = {
            "name": payload.name,
            "email": email,
            "password": get_password_hash(payload.password),
            "role": role,
            "is_active": True,
        }
        created = await self.user_repository.create(user_doc)
        created.pop("password", None)
        return created

    async def login(self, payload: LoginRequest) -> TokenResponse:
        email = normalize_email(payload.email)
        user = await self.user_repository.get_by_email(email)
        if not user or not verify_password(payload.password, user.get("password", "")):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        if not user.get("is_active", True):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User inactive")
        token = create_access_token(subject=user["id"], role=user["role"])
        return TokenResponse(access_token=token)
