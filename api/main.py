from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import Request, RequestResponse
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


@app.get("/requests/", response_model=List[RequestResponse])
def get_requests(db: Session = Depends(get_db)):
    requests = db.query(Request).all()
    return requests
