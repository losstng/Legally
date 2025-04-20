from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
import re

# class UserCreate(BaseModel): # field for input for user create # could be outdated
#    name: str
#    age: int
#    email: str
#    password: str
#    role: str = "user"

# class UserResponse(BaseModel): # for registering into database # could be outdated
#    id: int
#    name: str
#    age: int
#    email: str
#    role: str

#    class Config:
#        from_attributes = True

class UserRegister(BaseModel): # used for the user to input to create a user
    name: str = Field(..., min_length= 2, max_length= 50) 
    age: int = Field(..., ge=18, le=120)
    email: EmailStr
    password: str = Field(..., min_length= 6, max_length= 20)
    role: Optional[str] = "user" # standard

    @validator("password")
    def password_musthave_special_char(cls, v): # this is cool
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character.")
        return v #v here stands for value, cls is for the entire pydantic response "class"
                #it searches v with for "password" in cls
                
class UserLogin(BaseModel): # basic
    email: EmailStr
    password: str = Field(..., min_length= 6, max_length= 20)

class OTPVerify(BaseModel): # basic
    email: EmailStr
    otp: str