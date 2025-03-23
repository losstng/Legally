from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "sqlite:///./users.db" #setting up the file


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) #creating the engine to be use to connect tot he database


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #creating that single session for each request


Base = declarative_base() #the base is always to be declared later
