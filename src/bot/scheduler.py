from .settings import CONFIG, save_config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .reminders import notify_scheduler


scheduler = AsyncIOScheduler()


def update_scheduler(h, m):
    CONFIG["hour"] = h
    CONFIG["minute"] = m
    save_config(CONFIG)

    scheduler.remove_all_jobs()
    scheduler.add_job(notify_scheduler, "cron", hour=h, minute=m)


def activate_scheduler():
    scheduler.add_job(
        notify_scheduler, "cron", hour=CONFIG["hour"], minute=CONFIG["minute"])
    scheduler.start()
