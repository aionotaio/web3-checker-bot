from aiogram import types
from motor.motor_asyncio import AsyncIOMotorCollection

from shared.schemas import BotUser, BotUserUpdateData
from shared.bot_repo import BotRepository
from shared.exceptions import AlreadyExistsError, MissingError


class BotService:
    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self.repo = BotRepository(collection)

    async def create_one_user(self, user: BotUser) -> BotUser | None:
        try:
            await self.read_one_user(user.telegram_id)
        except MissingError:
            pass
        else:
            raise AlreadyExistsError("User already exists")

        dict_from_user = user.model_dump()

        result = await self.repo.create_one_user(dict_from_user)
        return BotUser.model_validate(result) if result is not None else None

    async def create_one_wallet(self, telegram_id: int, wallet: str) -> BotUser | None:
        await self.read_one_user(telegram_id)
        result = await self.repo.create_one_wallet(telegram_id, wallet)
        return BotUser.model_validate(result) if result is not None else None

    async def read_one_user(self, telegram_id: int) -> BotUser:
        result = await self.repo.read_one_user(telegram_id)
        if not result:
            raise MissingError("User not exists")

        return BotUser.model_validate(result)

    async def read_one_wallet(self, telegram_id: int, wallet: str) -> BotUser:
        result = await self.repo.read_one_wallet(telegram_id, wallet)
        if not result:
            raise MissingError("Wallet not exists")

        return BotUser.model_validate(result)

    async def read_all_wallets(self, telegram_id: int) -> list[str]:
        await self.read_one_user(telegram_id)
        return await self.repo.read_all_wallets(telegram_id)

    async def update_one_user(self, telegram_id: int, user_data: BotUserUpdateData) -> None:
        await self.read_one_user(telegram_id)
        await self.repo.update_one_user(telegram_id, user_data.model_dump())

    async def delete_one_wallet(self, telegram_id: int, wallet: str) -> BotUser | None:
        await self.read_one_user(telegram_id)
        await self.read_one_wallet(telegram_id, wallet)

        result = await self.repo.delete_one_wallet(telegram_id, wallet)
        return BotUser.model_validate(result) if result is not None else None

    async def delete_all_wallets(self, telegram_id: int) -> BotUser | None:
        await self.read_one_user(telegram_id)
        result = await self.repo.delete_all_wallets(telegram_id)
        return BotUser.model_validate(result) if result is not None else None

    async def get_menu(self, user_full_name: str) -> tuple[str, types.InlineKeyboardMarkup]:
        content = f"👋 Hello, <b>{user_full_name}</b>! First of all you need to add your ethereum wallets addresses and select all the projects you want to check your allocation."

        inline_keyboard = [
            [types.InlineKeyboardButton(text="📥 Add wallets", callback_data="add_wallets")],
            [types.InlineKeyboardButton(text="📤 Delete wallets", callback_data="delete_wallets")],
            [types.InlineKeyboardButton(text="❓ Select projects", callback_data="choose_projects")],
            [types.InlineKeyboardButton(text="✅ Check allocations", callback_data="check_wallets")]
        ]

        builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

        return content, builder
