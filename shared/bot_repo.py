from typing import Any

from motor.motor_asyncio import AsyncIOMotorCollection


class BotRepository:
    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self.collection = collection

    async def create_one_user(self, user: dict[str, Any]) -> dict[str, Any] | None:
        result = await self.collection.insert_one(user)
        return user if result.inserted_id else None

    async def create_one_wallet(self, telegram_id: int, wallet: str) -> dict[str, Any] | None:
        result = await self.collection.update_one(
            {"telegram_id": telegram_id}, 
            {"$push": {
                "wallets": wallet
                }
            }
        )

        return await self.read_one_user(telegram_id) if result.modified_count != 0 else None
    
    async def read_one_user(self, telegram_id: int) -> dict[str, Any] | None:
        return await self.collection.find_one({"telegram_id": telegram_id})

    async def read_one_wallet(self, telegram_id: int, wallet: str) -> dict[str, Any] | None:
        return await self.collection.find_one({"telegram_id": telegram_id, "wallets": {"$in": [wallet]}})
    
    async def read_all_wallets(self, telegram_id: int) -> list[str]:
        return await self.collection.distinct('wallets', {"telegram_id": telegram_id})
    
    async def update_one_user(self, telegram_id: int, user_data: dict[str, Any]) -> None:
        await self.collection.update_one(
            {"telegram_id": telegram_id}, 
            {"$set": user_data}
        )
        
    async def delete_one_wallet(self, telegram_id: int, wallet: str) -> dict[str, Any] | None:
        result = await self.collection.update_one(
            {"telegram_id": telegram_id}, 
            {"$pull": {
                "wallets": wallet
                }
            }
        )
        return await self.read_one_user(telegram_id) if result.modified_count != 0 else None

    async def delete_all_wallets(self, telegram_id: int) -> dict[str, Any] | None:
        result = await self.collection.update_one(
            {"telegram_id": telegram_id}, 
            {"$set": {
                "wallets": []
                }
            }
        )
        return await self.read_one_user(telegram_id) if result.modified_count != 0 else None
