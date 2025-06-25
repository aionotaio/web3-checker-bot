from typing import Annotated

import docker
from aiogram import Bot
from fastapi import APIRouter, status, Depends, Body, Path
from motor.motor_asyncio import AsyncIOMotorCollection

from services.auth import get_current_admin
from services.admin_service import AdminService
from shared.vars import BOT_CONTAINER_NAME, MAX_INT64
from shared.schemas import ResponseMsg
from shared.session import get_db
from shared.bot_instance import BotInstance


router = APIRouter(prefix="/api/bot")
client = docker.from_env()


@router.post(
    "/start",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ResponseMsg},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ResponseMsg},
    },
    dependencies=[Depends(get_current_admin)],
)
def start_bot() -> None:
    container = client.containers.get(BOT_CONTAINER_NAME)
    container.start()


@router.post(
    "/stop",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ResponseMsg},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ResponseMsg},
    },
    dependencies=[Depends(get_current_admin)],
)
def stop_bot() -> None:
    container = client.containers.get(BOT_CONTAINER_NAME)
    container.stop()


@router.post(
    "/restart",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ResponseMsg},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ResponseMsg},
    },
    dependencies=[Depends(get_current_admin)],
)
def restart_bot() -> None:
    container = client.containers.get(BOT_CONTAINER_NAME)
    container.restart()


@router.post(
    "/notify",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ResponseMsg},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ResponseMsg},
    },
    dependencies=[Depends(get_current_admin)],
)
async def send_message_to_all_users(
    message: Annotated[str, Body(min_length=1, max_length=4096, embed=True, pattern=r".*[^\x00-\x1F\s].*")],
    collection: AsyncIOMotorCollection = Depends(get_db),
    bot: Bot = Depends(BotInstance.get_bot),
) -> None:
    service = AdminService(collection)

    users = await service.read_all_users()
    telegram_ids = [user.telegram_id for user in users]
    await service.send_message_to_all_users(telegram_ids, bot, message)


@router.post(
    "/notify/{telegram_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ResponseMsg},
        status.HTTP_404_NOT_FOUND: {"model": ResponseMsg},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ResponseMsg},
    },
    dependencies=[Depends(get_current_admin)],
)
async def send_message_to_one_user(
    telegram_id: Annotated[int, Path(gt=0, le=MAX_INT64)],
    message: Annotated[
        str,
        Body(min_length=1, max_length=4096, embed=True, pattern=r".*[^\x00-\x1F\s].*"),
    ],
    collection: AsyncIOMotorCollection = Depends(get_db),
    bot: Bot = Depends(BotInstance.get_bot),
) -> None:
    service = AdminService(collection)

    await service.send_message_to_one_user(telegram_id, bot, message)
