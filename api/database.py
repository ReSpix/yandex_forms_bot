from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import ResponseType

DATABASE_URL = "sqlite:///./db/support.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    from models import Base

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        initialize_response_types(db)
    finally:
        db.close()


def initialize_response_types(db):
    response_types = ["work", "call", "accept", "refuse"]
    existing_types = db.query(ResponseType).count()
    if existing_types == 0:
        for type_text in response_types:
            response_type = ResponseType(type_text=type_text)
            db.add(response_type)
        db.commit()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
