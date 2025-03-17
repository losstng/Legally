import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#so before we didn't have OS 
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #use OS to find from Relative to Absolute 
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'users.db')}" #paste that OS Absolute finding function here to automate the process, but we still need to define the file name though


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) #creating or rather firing up the engine, allowing multiple threads to happen as once as well *thread is like any command

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #creating small commands to the engine, this will be used in main
#autocommit - we don't want to the computer to commit upon it self while the user is still typing no?
#autoflush - even with autocomit off we still want to have another safety measure
#essentially nothing happens before db.execute()
#binding that engine from before

#the base is to be declared
Base = declarative_base()

#just letting the user know
print(f"✅ Database connected: {DATABASE_URL}")
