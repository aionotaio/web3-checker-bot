from typing import Annotated
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, status, Query
from motor.motor_asyncio import AsyncIOMotorCollection

from services.auth import get_current_admin
from services.admin_service import AdminService
from shared.session import get_db
from shared.schemas import LanguageStats, AllStats, ActiveStats, ResponseMsg


router = APIRouter(prefix="/api/stats")


@router.get(
    "/",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ResponseMsg},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ResponseMsg},
    },
    dependencies=[Depends(get_current_admin)],
)
async def get_all_stats(
    collection: AsyncIOMotorCollection = Depends(get_db),
) -> AllStats:
    service = AdminService(collection)

    users = await service.read_all_users()
    now = datetime.now(timezone.utc)
    return await service.get_all_stats(users, now)


@router.get(
    "/activity",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ResponseMsg},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ResponseMsg},
    },
    dependencies=[Depends(get_current_admin)],
)
async def get_activity_stats(
    collection: AsyncIOMotorCollection = Depends(get_db),
) -> ActiveStats:
    service = AdminService(collection)

    users = await service.read_all_users()
    now = datetime.now(timezone.utc)
    return await service.get_active_stats(users, now)


@router.get(
    "/languages",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ResponseMsg},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ResponseMsg},
    },
    dependencies=[Depends(get_current_admin)],
)
async def get_language_stats(
    top: Annotated[int | None, Query(gt=0, le=50)] = None,
    collection: AsyncIOMotorCollection = Depends(get_db),
) -> LanguageStats:
    service = AdminService(collection)

    users = await service.read_all_users()
    language_stats = await service.get_language_stats(users)
    lang_dict = language_stats.model_dump()

    if top:
        return LanguageStats.model_validate(dict(sorted(lang_dict.items(), key=lambda item: item[1], reverse=True)[:top]))
    return LanguageStats.model_validate(dict(sorted(lang_dict.items(), key=lambda item: item[1], reverse=True)))
