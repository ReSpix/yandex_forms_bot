from fastapi import APIRouter, Depends
from models import (
    Request,
    RequestView,
    ResponseType,
    Response,
    TypeView,
    ResponseView
)
from typing import List
from sqlalchemy.orm import Session
from database import get_db

debug_router = APIRouter(prefix='/debug')


@debug_router.get("/requests/", response_model=List[RequestView])
def get_requests(db: Session = Depends(get_db)):
    requests = db.query(Request).all()
    return requests


@debug_router.get("/types/", response_model=List[TypeView])
def get_types(db: Session = Depends(get_db)):
    types = db.query(ResponseType).all()
    return types


@debug_router.get("/responses/", response_model=List[ResponseView])
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
