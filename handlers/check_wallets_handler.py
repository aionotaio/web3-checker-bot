import uuid
from typing import Any

from aiogram.fsm.context import FSMContext
from aiogram import F, Router, types, Dispatcher

from src.db import AsyncMongoManager
from rabbitmq.consumer import Consumer
from rabbitmq.producer import Producer
from src.wallet_checker import WalletChecker
from src.vars import PAGE_SIZE, TICKERS, CLAIM_LINKS, FORMATTED_NAMES


router = Router()
async_mongo_manager = AsyncMongoManager()


@router.callback_query(F.data == "check_wallets")
async def check_wallets(callback: types.CallbackQuery, state: FSMContext, dispatcher: Dispatcher):
    rpc_client = dispatcher['rpc_client']
    
    msg = callback.message
    if not msg: 
        return
    
    user_id = callback.from_user.id

    data = await state.get_data()

    selected_projects: list[str] = data.get("selected_projects", [])
    last_selected_projects: list[str] = data.get("last_selected_projects", [])
    saved_results: dict[str, Any] = data.get("wallet_results", {})

    wallets = await async_mongo_manager.read_all_user_wallets(user_id)

    if not selected_projects:
        inline_keyboard = [[types.InlineKeyboardButton(text="⏪ Выход", callback_data="go_back")]]

        builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

        await msg.edit_text("❗️ Вы не выбрали ни одного проекта", reply_markup=builder)
        await callback.answer()
        return
    
    if len(wallets) == 0:
        inline_keyboard = [[types.InlineKeyboardButton(text="⏪ Выход", callback_data="go_back")]]

        builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

        await msg.edit_text("❗️ У вас нет добавленных кошельков", reply_markup=builder)
        await callback.answer()
        return

    if selected_projects != last_selected_projects or not saved_results:
        await msg.delete()

        waiting_message = await msg.answer("🕐 Запрос отправлен, подождите...")

        results = {}

        for wallet in wallets:
            wallet_uuid = str(uuid.uuid4())

            producer = Producer(wallet, rpc_client)
            consumer = Consumer(wallet, rpc_client)

            await producer.publish_events(selected_projects, wallet_uuid)

            wallet_results = await consumer.consume_events(selected_projects, wallet_uuid)

            results[wallet] = wallet_results
            
        await state.update_data(wallet_results=results, last_selected_projects=selected_projects)
        await waiting_message.delete()

    inline_keyboard: list[list[types.InlineKeyboardButton]] = []

    page: int = data.get("page", 0)

    start_index = page * PAGE_SIZE
    end_index = start_index + PAGE_SIZE
    wallets_to_show = wallets[start_index:end_index]

    for wallet in wallets_to_show:
        wallet_checker = WalletChecker(wallet)

        formatted_address = wallet_checker.format_address()
        
        inline_keyboard.append([types.InlineKeyboardButton(text=formatted_address, callback_data=f"wallet_{wallet}")])

    pagination_buttons: list[types.InlineKeyboardButton] = []

    if start_index > 0:
        pagination_buttons.append(types.InlineKeyboardButton(text="◀️ Предыдущая", callback_data=f"checkwallet_page:{page - 1}"))
    if end_index < len(wallets):
        pagination_buttons.append(types.InlineKeyboardButton(text="▶️ Следующая", callback_data=f"checkwallet_page:{page + 1}"))

    if pagination_buttons:
        inline_keyboard.append(pagination_buttons)

    inline_keyboard.extend([
        [types.InlineKeyboardButton(text="📥 Скачать CSV (все)", callback_data="download_full_csv")],
        [types.InlineKeyboardButton(text="📥 Скачать CSV (только элигбл)", callback_data="download_eligible_csv")],
        [types.InlineKeyboardButton(text="⏪ Выход", callback_data="go_back_with_remove")]
    ])

    builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    

    await msg.answer("✅ Запрос завершен.\nВыберите кошелек для просмотра результатов:", reply_markup=builder)
    await callback.answer()

@router.callback_query(F.data.startswith("checkwallet_page:"))
async def change_check_wallet_page(callback: types.CallbackQuery, state: FSMContext, dispatcher: Dispatcher):
    msg = callback.message
    if not msg: 
        return
    
    callback_data = callback.data
    if not callback_data:
        return
    
    page = int(callback_data.split(":")[1])

    await state.update_data(page=page)
    await msg.delete()
    await check_wallets(callback, state, dispatcher)

@router.callback_query(F.data.startswith("wallet_"))
async def show_wallet_results(callback: types.CallbackQuery, state: FSMContext):
    msg = callback.message
    if not msg: 
        return
    
    callback_data = callback.data
    if not callback_data:
        return
    
    wallet = callback_data.split("_")[1]
    data = await state.get_data()

    wallet_results: dict[str, Any] = data.get("wallet_results", {}).get(wallet, {})

    if not wallet_results:
        result_message = "❗️ Нет данных для этого кошелька"
    else:
        result_message = f"✅ Результаты для кошелька <code>{wallet}</code>:\n\n"

        for project, details in wallet_results.items():
            project_name = FORMATTED_NAMES.get(project)

            result_message += f"🔸 {project_name}:\n"

            if type(details) == int:
                tokens = str(details)
                ticker: str = TICKERS.get(project, '')
                tokens_with_ticker = f'{tokens} {ticker}'
                eligibility = tokens != '0'
            else:
                tokens_with_ticker = 'N/A'
                eligibility = details

            claim_link = CLAIM_LINKS.get(project) if eligibility else 'N/A'

            result_message += f"— Элигбл: {eligibility}\n"
            result_message += f"— Кол-во токенов: {tokens_with_ticker}\n"
            
            if eligibility:
                result_message += f"— Клейм: {claim_link}\n\n"
            else:
                result_message += "\n"

    inline_keyboard = [[types.InlineKeyboardButton(text="◀️ Назад", callback_data="go_back_to_check_wallets")]]

    builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    
    await msg.edit_text(result_message, reply_markup=builder, disable_web_page_preview=True, parse_mode='HTML')
    await callback.answer()

@router.callback_query(F.data == "go_back_to_check_wallets")
async def go_back_to_check_wallets(callback: types.CallbackQuery, state: FSMContext, dispatcher: Dispatcher):
    msg = callback.message
    if not msg: 
        return
    
    await msg.delete()
    await check_wallets(callback, state, dispatcher)
