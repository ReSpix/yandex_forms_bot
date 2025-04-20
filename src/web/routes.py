from fastapi.routing import APIRouter
from fastapi import APIRouter, Request as fa_Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, aliased
from sqlalchemy import desc, func, select
from database import SessionLocal
import logging
from models import (
    Request,
    ResponseType,
    Response
)

web_router = APIRouter()
templates = Jinja2Templates(directory="web/templates")


@web_router.get("/", response_class=HTMLResponse)
async def index(request: fa_Request):
    db = SessionLocal()
    last_response_subquery = (
        select(
            Response.id.label("response_id"),
            Response.request_id,
            Response.employee_name,
            Response.responded_at,
            Response.response_type_id,
            func.row_number().over(
                partition_by=Response.request_id,
                order_by=Response.responded_at.desc()
            ).label("rn")
        ).subquery()
    )

    # Алиасы
    last_response_alias = aliased(Response, last_response_subquery)
    response_type_alias = aliased(ResponseType)

    # Основной запрос: Request + последний Response + ResponseType
    query = (
        select(Request, last_response_alias, response_type_alias)
        .outerjoin(
            last_response_alias,
            (last_response_subquery.c.request_id == Request.id) &
            (last_response_subquery.c.rn == 1)
        )
        .outerjoin(
            response_type_alias,
            response_type_alias.id == last_response_subquery.c.response_type_id
        )
    )

    # Выполнение запроса
    results = db.execute(query).all()
    # logging.info(results)

    # results = db.query(Request).all()
    db.close()
    return templates.TemplateResponse("index.html", {"request": request, "tickets": results})
