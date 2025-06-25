from aiogram import Bot

from shared.vars import BOT_API_TOKEN


class BotInstance:
    instance = None

    @classmethod
    def get_bot(cls) -> Bot:
        if cls.instance is None:
            cls.instance = Bot(token=BOT_API_TOKEN)
        return cls.instance
