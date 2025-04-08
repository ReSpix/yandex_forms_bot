import asyncio
import logging
import sys

from scheduler import activate_scheduler
from tgbot import dp, bot
import handlers


async def main() -> None:
    activate_scheduler()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
