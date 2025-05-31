import re
import io
from typing import Optional

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.vars import BOT_API_TOKEN
from src.states import WalletStates
from src.db import AsyncMongoManager
from src.bot_instance import BotInstance


router = Router()
bot = BotInstance.get_bot(BOT_API_TOKEN)
async_mongo_manager = AsyncMongoManager()


@router.callback_query(F.data == "add_wallets")
async def add_wallets(callback: types.CallbackQuery, state: FSMContext) -> None:
    msg = callback.message
    if not msg: 
        return

    await state.update_data(message_id=msg.message_id)

    inline_keyboard = [
        [types.InlineKeyboardButton(text="⏪ Выход", callback_data="go_back")]
    ]

    builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    content = '📥 Отправь адреса кошельков <b>(не приватники)</b> сообщением или .txt-файлом.\nФормат — 1 строка -> 1 кошелек'

    await msg.edit_text(content, parse_mode="HTML", reply_markup=builder)
    await state.set_state(WalletStates.adding_wallets)
    await callback.answer()

@router.message(WalletStates.adding_wallets)
async def handle_wallets(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()

    message_id = data.get("message_id")
    if message_id:
        msg_bot = message.bot
        if not msg_bot: 
            return

        await msg_bot.delete_message(chat_id=message.chat.id, message_id=message_id)
        await state.update_data(message_id=None)
    
    added_wallets: list[str] = []
    duplicate_wallets: list[str] = []
    invalid_wallets: list[str] = []
    
    if message.content_type == 'text':
        msg_text = message.text
        if not msg_text: 
            return

        wallets = msg_text.splitlines()

        for wallet in wallets:
            if re.match(r"^0x[a-fA-F0-9]{40}$", wallet):
                user = message.from_user
                if not user:
                    return
                
                if await async_mongo_manager.insert_new_wallet(user.id, wallet):
                    added_wallets.append(wallet)
                else:
                    duplicate_wallets.append(wallet)
            else:
                invalid_wallets.append(wallet)

    elif message.content_type == 'document':
        file = message.document
        if not file:
            return

        if file.mime_type != "text/plain":
            inline_keyboard = [[types.InlineKeyboardButton(text="⏪ Выход", callback_data="go_back")]]

            builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

            await message.answer('❗️ Неправильный формат файла', reply_markup=builder, parse_mode='HTML')
            return

        file_info = await bot.get_file(file.file_id)

        file_path = file_info.file_path
        if not file_path: 
            return

        file_content: Optional[io.BytesIO] = await bot.download_file(file_path)
        if not file_content: 
            return

        file_text = file_content.getvalue().decode('utf-8')

        wallets = file_text.splitlines()

        for wallet in wallets:
            if re.match(r"^0x[a-fA-F0-9]{40}$", wallet):
                user = message.from_user
                if not user: 
                    return
                
                if await async_mongo_manager.insert_new_wallet(user.id, wallet):
                    added_wallets.append(wallet)
                else:
                    duplicate_wallets.append(wallet)
            else:
                invalid_wallets.append(wallet)

    await state.update_data(
        added_wallets=added_wallets,
        duplicate_wallets=duplicate_wallets,
        invalid_wallets=invalid_wallets
    )

    response = ""
    if added_wallets:
        response += "✅ Добавлены следующие кошельки:\n" + "\n".join(f"<code>{wallet}</code>" for wallet in added_wallets) + "\n\n"
    if duplicate_wallets:
        response += "❓ Эти кошельки уже были добавлены:\n" + "\n".join(f"<code>{wallet}</code>" for wallet in duplicate_wallets) + "\n\n"
    if invalid_wallets:
        response += "❗️ Неверные адреса кошельков:\n" + "\n".join(f"<code>{wallet}</code>" for wallet in invalid_wallets) + "\n"

    inline_keyboard = [[types.InlineKeyboardButton(text="➕ Завершить добавление", callback_data="finish_adding_wallets")]]

    builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    if "bot_message" not in data:
        bot_message = await message.answer(
            text=response if response else "❗️ Не удалось добавить ни одного кошелька. Проверьте формат и попробуйте заново",
            parse_mode="HTML",
            reply_markup=builder
        )
        await state.update_data(bot_message=bot_message)
    else:
        bot_message = data['bot_message']

        try:
            await bot_message.delete()
        except Exception:
            pass

        bot_message = await message.answer(
            text=response if response else "❗️ Не удалось добавить ни одного кошелька. Проверьте формат и попробуйте заново",
            parse_mode="HTML",
            reply_markup=builder
        )
        await state.update_data(bot_message=bot_message)

    if "bot_message" in data:
        data.pop("bot_message")
        await state.update_data(data)

@router.callback_query(F.data == "finish_adding_wallets")
async def finish_adding_wallets(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    
    msg = callback.message
    if msg is None:
        return

    inline_keyboard = [[types.InlineKeyboardButton(text="⏪ Выход", callback_data="go_back")]]

    builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    await msg.edit_text("✅ Добавление кошельков завершено", reply_markup=builder)
    await callback.answer()
