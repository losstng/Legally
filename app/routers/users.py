from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.db import models
from app.db.database import get_db
from app.schemas.user import UserRegister, UserResponse
from app.utils.security import hash_password, get_current_user

import logging

router = APIRouter()

@router.post("/register", response_model=dict) 
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    
    if db.query(func.count(models.User.id)).scalar() == 0:
        user.role = "admin"

    hashed_pw = hash_password(user.password) #calling hashing user password
    new_user = models.User(
        name=user.name,
        age=user.age,
        email=user.email,
        hashed_password=hashed_pw,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user) #standard stuff
    return {"message": "User registered successfully"}


@router.delete("/{user_id}", response_model=dict)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only!")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")

    db.delete(user)
    db.commit()
    logging.info(f"User deleted: {user.email} by {current_user.email}") #standard logging
    return {"message": "User deleted successfully"}