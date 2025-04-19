from .utils import is_notify_skip
import requests
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .key import chat_id
from .tgbot import bot
from core import get_notify

async def notify():
    button_work = InlineKeyboardButton(
        text="Взял в работу", callback_data="take")
    button_call = InlineKeyboardButton(
        text="Позвонил клиенту", callback_data="call")
    button_accept = InlineKeyboardButton(
        text="Клиент принял", callback_data="accept")
    button_refuse = InlineKeyboardButton(
        text="Отказ клиента", callback_data="refuse")

    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[[button_work], [button_call],
                         [button_accept], [button_refuse]]
    )

    # url = f"http://api:8000/notify/"
    # res = requests.get(url).json()
    res = get_notify()

    if len(res) == 0:
        await bot.send_message(chat_id=chat_id, text="Необработанных запросов нет")
    else:
        await bot.send_message(
            chat_id=chat_id, text=f"Необработанные запросы - {len(res)} шт:"
        )
        for i in res:
            await bot.send_message(
                chat_id=chat_id, text=i["text"], reply_markup=inline_kb
            )


async def notify_scheduler():
    if is_notify_skip():
        return
    await notify()
