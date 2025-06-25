from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from shared.session import get_db
from shared.bot_service import BotService


router = Router()

collection = get_db()
service = BotService(collection)


@router.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    user = message.from_user
    if user is None:
        return

    content, builder = await service.get_menu(user.full_name)

    await message.answer(content, parse_mode="HTML", reply_markup=builder)


@router.callback_query(F.data == "go_back_with_remove")
async def go_back_with_remove(callback: types.CallbackQuery, state: FSMContext):
    msg = callback.message
    if msg is None:
        return

    await msg.delete()

    content, builder = await service.get_menu(callback.from_user.full_name)

    await msg.answer(content, parse_mode="HTML", reply_markup=builder)
    await callback.answer()


@router.callback_query(F.data == "go_back")
async def go_back(callback: types.CallbackQuery, state: FSMContext) -> None:
    msg = callback.message
    if msg is None:
        return

    content, builder = await service.get_menu(callback.from_user.full_name)

    await msg.edit_text(content, parse_mode="HTML", reply_markup=builder)
    await callback.answer()
