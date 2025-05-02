from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.database import Base
from sqlalchemy.orm import relationship

class User(Base): # table for user
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")
    files = relationship("UserFile", back_populates="user", cascade="all, delete") 
    # relationship here is important, it is regarding object relationship management, like keys
    # name of the related model, bi-directional relationship for the "user" attribute, 
                # controls how related objects behave when the parent is updated or deleted
class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True) # primary key, standard stuff
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) #fogreign key that postgresql has to parse and find themself
    chat_session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=True)
    question = Column(Text, nullable=False)
    base_answer = Column(Text, nullable=False) #nullable is essentialy cannot be empty
    full_answer = Column(Text, nullable=False) #nullable is essentialy cannot be empty
    timestamp = Column(DateTime(timezone=True), server_default=func.now()) #default of where the server is located right now.
    chat_session = relationship("Chatsession", back_populates="qna_entries")

class UserFile(Base):
    __tablename__ = "user_files" # standard stuff

    id = Column(Integer, primary_key=True, index=True) # still standard
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE")) 
    # it is column of integer that uses the foreign key of the model "users" 
    # and when that key is deleted, use the cascade defined on that foreign key 
    file_key = Column(String, unique=True, nullable=False) # standard
    filename = Column(String, nullable=False) # standard
    file_path = Column(String, nullable=False) # standard
    upload_time = Column(DateTime(timezone=True), server_default=func.now()) # standard

    user = relationship("User", back_populates="files") # establishes a relationship 
    # the corresponder to what we saw in the first model, without this, the other wouldn't have worked

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    qna_entries = relationship("Conversation", back_populates="chat_session", cascade="all, delete-orphan")