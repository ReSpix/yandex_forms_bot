import re
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import requests
from tgbot import dp, bot, chat_id, user_in_chat
from utils import is_notify_skip


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if not await user_in_chat(message):
        return
    await message.answer(f"Этот бот присылает полученные ответы из Яндекс формы")
    await show_commands(message)


@dp.message(Command("status"))
async def command_start_handler(message: Message) -> None:
    if not await user_in_chat(message):
        return
    await message.answer(f"(1/2) Бот: Активен ✅")
    service_status = "Неактивен ❌"
    try:
        res = requests.get(
            "https://test-forstbityandexformstgbotdev.pagekite.me/status"
        )
        if "ok" in res.text:
            service_status = "Активен ✅"
    except:
        pass
    await message.answer(f"(2/2) Сервис: {service_status}")


@dp.message(Command("explain"))
async def command_start_handler(message: Message) -> None:
    if not await user_in_chat(message):
        return
    await message.answer(
        f"Команда статус показывает 2 статуса: бот и сервис.\n\n🤖 Бот отвечает за работу кнопок в сообщениях.\n\n💻 Сервис отвечает за уведомление о сообщениях, на которые нет отклика.\n\nP.S. Даже если и бот, и сервис неактивны, сообщения из Яндекс форм все равно будут приходить (но кнопки работать не будут)"
    )


@dp.message(Command("notify"))
async def notify(message: Message):
    if not await user_in_chat(message):
        return
    if is_notify_skip():
        return

    button_work = InlineKeyboardButton(text="Взял в работу", callback_data="take")
    button_call = InlineKeyboardButton(text="Позвонил клиенту", callback_data="call")
    button_accept = InlineKeyboardButton(text="Клиент наш", callback_data="accept")
    button_refuse = InlineKeyboardButton(text="Отказ клиента", callback_data="refuse")

    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[[button_work], [button_call], [button_accept], [button_refuse]]
    )

    url = f"http://api:8000/notify/"
    res = requests.get(url).json()

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


@dp.message(Command("commands"))
async def show_commands(message: Message):
    if not await user_in_chat(message):
        return
    commands = await bot.get_my_commands()
    text = [f'/{a.command} - {a.description}' for a in commands]
    text.insert(0, 'Команды бота:')
    await message.answer('\n'.join(text))