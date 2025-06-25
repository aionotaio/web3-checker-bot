import asyncio
from datetime import datetime, timezone

from aiogram import Bot
from motor.motor_asyncio import AsyncIOMotorCollection

from shared.vars import BATCH_SIZE
from shared.schemas import BotUser, AllStats, ActiveStats, LanguageStats
from shared.exceptions import EmptyError
from shared.bot_service import BotService
from shared.bot_instance import BotInstance
from admin.repositories.admin_repo import AdminRepository


class AdminService(BotService):
    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self.repo = AdminRepository(collection)
        self.bot = BotInstance.get_bot()
        self.semaphore = asyncio.Semaphore(BATCH_SIZE)

    async def read_all_users(
        self,
        page: int | None = None,
        size: int | None = None,
        language_code: str | None = None,
        is_banned: bool | None = None,
        is_premium: bool | None = None,
    ) -> list[BotUser]:
        bot_users_dicts = await self.repo.read_all_users()
        if len(bot_users_dicts) == 0:
            raise EmptyError("No users found")

        bot_users = [BotUser.model_validate(bot_user) for bot_user in bot_users_dicts]

        if language_code is not None:
            bot_users = [user for user in bot_users if user.language_code == language_code]

        if is_banned is not None:
            bot_users = [user for user in bot_users if user.is_banned == is_banned]

        if is_premium is not None:
            bot_users = [user for user in bot_users if user.is_premium == is_premium]

        if page is not None and size is not None:
            offset_min = page * size
            offset_max = offset_min + size
            return bot_users[offset_min:offset_max]

        return bot_users

    async def ban_one_user(self, telegram_id: int) -> BotUser:
        await self.read_one_user(telegram_id)
        result = await self.repo.ban_one_user(telegram_id)
        return BotUser.model_validate(result)

    async def unban_one_user(self, telegram_id: int) -> BotUser:
        await self.read_one_user(telegram_id)
        result = await self.repo.unban_one_user(telegram_id)
        return BotUser.model_validate(result)

    async def send_message_to_one_user(self, telegram_id: int, bot: Bot, message: str) -> None:
        async with self.semaphore:
            await self.read_one_user(telegram_id)
            await bot.send_message(chat_id=telegram_id, text=message)
            await asyncio.sleep(0.05)

    async def send_message_to_all_users(self, telegram_ids: list[int], bot: Bot, message: str) -> None:
        tasks = [self.send_message_to_one_user(telegram_id, bot, message) for telegram_id in telegram_ids]

        await asyncio.gather(*tasks)

    async def get_active_stats(self, users: list[BotUser], now: datetime) -> ActiveStats:
        stats = {
            "active_users": {
                "last_24h": sum(1 for user in users if user.last_active_at and (now - user.last_active_at.replace(tzinfo=timezone.utc)).days < 1),
                "last_7d": sum(1 for user in users if user.last_active_at and (now - user.last_active_at.replace(tzinfo=timezone.utc)).days < 7),
            },
            "first_user_joined_at": min((user.joined_at for user in users), default=None),
            "last_user_active_at": max((user.last_active_at for user in users if user.last_active_at), default=None),
        }

        return ActiveStats.model_validate(stats)

    async def get_language_stats(self, users: list[BotUser]) -> LanguageStats:
        languages = {}
        for user in users:
            lang = user.language_code or "None"
            languages[lang] = languages.get(lang, 0) + 1

        stats = {"languages": languages}

        return LanguageStats.model_validate(stats)

    async def get_all_stats(self, users: list[BotUser], now: datetime) -> AllStats:
        total = len(users)

        active_stats = await self.get_active_stats(users, now)
        language_stats = await self.get_language_stats(users)

        stats = {
            "total_users": total,
            "active_stats": active_stats,
            "banned_users": sum(1 for user in users if user.is_banned),
            "premium_users": sum(1 for user in users if user.is_premium),
            "language_stats": language_stats,
        }

        return AllStats.model_validate(stats)
