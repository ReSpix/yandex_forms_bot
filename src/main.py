import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import init_db
from nats_wrapper import nats_wrapper as nats
import logging
from sys import stdout
from routes import main_router
from bot.main import main as bot_main

logging.basicConfig(level=logging.INFO, stream=stdout,
                    format="[%(levelname)s] %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Начинаю инициализацию")
    init_db()
    asyncio.create_task(bot_main())
    logging.info("Инициализация завершена")
    yield
    await nats.close()


app = FastAPI(lifespan=lifespan)
app.include_router(main_router)


@app.get("/status")
def status():
    return {"Im, ok"}
