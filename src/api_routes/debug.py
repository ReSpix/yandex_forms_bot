import json
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response as fa_Response
from models import (
    Ticket,
    TicketView,
    ResponseType,
    Response,
    TypeView,
    ResponseView
)
from typing import List
from sqlalchemy.orm import Session
from database import get_db

debug_router = APIRouter(prefix='/debug')


@debug_router.get("/requests/", response_model=List[TicketView])
def get_requests(db: Session = Depends(get_db)):
    requests = db.query(Ticket).all()
    return pretty_format(requests, TicketView)


@debug_router.get("/types/", response_model=List[TypeView])
def get_types(db: Session = Depends(get_db)):
    types = db.query(ResponseType).all()
    return pretty_format(types, TypeView)


@debug_router.get("/responses/", response_model=List[ResponseView])
def get_responses(db: Session = Depends(get_db)):
    responses = db.query(Response).join(ResponseType).all()
    return pretty_format(responses, ResponseView)


def pretty_format(content, cls):
    output = [cls.model_validate(out) for out in content]
    encoded = jsonable_encoder(output)
    pretty_json = json.dumps(encoded, indent=4, ensure_ascii=False)
    return fa_Response(content=pretty_json, media_type="application/json")
