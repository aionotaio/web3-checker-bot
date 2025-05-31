from aiogram.filters import Command
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.db import AsyncMongoManager


router = Router()
async_mongo_manager = AsyncMongoManager()


@router.message(Command('start'))
async def cmd_start(message: types.Message) -> None:
    inline_keyboard = [
        [types.InlineKeyboardButton(text="📥 Добавить кошельки", callback_data="add_wallets")],
        [types.InlineKeyboardButton(text="📤 Удалить кошельки", callback_data="delete_wallets")],
        [types.InlineKeyboardButton(text="❓ Выбрать проекты", callback_data="choose_projects")],
        [types.InlineKeyboardButton(text="✅ Проверить аллокации", callback_data="check_wallets")]
    ]

    builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    user = message.from_user
    if user is None: 
        return
    
    content = f"👋 Привет, <b>{user.full_name}</b>! Для начала добавь адреса EVM-кошельков и выбери проекты, в которых ты хочешь проверить свою аллокацию."

    await async_mongo_manager.create_new_user(user.full_name, user.id)

    await message.answer(content, parse_mode="HTML", reply_markup=builder)

@router.callback_query(F.data == "go_back_with_remove")
async def go_back_with_remove(callback: types.CallbackQuery, state: FSMContext):
    msg = callback.message
    if msg is None: 
        return
    
    await msg.delete()
    
    inline_keyboard = [
        [types.InlineKeyboardButton(text="📥 Добавить кошельки", callback_data="add_wallets")],
        [types.InlineKeyboardButton(text="📤 Удалить кошельки", callback_data="delete_wallets")],
        [types.InlineKeyboardButton(text="❓ Выбрать проекты", callback_data="choose_projects")],
        [types.InlineKeyboardButton(text="✅ Проверить аллокации", callback_data="check_wallets")]
    ]

    builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    content = f"👋 Привет, <b>{callback.from_user.full_name}</b>! Для начала добавь адреса EVM-кошельков и выбери проекты, в которых ты хочешь проверить свою аллокацию."

    await msg.answer(content, parse_mode="HTML", reply_markup=builder)
    await callback.answer()

@router.callback_query(F.data == "go_back")
async def go_back(callback: types.CallbackQuery, state: FSMContext) -> None:
    msg = callback.message
    if msg is None: 
        return

    inline_keyboard = [
        [types.InlineKeyboardButton(text="📥 Добавить кошельки", callback_data="add_wallets")],
        [types.InlineKeyboardButton(text="📤 Удалить кошельки", callback_data="delete_wallets")],
        [types.InlineKeyboardButton(text="❓ Выбрать проекты", callback_data="choose_projects")],
        [types.InlineKeyboardButton(text="✅ Проверить аллокации", callback_data="check_wallets")]
    ]

    builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    content = f"👋 Привет, <b>{callback.from_user.full_name}</b>! Для начала добавь адреса EVM-кошельков и выбери проекты, в которых ты хочешь проверить свою аллокацию."
    
    await msg.edit_text(content, parse_mode="HTML", reply_markup=builder)
    await callback.answer()
