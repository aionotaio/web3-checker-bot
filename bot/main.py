import asyncio
import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from rabbitmq_rpc import RPCClient

from handlers import start_handler, delete_wallets_handler, csv_handler, choose_projects_handler, check_wallets_handler, add_wallets_handler
from shared.vars import RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS, RABBITMQ_HOST, RABBITMQ_PORT
from shared.session import get_db
from shared.bot_service import BotService
from shared.bot_instance import BotInstance
from services.middlewares import CheckBanMiddleware, SyncDataMiddleware


logging.basicConfig(level=logging.INFO)


collection = get_db()
service = BotService(collection)


async def main():
    rpc_client = await RPCClient.create(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        user=RABBITMQ_DEFAULT_USER,
        password=RABBITMQ_DEFAULT_PASS,
        vhost="/",
        ssl=False,
    )

    bot = BotInstance.get_bot()
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.middleware(CheckBanMiddleware(service))
    dp.message.middleware(SyncDataMiddleware(service))

    dp.callback_query.middleware(CheckBanMiddleware(service))
    dp.callback_query.middleware(SyncDataMiddleware(service))

    dp["rpc_client"] = rpc_client

    dp.include_routers(
        start_handler.router,
        delete_wallets_handler.router,
        csv_handler.router,
        check_wallets_handler.router,
        choose_projects_handler.router,
        add_wallets_handler.router,
    )

    await dp.start_polling(bot)
    await rpc_client.close()


if __name__ == "__main__":
    asyncio.run(main())
