from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from key import TOKEN, chat_id

from aiogram.types.chat_member_owner import ChatMemberOwner
from aiogram.types.chat_member_administrator import ChatMemberAdministrator
from aiogram.types.chat_member_member import ChatMemberMember
from aiogram.types.chat_member_restricted import ChatMemberRestricted

available = [
    ChatMemberOwner,
    ChatMemberAdministrator,
    ChatMemberMember,
    ChatMemberRestricted,
]

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def user_in_chat(message: types.Message):
    user_id = message.from_user.id
    try:
        member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        return any(isinstance(member, chatmember) for chatmember in available)
    except Exception as e:
        print(e)
        return False


async def user_in_chat_callback(callback):
    user_id = callback.from_user.id
    try:
        member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        return any(isinstance(member, chatmember) for chatmember in available)
    except Exception as e:
        print(e)
        return False
