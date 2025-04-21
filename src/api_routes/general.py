import asyncio
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from models import (
    Ticket,
    TicketView,
    Response
)
from database import get_db
from typing import List
import logging
from asana_helper import publish_asana_task
from bot.main import send_message
from core import on_new_response, get_notify

general_router = APIRouter()


@general_router.get("/receive/{text}")
async def receive(text: str, db: Session = Depends(get_db)):
    logging.info(
        "Получены данные:\n--------Начало--------\n%s\n--------Конец--------", text)
    new_request = Ticket(text=text)
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    asyncio.create_task(export(text))

    return {"Received succesfully"}


async def export(text: str):
    await asyncio.gather(
        send_message(text),
        publish_asana_task(text)
    )


@general_router.get("/response/{text}/{name}/{response_type_text}")
def save_response(
    text: str, name: str, response_type_text: str
):
    return on_new_response(text, name, response_type_text)


@general_router.get("/notify/", response_model=List[TicketView])
def get_requests(db: Session = Depends(get_db)):
    return get_notify()
