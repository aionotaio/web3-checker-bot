from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from shared.vars import PAGE_SIZE
from shared.session import get_db
from shared.exceptions import MissingError
from shared.bot_service import BotService
from shared.wallet_checker import WalletChecker


router = Router()

collection = get_db()
service = BotService(collection)


@router.callback_query(F.data == "delete_wallets")
async def delete_wallets(callback: types.CallbackQuery, state: FSMContext) -> None:
    msg = callback.message
    if not msg:
        return

    user_id = callback.from_user.id

    data = await state.get_data()
    page: int = data.get("page", 0)

    try:
        wallets = await service.read_all_wallets(user_id)
        if not wallets:
            inline_keyboard = [[types.InlineKeyboardButton(text="⏪ Quit", callback_data="go_back")]]
            builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
            await msg.edit_text("❗️ You haven't added any wallets", reply_markup=builder)
            return
    except MissingError:
        wallets = []

    start_index = page * PAGE_SIZE
    end_index = start_index + PAGE_SIZE
    wallets_to_show = wallets[start_index:end_index]

    inline_keyboard: list[list[types.InlineKeyboardButton]] = []

    inline_keyboard.append([types.InlineKeyboardButton(text="📤 Delete all", callback_data="delete_all_wallets")])

    for wallet in wallets_to_show:
        wallet_checker = WalletChecker(wallet)

        formatted_address = wallet_checker.format_address()

        inline_keyboard.append([types.InlineKeyboardButton(text=formatted_address, callback_data=f"delete_wallet:{wallet}")])

    pagination_buttons: list[types.InlineKeyboardButton] = []

    if start_index > 0:
        pagination_buttons.append(types.InlineKeyboardButton(text="◀️", callback_data=f"page:{page - 1}"))
    if end_index < len(wallets):
        pagination_buttons.append(types.InlineKeyboardButton(text="▶️", callback_data=f"page:{page + 1}"))

    if pagination_buttons:
        inline_keyboard.append(pagination_buttons)

    inline_keyboard.append([types.InlineKeyboardButton(text="⏪ Quit", callback_data="go_back")])

    builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    await state.update_data(page=page)

    await msg.edit_text(f"❓ Choose a wallet to delete:", reply_markup=builder)
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

    try:
        wallets = await service.read_all_wallets(user_id)
        if not wallets:
            inline_keyboard = [[types.InlineKeyboardButton(text="⏪ Quit", callback_data="go_back")]]
            builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
            await msg.edit_text("❗️ You haven't added any wallets", reply_markup=builder)
            return
    except MissingError:
        wallets = []

    inline_keyboard: list[list[types.InlineKeyboardButton]] = []

    inline_keyboard.append([types.InlineKeyboardButton(text="📤 Delete all", callback_data="delete_all_wallets")])

    start_index = page * PAGE_SIZE
    end_index = start_index + PAGE_SIZE
    wallets_to_show = wallets[start_index:end_index]

    for wallet in wallets_to_show:
        wallet_checker = WalletChecker(wallet)

        formatted_address = wallet_checker.format_address()

        inline_keyboard.append([types.InlineKeyboardButton(text=formatted_address, callback_data=f"delete_wallet:{wallet}")])

    pagination_buttons: list[types.InlineKeyboardButton] = []

    if start_index > 0:
        pagination_buttons.append(types.InlineKeyboardButton(text="◀️ ", callback_data=f"page:{page - 1}"))
    if end_index < len(wallets):
        pagination_buttons.append(types.InlineKeyboardButton(text="▶️", callback_data=f"page:{page + 1}"))

    if pagination_buttons:
        inline_keyboard.append(pagination_buttons)

    inline_keyboard.append([types.InlineKeyboardButton(text="⏪ Quit", callback_data="go_back")])

    builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    await state.update_data(page=page)

    await msg.edit_text(f"❓ Choose a wallet to delete:", reply_markup=builder)
    await callback.answer()


@router.callback_query(F.data == "delete_all_wallets")
async def delete_all_wallets(callback: types.CallbackQuery) -> None:
    msg = callback.message
    if not msg:
        return

    user_id = callback.from_user.id

    if not await service.delete_all_wallets(user_id):
        return

    inline_keyboard = [
        [types.InlineKeyboardButton(text="⏪ Quit", callback_data="go_back")]
    ]

    builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    await msg.edit_text(
        "📤 All your wallets were successfully deleted!", reply_markup=builder
    )
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

    inline_keyboard = [[types.InlineKeyboardButton(text="◀️ Go back", callback_data="go_back_to_delete")]]

    builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    try:
        await service.read_one_wallet(user_id, wallet_address)
    except MissingError:
        await msg.edit_text("❗️ Wallet not found", reply_markup=builder)
    else:
        await service.delete_one_wallet(user_id, wallet_address)
        await msg.edit_text(
            f"📤 Wallet <code>{wallet_address}</code> was successfully deleted",
            reply_markup=builder,
            parse_mode="HTML",
        )

    await callback.answer()


@router.callback_query(F.data == "go_back_to_delete")
async def go_back_to_delete(callback: types.CallbackQuery, state: FSMContext) -> None:
    await delete_wallets(callback, state)
