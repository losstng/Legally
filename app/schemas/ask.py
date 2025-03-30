from pydantic import BaseModel
from datetime import datetime

class AskRequest(BaseModel):
    question: str

class QAResponse(BaseModel):
    id: int
    question: str
    answer: str

    class Config:
        from_attributes = True #attributes extraction

class AskResponse(BaseModel):
    question: str
    answer: str

class HistoryResponseItem(BaseModel):
    id: int
    question: str
    answer: str
    timestamp: datetime

    class Config:
        from_attributes = True
