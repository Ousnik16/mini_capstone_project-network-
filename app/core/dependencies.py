from typing import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.config import settings
from app.repositories.user_repository import UserRepository
from app.utils.constants import ROLE_ADMIN, ROLE_CUSTOMER, ROLE_ENGINEER

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await UserRepository().get_by_id(user_id)
    if not user or not user.get("is_active", True):
        raise credentials_exception
    return user


def require_roles(*roles: str) -> Callable:
    async def checker(current_user: dict = Depends(get_current_user)) -> dict:
        if current_user.get("role") not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user

    return checker


def require_customer() -> Callable:
    return require_roles(ROLE_CUSTOMER)


def require_engineer() -> Callable:
    return require_roles(ROLE_ENGINEER)


def require_admin() -> Callable:
    return require_roles(ROLE_ADMIN)
