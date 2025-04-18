from fastapi import BackgroundTasks, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session, aliased
from models import (
    Request,
    RequestView,
    Response
)
from database import get_db
from typing import List
import logging
from asana_helper import publish_asana_task
from core import on_new_response, get_notify

general_router = APIRouter()


@general_router.get("/receive/{text}")
async def receive(text: str, db: Session = Depends(get_db)):
    logging.info(
        "Получены данные:\n--------Начало--------\n%s\n--------Конец--------", text)
    new_request = Request(text=text)
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    publish_asana_task(text)

    return {"Received succesfully"}


@general_router.get("/response/{text}/{name}/{response_type_text}")
def save_response(
    text: str, name: str, response_type_text: str
):
    return on_new_response(text, name, response_type_text)


@general_router.get("/notify/", response_model=List[RequestView])
def get_requests(db: Session = Depends(get_db)):
    return get_notify()
