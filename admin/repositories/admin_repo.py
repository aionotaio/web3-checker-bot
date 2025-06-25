from typing import Any

from motor.motor_asyncio import AsyncIOMotorCollection

from shared.bot_repo import BotRepository


class AdminRepository(BotRepository):
    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        super().__init__(collection)

    async def read_all_users(self) -> list[dict[str, Any]]:
        users = [user async for user in self.collection.find()]
        return users
    
    async def ban_one_user(self, telegram_id: int) -> dict[str, Any] | None:
        result = await self.collection.update_one(
            {"telegram_id": telegram_id}, 
            {"$set": {
                "is_banned": True
            }}
        )
        return await self.read_one_user(telegram_id) if result.matched_count != 0 else None

    async def unban_one_user(self, telegram_id: int) -> dict[str, Any] | None:
        result = await self.collection.update_one(
            {"telegram_id": telegram_id}, 
            {"$set": {
                "is_banned": False
            }}
        )
        return await self.read_one_user(telegram_id) if result.matched_count != 0 else None
