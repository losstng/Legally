from pydantic import BaseModel
from typing import Optional

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
    name: str
    age: int
    email: str
    password: str
    role: Optional[str] = "user"

class UserLogin(BaseModel):
    email: str
    password: str

class OTPVerify(BaseModel):
    email: str
    otp: str