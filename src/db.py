from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient

from src.vars import MONGO_INITDB_ROOT_USERNAME, MONGO_INITDB_ROOT_PASSWORD, MONGO_HOST, MONGO_PORT

class AsyncMongoManager:
    def __init__(self) -> None:
        self.client = AsyncIOMotorClient(f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin")
        self.database = self.client['admin']
        self.collection = self.database["users"]

    async def create_new_user(self, username: str, user_id: int) -> bool:
        if await self.collection.find_one({"tg_id": user_id}):
            return False
        
        user: dict[str, Any] = {
            "tg_name": username,
            "tg_id": user_id,
            "wallets": []
        }

        result = await self.collection.insert_one(user)
        return result.acknowledged

    async def insert_new_wallet(self, user_id: int, wallet: str) -> bool:
        if await self.collection.find_one({"tg_id": user_id, "wallets": {"$in": [wallet]}}):
            return False
        
        result = await self.collection.update_one(
            {"tg_id": user_id}, 
            {"$push": {
                "wallets": wallet
                }
            }
        )
        return result.acknowledged
    
    async def read_all_user_wallets(self, user_id: int) -> list[str]:
        return await self.collection.distinct('wallets', {"tg_id": user_id})

    async def read_one_user_wallet(self, user_id: int, wallet: str) -> Any:
        return wallet if await self.collection.find_one({"tg_id": user_id, "wallets": {"$in": [wallet]}}) else False
        
    async def delete_all_user_wallets(self, user_id: int) -> bool:
        result = await self.collection.update_one(
            {"tg_id": user_id}, 
            {"$set": {
                "wallets": []
                }
            }
        )
        return result.acknowledged
    
    async def delete_one_user_wallet(self, user_id: int, wallet: str) -> bool:
        result = await self.collection.update_one(
            {"tg_id": user_id}, 
            {"$pull": {
                "wallets": wallet
                }
            }
        )
        return result.acknowledged
