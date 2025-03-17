from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.sql import func
from database import Base, DATABASE_URL
from pydantic import BaseModel, EmailStr, Field

#we getting that table yo!
class User(Base): #Base is in database.py
    __tablename__ = "users" #the table name yo

    id = Column(Integer, primary_key=True, index=True) #standard stuff, still using standard index key though
    name = Column(Text, index=True)  #longer names idk but we will limit it later
    age = Column(Integer) 
    email = Column(String, unique=True, index=True) #like we can't allow mf to create accounts on us yo
    created_at = Column(String, default=func.now())  #chat told me to get this

#the basemodel for user to update *it is without id 
class UserCreate(BaseModel): 
    name: str = Field(..., min_length=2, max_length=50, example="John Doe") #yea we limit it here
    age: int = Field(..., ge=18, le=100, example=25)  # Restricts age between 18-100
    email: EmailStr = Field(..., example="user@example.com") #standard stuff, the unique checking is above and in main.py
#we have examples and shit

#the basemodel for computer to return *with id
class UserResponse(BaseModel): #mostly returning shit, similar to the ones above
    id: int
    name: str
    age: int
    email: EmailStr
    created_at: str  #timestamp

    class Config:
        from_attributes = True  #replaces `orm_mode = True` and convert from the pydantic to JSON for the API

#just letting the user know
print(f"✅ Database connected: {DATABASE_URL}")
