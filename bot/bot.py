import asyncio
import logging
import sys
import requests

from aiogram import F, Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from key import TOKEN

from buttons import get_new_text

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Этот бот получает ответы из Яндекс формы.\nСостояние бота: Активен."
    )
    service_status = 'Неактивно'
    try:
        res = requests.get('https://testyandexformstgbot.serveo.net/status')
        if 'ok' in res.text:
            service_status = 'Активно'
    except:
        pass
    await message.answer(f"Состояние сервсиса: {service_status}")


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


@dp.callback_query(F.data == "call")
async def refure_task(callback: CallbackQuery):
    button_accept = InlineKeyboardButton(text="Клиент наш", callback_data="accept")
    button_refuse = InlineKeyboardButton(text="Отказ клиента", callback_data="refuse")

    inline_kb = InlineKeyboardMarkup(inline_keyboard=[[button_accept], [button_refuse]])
    await callback.message.edit_text(
        get_new_text(callback.message.text, f"Позвонили клиенту"),
        reply_markup=inline_kb,
    )


@dp.callback_query(F.data == "accept")
async def refure_task(callback: CallbackQuery):
    await callback.message.edit_text(
        get_new_text(callback.message.text, f"Клиент принял работу")
    )


@dp.callback_query(F.data == "refuse")
async def refure_task(callback: CallbackQuery):
    await callback.message.edit_text(
        get_new_text(callback.message.text, f"Клиент отказался")
    )


@dp.message(F.text)
async def any_message(message: Message):
    print(f'Сообщение: "{message.text}" от {message.from_user.username}')


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
