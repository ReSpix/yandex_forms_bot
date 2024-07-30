import asyncio
import logging
import sys

from scheduler import scheduler
from tgbot import dp, bot
from handlers import messages, callbacks, updates


async def main() -> None:
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
