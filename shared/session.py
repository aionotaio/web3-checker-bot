from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from shared.settings import settings


def get_db() -> AsyncIOMotorCollection:
    client = AsyncIOMotorClient(f"mongodb://{settings.mongo_initdb_root_username}:{settings.mongo_initdb_root_password}@{settings.mongo_host}:{settings.mongo_port}/?authSource=admin")
    db = client['admin']
    return db["users"]


def get_admin_db() -> AsyncIOMotorCollection:
    client = AsyncIOMotorClient(f"mongodb://{settings.mongo_initdb_root_username}:{settings.mongo_initdb_root_password}@{settings.mongo_host}:{settings.mongo_port}/?authSource=admin")
    db = client['admin']
    return db["admins"]
