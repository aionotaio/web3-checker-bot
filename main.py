import asyncio 
import logging

from aiogram import Dispatcher 
from rabbitmq_rpc import RPCClient
from aiogram.fsm.storage.memory import MemoryStorage

from src.vars import BOT_API_TOKEN, RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS, RABBITMQ_HOST, RABBITMQ_PORT
from src.bot_instance import BotInstance
from handlers import start_handler, delete_wallets_handler, csv_handler, choose_projects_handler, check_wallets_handler, add_wallets_handler


logging.basicConfig(level=logging.INFO)


async def main():
    rpc_client = await RPCClient.create(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        user=RABBITMQ_DEFAULT_USER,
        password=RABBITMQ_DEFAULT_PASS,
        vhost='/',
        ssl=False,
    )

    bot = BotInstance.get_bot(BOT_API_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp['rpc_client'] = rpc_client
    
    dp.include_routers(start_handler.router, 
                       delete_wallets_handler.router, 
                       csv_handler.router, 
                       check_wallets_handler.router, 
                       choose_projects_handler.router, 
                       add_wallets_handler.router
                       )

    await dp.start_polling(bot)
    await rpc_client.close()


if __name__ == "__main__":
    asyncio.run(main())
