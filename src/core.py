from fastapi import HTTPException
from sqlalchemy.orm import aliased
from models import (
    Ticket,
    ResponseType,
    Response
)
from database import get_db, SessionLocal

def on_new_response(
    text: str, name: str, response_type_text: str,
):
    db = SessionLocal()
    request = db.query(Ticket).filter(Ticket.text == text).first()

    if not request:
        # TODO: создавать request
        raise HTTPException(status_code=404, detail="Request not found")

    response_type = (
        db.query(ResponseType)
        .filter(ResponseType.type_text == response_type_text)
        .first()
    )

    if not response_type:
        raise ValueError("Response type not found")

    new_response = Response(
        ticket_id=request.id, employee_name=name, response_type_id=response_type.id
    )
    db.add(new_response)
    db.commit()
    db.refresh(new_response)
    return {"Response saved"}

def get_notify():
    db = SessionLocal()
    response_alias = aliased(Response)

    requests = (
        db.query(Ticket)
        .outerjoin(response_alias, Ticket.id == response_alias.ticket_id)
        .filter(response_alias.id.is_(None))
        .all()
    )
    return requests