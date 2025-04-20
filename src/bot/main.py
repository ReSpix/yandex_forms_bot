import asyncio
import logging
import sys
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .scheduler import activate_scheduler, shutdown_scheduler
from .tgbot import dp, bot
from . import handlers
from .key import chat_id


async def shutdown():
    shutdown_scheduler()
    await dp.stop_polling()


async def main() -> None:
    activate_scheduler()
    await dp.start_polling(bot, handle_signals=False)


async def send_message(text):
    button_refuse = InlineKeyboardButton(text="Взять в работу", callback_data="take")

    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[[button_refuse]]
    )
    await bot.send_message(chat_id, text, reply_markup=inline_kb)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
