from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers.messages import notify
from settings import CONFIG, save_config


scheduler = AsyncIOScheduler()
scheduler.add_job(notify, "cron", hour=CONFIG["hour"], minute=CONFIG["minute"])


def update_scheduler(h, m):
    CONFIG["hour"] = h
    CONFIG["minute"] = m
    save_config(CONFIG)

    scheduler.remove_all_jobs()
    scheduler.add_job(notify, "cron", hour=h, minute=m)
