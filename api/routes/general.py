from fastapi import BackgroundTasks, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session, aliased
from models import (
    Request,
    RequestView,
    ResponseType,
    Response
)
from database import get_db
from typing import List
from nats_wrapper import nats_wrapper as nats
import logging

general_router = APIRouter()


@general_router.get("/receive/{text}")
async def receive(text: str, db: Session = Depends(get_db), background_tasks : BackgroundTasks = BackgroundTasks()):
    logging.info(
        "Получены данные:\n--------Начало--------\n%s\n--------Конец--------", text)
    new_request = Request(text=text)
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    background_tasks.add_task(nats.publish, text)

    return {"Received succesfully"}


@general_router.get("/response/{text}/{name}/{response_type_text}")
def save_response(
    text: str, name: str, response_type_text: str, db: Session = Depends(get_db)
):
    request = db.query(Request).filter(Request.text == text).first()

    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    response_type = (
        db.query(ResponseType)
        .filter(ResponseType.type_text == response_type_text)
        .first()
    )

    if not response_type:
        raise HTTPException(status_code=404, detail="Response type not found")

    new_response = Response(
        request_id=request.id, employee_name=name, response_type_id=response_type.id
    )
    db.add(new_response)
    db.commit()
    db.refresh(new_response)
    return {"Response saved"}


@general_router.get("/notify/", response_model=List[RequestView])
def get_requests(db: Session = Depends(get_db)):
    response_alias = aliased(Response)

    requests = (
        db.query(Request)
        .outerjoin(response_alias, Request.id == response_alias.request_id)
        .filter(response_alias.id.is_(None))
        .all()
    )
    return requests
