from aiogram.filters import Command
from aiogram.types import Message
from scheduler import update_scheduler
import re

from tgbot import dp, user_in_chat
from settings import CONFIG, save_config


@dp.message(Command("settime"))
async def set_time(message: Message):
    if not await user_in_chat(message):
        return
    pattern = r"^/settime (\d+):(\d+)$"
    text = message.text

    match = re.match(pattern, text)
    if match:
        x = match.group(1)
        y = match.group(2)
        if int(x) > 23 or int(x) < 0 or int(y) < 0 or int(y) > 59:
            await message.answer("Неверное значение")
            return
        update_scheduler(int(x), int(y))
        await message.answer(f"🕓 Время уведомлений установлено на {x}:{y}")
    else:
        await message.answer(
            "Для установки времени уведомления отправьте сообщение:\n\n/settime x:y\n\nгде «x» часы (в 24 часовом формате), «y» минуты"
        )


@dp.message(Command("setnotify"))
async def set_time(message: Message):
    if not await user_in_chat(message):
        return
    CONFIG["notify"] = not CONFIG["notify"]
    save_config(CONFIG)

    if CONFIG["notify"]:
        await message.answer(
            "🔔 ✅\nУведомления о сообщениях без отклика теперь будут приходить.\nЧтобы изменить отправьте команду еще раз."
        )
    else:
        await message.answer(
            "🔔 ❌\nУведомления о сообщениях без отклика больше не будут приходить.\nЧтобы изменить отправьте команду еще раз."
        )


@dp.message(Command("setweekends"))
async def set_time(message: Message):
    if not await user_in_chat(message):
        return
    CONFIG["skip_weekends"] = not CONFIG["skip_weekends"]
    save_config(CONFIG)

    if CONFIG["skip_weekends"]:
        await message.answer(
            "📆 ❌\nУведомления о сообщениях без отклика теперь не будут приходить в субботу и воскреенье.\nЧтобы изменить отправьте команду еще раз."
        )
    else:
        await message.answer(
            "📆 ✅\nУведомления о сообщениях без отклика теперь будут приходить в субботу и воскресенье.\nЧтобы изменить отправьте команду еще раз."
        )

@dp.message(Command("showsettings"))
async def set_time(message: Message):
    if not await user_in_chat(message):
        return
    await message.answer(
f"""🔔 Уведомления о сообщениях без отклика: {'✅ Включены' if CONFIG['notify'] else '❌ Отключены'}
Для изменения /setnotify
        
🕓 Время уведомления: {CONFIG['hour']}:{CONFIG['minute']}
Для изменения /settime

📆 Уведомления по выходным: {'✅ Включены' if not CONFIG['skip_weekends'] else '❌ Отключены'}
Для изменения /setweekends"""
    )