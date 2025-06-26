import asyncio
import logging
from logging.handlers import RotatingFileHandler

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from rabbitmq_rpc import RPCClient

from handlers import start_handler, delete_wallets_handler, csv_handler, choose_projects_handler, check_wallets_handler, add_wallets_handler
from shared.vars import RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS, RABBITMQ_HOST, RABBITMQ_PORT, BOT_LOGS_PATH
from shared.session import get_db
from shared.bot_service import BotService
from shared.bot_instance import BotInstance
from services.middlewares import CheckBanMiddleware, SyncDataMiddleware


file_log = RotatingFileHandler(BOT_LOGS_PATH, 'a', 1000000, 5)
console_log = logging.StreamHandler()

logging.basicConfig(handlers=(file_log, console_log), level=logging.INFO, format="%(asctime)s.%(msecs)03d | %(levelname)s | %(name)s | %(message)s")


async def main():
    collection = get_db()
    service = BotService(collection)

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
