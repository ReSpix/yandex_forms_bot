import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import init_db
import logging
from sys import stdout
from api_routes import api_router
from web import web_router
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


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
app.include_router(web_router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/status")
def status():
    return {"Im, ok"}
