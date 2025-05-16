from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, Any


class ApiResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    
class HistoryResponseItem(BaseModel):
    id: int
    question: str
    answer: str
    timestamp: datetime

    class Config:
        from_attributes = True