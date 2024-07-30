import asyncio
import logging
import sys

from scheduler import scheduler
from bot import dp, bot
from handlers import messages, callbacks


async def main() -> None:
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
