from rabbitmq_rpc import RPCClient
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from shared.vars import MONGO_INITDB_ROOT_USERNAME, MONGO_INITDB_ROOT_PASSWORD, MONGO_HOST, MONGO_PORT


def get_db() -> AsyncIOMotorCollection:
    client = AsyncIOMotorClient(f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin")
    db = client['admin']
    return db["users"]


def get_admin_db() -> AsyncIOMotorCollection:
    client = AsyncIOMotorClient(f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin")
    db = client['admin']
    return db["admins"]
