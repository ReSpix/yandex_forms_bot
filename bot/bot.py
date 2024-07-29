import asyncio
import logging
import sys
import requests

from aiogram import F, Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from key import TOKEN

from buttons import get_new_text, get_original_text
from urllib.parse import quote

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Этот бот присылает полученные ответы из Яндекс формы")


@dp.message(Command("status"))
async def command_start_handler(message: Message) -> None:
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
    await message.answer(
        f"Команда статус показывает 2 статуса: бот и сервис.\n\n🤖 Бот отвечает за работу кнопок в сообщениях.\n\n💻 Сервис отвечает за уведомление о сообщениях, на которые не было откликов в течении суток.\n\nP.S. Даже если и бот, и сервис неактивны, сообщения из Яндекс форм все равно будут приходить (но кнопки работать не будут)"
    )


def save_response(text, username, type):
    text = get_original_text(text)
    text = quote(text)
    url = f"http://api:8000/response/{text}/{username}/{type}"
    res = requests.get(url)
    return res.text


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


@dp.message(Command("notify"))
async def notify(message: Message):
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
        await bot.send_message(
            chat_id="-4226511920", text="Необработанных запросов нет"
        )
    else:
        await bot.send_message(
            chat_id="-4226511920", text=f"Необработанные запросы - {len(res)} шт:"
        )
        for i in res:
            await bot.send_message(
                chat_id="-4226511920", text=i["text"], reply_markup=inline_kb
            )


async def notify_scedule():
    print("NOTIFIED")
    await notify(None)

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

scheduler = AsyncIOScheduler()
scheduler.add_job(
    notify_scedule, 'cron', hour=9, minute=30
)


@dp.message(F.text)
async def any_message(message: Message):
    print(f'Сообщение: "{message.text}" от {message.from_user.username}')


async def main() -> None:
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
