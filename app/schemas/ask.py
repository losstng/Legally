from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, Any


class ApiResponse(BaseModel): # future-proofed for frontend
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None