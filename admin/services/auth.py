from typing import Any
from datetime import datetime, timezone, timedelta

from jose import JWTError, jwt
from fastapi import Depends, Request
from passlib.context import CryptContext

from shared.session import get_admin_db
from shared.schemas import AdminUser
from shared.settings import settings
from shared.exceptions import MissingError, WrongCredentialsError, TokenValidationError


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

collection = get_admin_db()


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(seconds=settings.jwt_expire_seconds)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError:
        raise TokenValidationError("Failed to auth admin due to failed token decoding")


async def authn_admin(username: str, password: str) -> AdminUser:
    dict_admin: dict[str, Any] = await collection.find_one({"username": username})
    if not dict_admin:
        raise MissingError("User not exists")

    admin = AdminUser.model_validate(dict_admin)
    if verify_password(password, admin.hashed_password) is False:
        raise WrongCredentialsError("Failed to auth admin due to wrong credentials")
    return admin


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise TokenValidationError("Failed to auth admin due to not found token")
    return token


async def get_current_admin(token: str = Depends(get_token)):
    payload = decode_access_token(token)

    username = payload.get("sub")
    if not username:
        raise TokenValidationError("Failed to auth admin due to failed token validation")

    expire = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenValidationError("Failed to auth admin due to expired token")

    dict_admin: dict[str, Any] = await collection.find_one({"username": username})
    if not dict_admin:
        raise MissingError("User not exists")
    return AdminUser.model_validate(dict_admin)
