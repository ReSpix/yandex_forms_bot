from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers.messages import notify


async def notify_scedule():
    await notify(None)


scheduler = AsyncIOScheduler()
scheduler.add_job(notify_scedule, "cron", hour=9, minute=30)
