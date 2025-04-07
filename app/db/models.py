from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) #fogreign key that postgresql has to parse and find themself
    question = Column(Text, nullable=False)
    base_answer = Column(Text, nullable=False) #nullable is essentialy cannot be empty
    full_answer = Column(Text, nullable=False) #nullable is essentialy cannot be empty
    timestamp = Column(DateTime(timezone=True), server_default=func.now()) #default of where the server is located right now.