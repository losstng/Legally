from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from models import UserCreate, UserResponse
import re
#the whole trinity is here

models.Base.metadata.create_all(bind=engine) 
#use the declarative Base basemodel
#get all the metadata from Base *aka the blueprint for the data
#check the existence of users.db and connect to it *refer to database.py

#turn on FastAPI
app = FastAPI()

#open & closing new session for each command
def get_db():
    db = SessionLocal() #refer to database.py
    try:
        yield db
    finally:
        db.close()

#so each @ and def below is a command so that's why multiple threads is ON

#essentially "hey app, a request of creating a user is on, get to this path and what the input is"
@app.post("/users/", response_model=UserResponse) #post is create in CRUD
#"/users/" is the route path, i know the app is not that smart yet, it is still SQLite
#response_model is the return to give to the user after completion

#simply getting the input and then executing the function below, by reading user: UserCreate as the input form

#note that no @app is called in between for this to work

#so this is what being executed to the actual database 
def create_user(user: UserCreate, db: Session = Depends(get_db)):  #getting the UserCreate then opening a session, get_db is a sessionmaker, and depends is like only when there is a command
    existing_user = db.query(models.User).filter(models.User.email == user.email).first() #checking the email first
    if existing_user:
        raise HTTPException(status_code=400, detail="you ain't fucking with me dawg!") #registering error 

    new_user = models.User(name=user.name, age=user.age, email=user.email) #writing out the information from user
    db.add(new_user) #adding to the database
    db.commit() #commitment
    db.refresh(new_user) #refresh to show the newest result because there could be a lag
    return new_user #return the new_user to the @app in JSON then for the app to reformat to UserResponse

#nah im not explaining the rest

@app.get("/users/{user_id}", response_model=UserResponse) #the user_id is dynamic here and is followed by the principles of the *.post
def get_user(user_id: int, db: Session = Depends(get_db)): #note that the user_id is decleared above for the function here
    user = db.query(models.User).filter(models.User.id == user_id).first() #getting the first one
    if not user:
        raise HTTPException(status_code=404, detail=" you sure you got the right one?")
    return user


@app.get("/users/all/", response_model=list[UserResponse]) #getting all of them =))), note that it is now a list of user response
def get_all_users(db: Session = Depends(get_db)): 
    users = db.query(models.User).all() #getting all of them yo
    if not users:
        raise HTTPException(status_code=404, detail="dawg we ain't have shit, come back later yo!")
    return users

@app.get("/users/selected/", response_model=list[UserResponse]) #still returning the list, but like the name now is the SELECTED lol
def get_users(user_ids: str, db: Session = Depends(get_db)): #we don't know if they will give 1, 2, 3 or 1 2 3
    user_id_list = [int(id) for id in re.split(r"[, ]+", user_ids.strip()) if id]  #so we use regular expression to get that convert that shit yo

    users = db.query(models.User).filter(models.User.id.in_(user_id_list)).all() #filtering by the list, typeshit
    if not users:
        raise HTTPException(status_code=404, detail="bro! you sure you got the right one?")
    return users


@app.put("/users/{user_id}", response_model=UserResponse) #okay this is a bit more complex, similar to the individual finding though
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)): #so we have 2 input of user_id and user, the user is to update
    existing_user = db.query(models.User).filter(models.User.id == user_id).first() #checking if that MF exists or not
    if not existing_user:
        raise HTTPException(status_code=404, detail="who you finding bro? whoever it is, they are not in here!")
    
    email_check = db.query(models.User).filter(models.User.email == user.email, models.User.id != user_id).first() 
    #so we check if the new email is taken or not by checking into the database if the email returns an id that is the given id or not, kinda complex but great!
    if email_check:
        raise HTTPException(status_code=400, detail="this email is ALREADY TAKEN BRAHHHHHHH!")

    existing_user.name = user.name
    existing_user.age = user.age
    existing_user.email = user.email
    db.commit()
    db.refresh(existing_user)
    return existing_user


@app.delete("/users/{user_id}") #similar to the one above
def delete_user(user_id: int, db: Session = Depends(get_db)): 
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="who you trying to kill bro?")
    
    db.delete(user) #like this is the important thing of this function here
    db.commit()
    return {"message": "that motherfucker has been dematerialized"}
