from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.vars import PAGE_SIZE
from src.db import AsyncMongoManager
from src.wallet_checker import WalletChecker


router = Router()
async_mongo_manager = AsyncMongoManager()


@router.callback_query(F.data == "delete_wallets")
async def delete_wallets(callback: types.CallbackQuery, state: FSMContext) -> None:
    msg = callback.message
    if not msg: 
        return
    
    user_id = callback.from_user.id

    data = await state.get_data()
    page: int = data.get("page", 0)

    wallets = await async_mongo_manager.read_all_user_wallets(user_id)

    if not wallets:
        inline_keyboard = [[types.InlineKeyboardButton(text="⏪ Выход", callback_data="go_back")]]
        builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        await msg.edit_text("❗️ У вас нет добавленных кошельков", reply_markup=builder)
        return

    start_index = page * PAGE_SIZE
    end_index = start_index + PAGE_SIZE
    wallets_to_show = wallets[start_index:end_index]

    inline_keyboard: list[list[types.InlineKeyboardButton]] = []

    inline_keyboard.append([types.InlineKeyboardButton(text="📤 Удалить все", callback_data="delete_all_wallets")])

    for wallet in wallets_to_show:
        wallet_checker = WalletChecker(wallet)

        formatted_address = wallet_checker.format_address()
        
        inline_keyboard.append([types.InlineKeyboardButton(text=formatted_address, callback_data=f"delete_wallet:{wallet}")])

    pagination_buttons: list[types.InlineKeyboardButton] = []

    if start_index > 0:
        pagination_buttons.append(types.InlineKeyboardButton(text="◀️ Предыдущая", callback_data=f"page:{page - 1}"))
    if end_index < len(wallets):
        pagination_buttons.append(types.InlineKeyboardButton(text="▶️ Следующая", callback_data=f"page:{page + 1}"))

    if pagination_buttons:
        inline_keyboard.append(pagination_buttons)
    
    inline_keyboard.append([types.InlineKeyboardButton(text="⏪ Выход", callback_data="go_back")])

    builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    await state.update_data(page=page)

    await msg.edit_text(f"❓ Выберите кошелек для удаления:", reply_markup=builder)
    await callback.answer()

@router.callback_query(F.data.startswith("page:"))
async def change_page(callback: types.CallbackQuery, state: FSMContext) -> None:
    callback_data = callback.data
    if not callback_data:
        return

    msg = callback.message
    if not msg: 
        return
    
    user_id = callback.from_user.id

    page: int = int(callback_data.split(":")[1])

    wallets = await async_mongo_manager.read_all_user_wallets(user_id)

    if not wallets:
        inline_keyboard = [[types.InlineKeyboardButton(text="⏪ Выход", callback_data="go_back")]]
        builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        await msg.edit_text("❗️ У вас нет добавленных кошельков", reply_markup=builder)
        return
    
    inline_keyboard: list[list[types.InlineKeyboardButton]] = []

    inline_keyboard.append([types.InlineKeyboardButton(text="📤 Удалить все", callback_data="delete_all_wallets")])

    start_index = page * PAGE_SIZE
    end_index = start_index + PAGE_SIZE
    wallets_to_show = wallets[start_index:end_index]

    for wallet in wallets_to_show:
        wallet_checker = WalletChecker(wallet)

        formatted_address = wallet_checker.format_address()
        
        inline_keyboard.append([types.InlineKeyboardButton(text=formatted_address, callback_data=f"delete_wallet:{wallet}")])

    pagination_buttons: list[types.InlineKeyboardButton] = []

    if start_index > 0:
        pagination_buttons.append(types.InlineKeyboardButton(text="◀️ Предыдущая", callback_data=f"page:{page - 1}"))
    if end_index < len(wallets):
        pagination_buttons.append(types.InlineKeyboardButton(text="▶️ Следующая", callback_data=f"page:{page + 1}"))

    if pagination_buttons:
        inline_keyboard.append(pagination_buttons)

    inline_keyboard.append([types.InlineKeyboardButton(text="⏪ Выход", callback_data="go_back")])
    
    builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    await state.update_data(page=page)

    await msg.edit_text(f"❓ Выберите кошелек для удаления:", reply_markup=builder)
    await callback.answer()

@router.callback_query(F.data == "delete_all_wallets")
async def delete_all_wallets(callback: types.CallbackQuery) -> None:
    msg = callback.message
    if not msg: 
        return
    
    user_id = callback.from_user.id
    
    await async_mongo_manager.delete_all_user_wallets(user_id)
    
    inline_keyboard = [[types.InlineKeyboardButton(text="⏪ Выход", callback_data="go_back")]]

    builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    await msg.edit_text("📤 Все ваши кошельки были успешно удалены", reply_markup=builder)
    await callback.answer()

@router.callback_query(F.data.startswith("delete_wallet:"))
async def confirm_delete_wallet(callback: types.CallbackQuery) -> None:
    callback_data = callback.data
    if not callback_data:
        return

    msg = callback.message
    if not msg: 
        return
    
    wallet_address = callback_data.split(":")[1]
    user_id = callback.from_user.id

    is_wallet_created = await async_mongo_manager.read_one_user_wallet(user_id, wallet_address)

    inline_keyboard = [[types.InlineKeyboardButton(text="◀️ Назад", callback_data="go_back_to_delete")]]

    builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    if is_wallet_created:
        await async_mongo_manager.delete_one_user_wallet(user_id, wallet_address)
        await msg.edit_text(f"📤 Кошелек <code>{wallet_address}</code> был успешно удален", reply_markup=builder, parse_mode='HTML')
    else:
        await msg.edit_text("❗️ Кошелек не найден", reply_markup=builder)

    await callback.answer()

@router.callback_query(F.data == "go_back_to_delete")
async def go_back_to_delete(callback: types.CallbackQuery, state: FSMContext) -> None:
    await delete_wallets(callback, state)
