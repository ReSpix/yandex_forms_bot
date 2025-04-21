from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel, field_validator, validator
from datetime import datetime

Base = declarative_base()


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    received_at = Column(DateTime, default=datetime.now, nullable=False)

    responses = relationship("Response", back_populates="ticket")


class ResponseType(Base):
    __tablename__ = "response_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_text = Column(String, nullable=False)
    pretty_text = Column(String, nullable=False)

    responses = relationship("Response", back_populates="response_type")


class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    employee_name = Column(String, nullable=False)
    responded_at = Column(DateTime, default=datetime.now, nullable=False)
    response_type_id = Column(Integer, ForeignKey("response_types.id"), nullable=False)

    ticket = relationship("Ticket", back_populates="responses")
    response_type = relationship("ResponseType", back_populates="responses")


class TicketView(BaseModel):
    id: int
    text: str
    received_at: datetime

    class Config:
        from_attributes = True
        
        
class ResponseView(BaseModel):
    id: int
    request_id: int
    employee_name: str
    responded_at: datetime
    response_type: str

    class Config:
        from_attributes = True

    @field_validator('response_type', mode='before')
    def convert_response_type(cls, value):
        if isinstance(value, ResponseType):
            return value.type_text
        if isinstance(value, TypeView):
            return value.type_text
        return value
        
    
class TypeView(BaseModel):
    id: int
    type_text: str

    class Config:
        from_attributes = True
