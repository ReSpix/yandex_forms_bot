from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, aliased
from models import (
    Request,
    RequestView,
    ResponseType,
    Response,
    ResponseView,
    TypeView,
)
from database import get_db, init_db
from typing import List

init_db()
app = FastAPI()


@app.get("/status")
def status():
    return {"Im, ok"}


@app.get("/receive/{text}")
def receive(text: str, db: Session = Depends(get_db)):
    print("RECEIVED:\n", text)
    new_request = Request(text=text)
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return {"Received succesfully"}


@app.get("/response/{text}/{name}/{response_type_text}")
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


@app.get("/notify/", response_model=List[RequestView])
def get_requests(db: Session = Depends(get_db)):
    response_alias = aliased(Response)

    requests = (
        db.query(Request)
        .outerjoin(response_alias, Request.id == response_alias.request_id)
        .filter(response_alias.id.is_(None))
        .all()
    )
    return requests


# -------------------------------------------------------------------------------------------
#
#
#
#
# DEBUG VIEWS
#
#
#
# -------------------------------------------------------------------------------------------
@app.get("/requests/", response_model=List[RequestView])
def get_requests(db: Session = Depends(get_db)):
    requests = db.query(Request).all()
    return requests


@app.get("/types/", response_model=List[TypeView])
def get_requests(db: Session = Depends(get_db)):
    types = db.query(ResponseType).all()
    return types


@app.get("/responses/", response_model=List[ResponseView])
def get_responses(db: Session = Depends(get_db)):
    responses = db.query(Response).join(ResponseType).all()
    return [
        ResponseView(
            id=response.id,
            request_id=response.request_id,
            employee_name=response.employee_name,
            responded_at=response.responded_at,
            response_type=response.response_type.type_text,
        )
        for response in responses
    ]
