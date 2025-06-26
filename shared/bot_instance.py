from aiogram import Bot

from shared.settings import settings


class BotInstance:
    instance = None

    @classmethod
    def get_bot(cls) -> Bot:
        if cls.instance is None:
            cls.instance = Bot(token=settings.bot_api_token)
        return cls.instance
