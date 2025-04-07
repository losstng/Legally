from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, description="question unfortunately cannot be empty")
#field is like an extension with armor and plate for str
class QAResponse(BaseModel):
    id: int
    question: str
    answer: str

    class Config:
        from_attributes = True #attributes extraction from a class of pydantic

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
