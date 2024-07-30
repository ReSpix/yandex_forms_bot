from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers.messages import notify
from settings import CONFIG


async def notify_scedule():
    await notify(None)


scheduler = AsyncIOScheduler()
scheduler.add_job(notify_scedule, "cron", hour=CONFIG["hour"], minute=CONFIG["minute"])
