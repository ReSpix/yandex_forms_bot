from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot import dp
from utils import get_new_text, save_response


@dp.callback_query(F.data == "take")
async def accept_task(callback: CallbackQuery):
    button_call = InlineKeyboardButton(text="Позвонил клиенту", callback_data="call")
    button_accept = InlineKeyboardButton(text="Клиент наш", callback_data="accept")
    button_refuse = InlineKeyboardButton(text="Отказ клиента", callback_data="refuse")

    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[[button_call], [button_accept], [button_refuse]]
    )
    await callback.message.edit_text(
        get_new_text(callback.message.text, f"Взято в работу"),
        reply_markup=inline_kb,
    )
    save_response(callback.message.text, callback.from_user.username, "take")


@dp.callback_query(F.data == "call")
async def refure_task(callback: CallbackQuery):
    button_accept = InlineKeyboardButton(text="Клиент наш", callback_data="accept")
    button_refuse = InlineKeyboardButton(text="Отказ клиента", callback_data="refuse")

    inline_kb = InlineKeyboardMarkup(inline_keyboard=[[button_accept], [button_refuse]])
    await callback.message.edit_text(
        get_new_text(callback.message.text, f"Позвонили клиенту"),
        reply_markup=inline_kb,
    )
    res = save_response(callback.message.text, callback.from_user.username, "call")


@dp.callback_query(F.data == "accept")
async def refure_task(callback: CallbackQuery):
    await callback.message.edit_text(
        get_new_text(callback.message.text, f"Клиент принял работу")
    )
    save_response(callback.message.text, callback.from_user.username, "accept")


@dp.callback_query(F.data == "refuse")
async def refure_task(callback: CallbackQuery):
    await callback.message.edit_text(
        get_new_text(callback.message.text, f"Клиент отказался")
    )
    save_response(callback.message.text, callback.from_user.username, "refuse")
