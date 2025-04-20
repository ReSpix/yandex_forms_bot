from ..reminders import notify
from ..key import api_url
from ..tgbot import dp, bot, user_in_chat
import requests
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from typing import Callable
import re
from functools import wraps


def requires_user_in_chat(func: Callable):
    @wraps(func)
    async def wrapper(message: Message, *args, **kwargs):
        if not await user_in_chat(message):
            return
        return await func(message, *args, **kwargs)
    return wrapper


@dp.message(CommandStart())
@requires_user_in_chat
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Этот бот присылает полученные ответы из Яндекс формы")
    await show_commands(message)


@dp.message(Command("status"))
async def command_status_handler(message: Message) -> None:
    if not await user_in_chat(message):
        return
    await message.answer(f"(1/2) Бот: Активен ✅")
    service_status = "Неактивен ❌"
    try:
        res = requests.get(api_url, timeout=10)
        if "ok" in res.text:
            service_status = "Активен ✅"
    except:
        pass
    await message.answer(f"(2/2) Сервис: {service_status}")


@dp.message(Command("explain"))
async def command_explain_handler(message: Message) -> None:
    if not await user_in_chat(message):
        return
    await message.answer(
        f"Команда статус показывает 2 статуса: бот и сервис.\n\n🤖 Бот отвечает за работу кнопок в сообщениях.\n\n💻 Сервис отвечает за уведомление о сообщениях, на которые нет отклика.\n\nP.S. Даже если и бот, и сервис неактивны, сообщения из Яндекс форм все равно будут приходить (но кнопки работать не будут)"
    )


@dp.message(Command("notify"))
@requires_user_in_chat
async def handle_notify(message: Message):
    await notify()


@dp.message(Command("commands"))
async def show_commands(message: Message):
    if not await user_in_chat(message):
        return
    commands = await bot.get_my_commands()
    text = [f'/{a.command} - {a.description}' for a in commands]
    text.insert(0, 'Команды бота:')
    await message.answer('\n'.join(text))
