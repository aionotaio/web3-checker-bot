import os
from typing import Any

from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext

from src.csv_manager import CSVManager
from src.vars import TICKERS, FORMATTED_NAMES, CLAIM_LINKS, FULL_RESULTS_TEMP_CSV, FULL_RESULTS_CSV, ELIGIBLE_RESULTS_TEMP_CSV, ELIGIBLE_RESULTS_CSV


router = Router()


@router.callback_query(F.data == "delete_file")
async def delete_file(callback: types.CallbackQuery, state: FSMContext) -> None:
    msg = callback.message
    if not msg: 
        return
    
    await msg.delete()
    return

async def download_full_csv(callback: types.CallbackQuery, state: FSMContext) -> None:
    msg = callback.message
    if not msg: 
        return
    
    data = await state.get_data()
    results: dict[str, dict[str, Any]] = data.get("wallet_results", {})
    
    inline_keyboard = [[types.InlineKeyboardButton(text="❌ Скрыть файл", callback_data="delete_file")]]

    builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    csv_data: list[Any] = []

    for wallet, wallet_results in results.items():
        for project, details in wallet_results.items():
            project_name = FORMATTED_NAMES.get(project)

            if type(details) == int:
                tokens = str(details)
                ticker: str = TICKERS.get(project, '')
                tokens_with_ticker = f'{tokens} {ticker}'
                eligibility = tokens != '0'
            else:
                tokens_with_ticker = 'N/A'
                eligibility = details

            claim_link = CLAIM_LINKS.get(project) if eligibility else 'N/A'

            csv_data.append([wallet, project_name, tokens_with_ticker, eligibility, claim_link])

    await CSVManager.write_to_csv(csv_data, FULL_RESULTS_TEMP_CSV)

    input_file = types.FSInputFile(FULL_RESULTS_TEMP_CSV, filename=FULL_RESULTS_CSV)

    await msg.answer_document(input_file, reply_markup=builder)

    os.remove(FULL_RESULTS_TEMP_CSV)

async def download_eligible_csv(callback: types.CallbackQuery, state: FSMContext) -> None:
    msg = callback.message
    if not msg: 
        return
    
    data = await state.get_data()
    wallet_results: dict[str, dict[str, Any]] = data.get("wallet_results", {})
    
    inline_keyboard = [[types.InlineKeyboardButton(text="❌ Скрыть файл", callback_data="delete_file")]]
    builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    csv_data: list[Any] = []

    for wallet, results in wallet_results.items():
        for project, details in results.items():
            project_name = FORMATTED_NAMES.get(project)

            if type(details) == int:
                tokens = str(details)
                ticker: str = TICKERS.get(project, '')
                tokens_with_ticker = f'{tokens} {ticker}'
                eligibility = tokens != '0'
            else:
                tokens_with_ticker = 'N/A'
                eligibility = details

            claim_link = CLAIM_LINKS.get(project) if eligibility else 'N/A'
            
            if eligibility:
                csv_data.append([wallet, project_name, tokens_with_ticker, eligibility, claim_link])

    await CSVManager.write_eligible_to_csv(csv_data, ELIGIBLE_RESULTS_TEMP_CSV)

    input_file = types.FSInputFile(ELIGIBLE_RESULTS_TEMP_CSV, filename=ELIGIBLE_RESULTS_CSV)

    await msg.answer_document(input_file, reply_markup=builder)

    os.remove(ELIGIBLE_RESULTS_TEMP_CSV)

@router.callback_query(F.data == "download_full_csv")
async def handle_download_full_csv(callback: types.CallbackQuery, state: FSMContext) -> None:
    await download_full_csv(callback, state)
    await callback.answer()

@router.callback_query(F.data == "download_eligible_csv")
async def handle_download_eligible_csv(callback: types.CallbackQuery, state: FSMContext) -> None:
    await download_eligible_csv(callback, state)
    await callback.answer()
