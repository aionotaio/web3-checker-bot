from aiogram.fsm.state import State, StatesGroup


class WalletStates(StatesGroup):
    adding_wallets = State()
