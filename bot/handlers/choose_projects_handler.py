from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from shared.vars import FORMATTED_NAMES


router = Router()


@router.callback_query(F.data == "choose_projects")
async def choose_projects(callback: types.CallbackQuery, state: FSMContext):
    msg = callback.message
    if not msg: 
        return
    
    inline_keyboard: list[list[types.InlineKeyboardButton]] = []

    data = await state.get_data()
    selected_projects: list[str] = data.get("selected_projects", [])
    
    last_selected_projects = selected_projects.copy()
    await state.update_data(last_selected_projects=last_selected_projects)

    for key, value in FORMATTED_NAMES.items():
        button_text = f"✅ {value}" if key in selected_projects else value
        inline_keyboard.append([types.InlineKeyboardButton(text=button_text, callback_data=f"toggle_{key}")])

    inline_keyboard.append([types.InlineKeyboardButton(text="✅ Select all", callback_data="choose_all")])
    inline_keyboard.append([types.InlineKeyboardButton(text="❌ Deselect all", callback_data="deselect_all")])
    inline_keyboard.append([types.InlineKeyboardButton(text="⏪ Quit", callback_data="go_back")])

    builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    await msg.edit_text("❓ Select projects to check your allocation", reply_markup=builder)
    await callback.answer()


@router.callback_query(F.data.startswith("toggle_"))
async def toggle_project(callback: types.CallbackQuery, state: FSMContext):
    msg = callback.message
    if not msg: 
        return
    
    callback_data = callback.data
    if not callback_data:
        return
    
    project = callback_data.split("_")[1]

    data = await state.get_data()
    selected_projects: list[str] = data.get("selected_projects", [])
    
    last_selected_projects = selected_projects.copy()
    await state.update_data(last_selected_projects=last_selected_projects)

    if project in selected_projects:
        selected_projects.remove(project)
    else:
        selected_projects.append(project)

    await state.update_data(selected_projects=selected_projects)

    inline_keyboard: list[list[types.InlineKeyboardButton]] = []

    for key, value in FORMATTED_NAMES.items():
        button_text = f"✅ {value}" if key in selected_projects else value
        inline_keyboard.append([types.InlineKeyboardButton(text=button_text, callback_data=f"toggle_{key}")])

    inline_keyboard.append([types.InlineKeyboardButton(text="✅ Select all", callback_data="choose_all")])
    inline_keyboard.append([types.InlineKeyboardButton(text="❌ Deselect all", callback_data="deselect_all")])
    inline_keyboard.append([types.InlineKeyboardButton(text="⏪ Quit", callback_data="go_back")])
    
    builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    await msg.edit_text("❓ Select projects to check your allocation", reply_markup=builder)
    await callback.answer()


@router.callback_query(F.data == "choose_all")
async def choose_all_projects(callback: types.CallbackQuery, state: FSMContext):
    msg = callback.message
    if not msg: 
        return
    
    selected_projects = list(FORMATTED_NAMES.keys())

    await state.update_data(selected_projects=selected_projects)

    inline_keyboard: list[list[types.InlineKeyboardButton]] = []

    for key, value in FORMATTED_NAMES.items():
        button_text = f"✅ {value}" if key in selected_projects else value
        inline_keyboard.append([types.InlineKeyboardButton(text=button_text, callback_data=f"toggle_{key}")])
    
    inline_keyboard.append([types.InlineKeyboardButton(text="✅ Select all", callback_data="choose_all")])
    inline_keyboard.append([types.InlineKeyboardButton(text="❌ Deselect all", callback_data="deselect_all")])
    inline_keyboard.append([types.InlineKeyboardButton(text="⏪ Quit", callback_data="go_back")])

    builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    await msg.edit_text("❓ Select projects to check your allocation", reply_markup=builder)
    await callback.answer()


@router.callback_query(F.data == "deselect_all")
async def deselect_all_projects(callback: types.CallbackQuery, state: FSMContext):
    msg = callback.message
    if not msg: 
        return
    
    await state.update_data(selected_projects=[])

    inline_keyboard: list[list[types.InlineKeyboardButton]] = []

    for key, value in FORMATTED_NAMES.items():
        button_text = f"✅ {value}" if key in [] else value
        inline_keyboard.append([types.InlineKeyboardButton(text=button_text, callback_data=f"toggle_{key}")])

    inline_keyboard.append([types.InlineKeyboardButton(text="✅ Select all", callback_data="choose_all")])
    inline_keyboard.append([types.InlineKeyboardButton(text="❌ Deselect all", callback_data="deselect_all")])
    inline_keyboard.append([types.InlineKeyboardButton(text="⏪ Quit", callback_data="go_back")])

    builder = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    await msg.edit_text("❓ Select projects to check your allocation", reply_markup=builder)
    await callback.answer()
