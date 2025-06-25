from typing import Annotated

from fastapi import APIRouter, Response, Depends, Query, Path, status
from motor.motor_asyncio import AsyncIOMotorCollection

from services.auth import get_current_admin
from services.admin_service import AdminService
from shared.vars import MAX_INT64
from shared.session import get_db
from shared.schemas import BotUser, ResponseMsg


router = APIRouter(prefix="/api/users")


@router.get(
    "/",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ResponseMsg},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ResponseMsg},
    },
    dependencies=[Depends(get_current_admin)],
)
async def get_all_users(
    response: Response,
    page: Annotated[int | None, Query(ge=0, le=MAX_INT64)] = None,
    size: Annotated[int | None, Query(ge=1, le=100)] = None,
    collection: AsyncIOMotorCollection = Depends(get_db),
    language_code: Annotated[str | None, Query(min_length=2, max_length=2, regex=r".*[^\x00-\x1F\s].*")] = None,
    is_banned: bool | None = None,
    is_premium: bool | None = None,
) -> list[BotUser]:
    service = AdminService(collection)

    users = await service.read_all_users(page, size, language_code, is_banned, is_premium)
    total = len(users)

    response.headers["X-Total-Count"] = str(total)
    response.headers["Access-Control-Expose-Headers"] = "X-Total-Count"

    return users


@router.get(
    "/{telegram_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ResponseMsg},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ResponseMsg},
    },
    dependencies=[Depends(get_current_admin)],
)
async def get_one_user(
    telegram_id: Annotated[int, Path(gt=0, le=MAX_INT64)],
    collection: AsyncIOMotorCollection = Depends(get_db),
) -> BotUser:
    service = AdminService(collection)

    return await service.read_one_user(telegram_id)


@router.patch(
    "/{telegram_id}/ban",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ResponseMsg},
        status.HTTP_405_METHOD_NOT_ALLOWED: {"model": ResponseMsg},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ResponseMsg},
    },
    dependencies=[Depends(get_current_admin)],
)
async def ban_user(
    telegram_id: Annotated[int, Path(gt=0, le=MAX_INT64)],
    collection: AsyncIOMotorCollection = Depends(get_db),
) -> BotUser:
    service = AdminService(collection)

    return await service.ban_one_user(telegram_id)


@router.patch(
    "/{telegram_id}/unban",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ResponseMsg},
        status.HTTP_405_METHOD_NOT_ALLOWED: {"model": ResponseMsg},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ResponseMsg},
    },
    dependencies=[Depends(get_current_admin)],
)
async def unban_user(
    telegram_id: Annotated[int, Path(gt=0, le=MAX_INT64)],
    collection: AsyncIOMotorCollection = Depends(get_db),
) -> BotUser:
    service = AdminService(collection)

    return await service.unban_one_user(telegram_id)
