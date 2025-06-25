from datetime import datetime, timezone
from typing import Callable, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject

from shared.schemas import BotUser, BotUserUpdateData
from shared.exceptions import MissingError
from shared.bot_service import BotService


class CheckBanMiddleware(BaseMiddleware):
    def __init__(self, service: BotService):
        self.service = service

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        telegram_id = event.from_user.id

        try:
            user = await self.service.read_one_user(telegram_id)
        except MissingError:
            pass
        else:
            if user.is_banned:
                if isinstance(event, Message):
                    await event.answer("❗️ You're banned in this bot")
                elif isinstance(event, CallbackQuery):
                    await event.answer("❗️ You're banned in this bot", show_alert=True)
                return
        return await handler(event, data)


class SyncDataMiddleware(BaseMiddleware):
    def __init__(self, service: BotService):
        self.service = service

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        telegram_user = event.from_user

        telegram_id = telegram_user.id

        is_premium = telegram_user.is_premium
        if is_premium is None:
            is_premium = False

        try:
            await self.service.read_one_user(telegram_id)
        except MissingError:
            user_data: dict[str, Any] = {
                "full_name": telegram_user.full_name,
                "username": telegram_user.username,
                "telegram_id": telegram_id,
                "is_premium": is_premium,
                "is_banned": False,
                "language_code": telegram_user.language_code,
                "joined_at": datetime.now(timezone.utc),
                "last_active_at": datetime.now(timezone.utc),
                "wallets": [],
            }
            bot_user = BotUser.model_validate(user_data)
            await self.service.create_one_user(bot_user)
        else:
            user_data: dict[str, Any] = {
                "full_name": telegram_user.full_name,
                "username": telegram_user.username,
                "is_premium": is_premium,
                "language_code": telegram_user.language_code,
                "last_active_at": datetime.now(timezone.utc),
            }

            update_data = BotUserUpdateData.model_validate(user_data)
            await self.service.update_one_user(telegram_id, update_data)
        return await handler(event, data)
