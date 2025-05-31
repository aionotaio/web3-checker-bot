from aiogram import Bot


class BotInstance:
    instance = None

    @classmethod
    def get_bot(cls, token: str) -> Bot:
        if cls.instance is None:
            cls.instance = Bot(token=token)
        return cls.instance
