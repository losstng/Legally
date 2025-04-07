from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
import re

class UserCreate(BaseModel):
    name: str
    age: int
    email: str
    password: str
    role: str = "user"

class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    email: str
    role: str

    class Config:
        from_attributes = True

class UserRegister(BaseModel):
    name: str = Field(..., min_length= 2, max_length= 50)
    age: int = Field(..., ge=18, le=120)
    email: EmailStr
    password: str = Field(..., min_length= 6, max_length= 20)
    role: Optional[str] = "user"

    @validator("password")
    def password_musthave_special_char(cls, v):
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character.")
        return v #v here stands for value, cls is for the entire pydantic response
                #it searches v with for "password"
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length= 6, max_length= 20)

class OTPVerify(BaseModel):
    email: EmailStr
    otp: str