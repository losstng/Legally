from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.db import models
from app.db.database import get_db
from app.schemas.user import UserRegister
from app.schemas.ask import ApiResponse
from app.utils.security import hash_password, get_current_user
from dotenv import load_dotenv
load_dotenv()

import logging

router = APIRouter() # again establishing routers

#@router.post("/register", response_model=dict)  # in dictionary to register, * due for a review
#def register(user: UserRegister, db: Session = Depends(get_db)):
#    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
#    if existing_user:
#        raise HTTPException(status_code=400, detail="Email already registered.") # checking emal
    
#    if db.query(func.count(models.User.id)).scalar() == 0:
#        user.role = "admin" # counting

#    hashed_pw = hash_password(user.password) #calling hashing user password
#    new_user = models.User(
#        name=user.name,
#        age=user.age,
#        email=user.email,
#        hashed_password=hashed_pw,
#        role=user.role
#    )
# THIS IS REDUNDANT AND WILL SOON BE UPDATED
#    db.add(new_user)
#    db.commit()
#    db.refresh(new_user) #standard stuff
#    return ApiResponse(success=True, data={"message": "User registered successfully"})


@router.delete("/{user_id}", response_model=dict) # good 
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # checking the role
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only!") # getting the attributes

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")

    db.delete(user)
    db.commit()
    logging.info(f"User deleted: {user.email} by {current_user.email}") #standard logging
    return ApiResponse(success=True, data={"message": "User deleted successfully"})