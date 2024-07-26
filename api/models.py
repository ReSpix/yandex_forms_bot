from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel
from datetime import datetime

Base = declarative_base()


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    received_at = Column(DateTime, default=datetime.now, nullable=False)

    responses = relationship("Response", back_populates="request")


class ResponseType(Base):
    __tablename__ = "response_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_text = Column(String, nullable=False)

    responses = relationship("Response", back_populates="response_type")


class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(Integer, ForeignKey("requests.id"), nullable=False)
    employee_name = Column(String, nullable=False)
    responded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    response_type_id = Column(Integer, ForeignKey("response_types.id"), nullable=False)

    request = relationship("Request", back_populates="responses")
    response_type = relationship("ResponseType", back_populates="responses")


class RequestResponse(BaseModel):
    id: int
    text: str
    received_at: datetime

    class Config:
        orm_mode = True
        
        
class ResponseResponse(BaseModel):
    id: int
    request_id: int
    employee_name: str
    responded_at: datetime
    response_type: str

    class Config:
        orm_mode = True
        
    
class TypeResponse(BaseModel):
    id: int
    type_text: str

    class Config:
        orm_mode = True
