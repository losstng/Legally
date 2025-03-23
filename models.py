from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel

class User(Base):
    __tablename__ = "users" #making the of the database, in which for mat it will take place

    id = Column(Integer, primary_key=True, index=True) #the id is the primary_key and unless specified otherwise, will follows the index
    name = Column(String, index=True)
    age = Column(Integer)
    email = Column(String, unique=True, index=True) #unique is important
    hashed_password = Column(String)
    role = Column(String, default="user")  # Role-based access control

#Pydantic models for request validation
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
        from_attributes = True  #ORM mode, for the response from the data base to convert data between a relational database and the temporary memory
