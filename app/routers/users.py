from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.db import models
from app.db.database import get_db
from app.schemas.user import UserRegister, PasswordChangeRequest
from app.schemas.ask import ApiResponse
from app.utils.security import hash_password, get_current_user, verify_password
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
import csv
import io
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

@router.delete("/delete-user", response_model=dict)
def delete_own_account(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")

    db.delete(user)
    db.commit()
    logging.info(f"User self-deleted: {current_user.email}")
    return ApiResponse(success=True, data={"message": "Your account has been deleted."})

@router.post("/change-password", response_model=ApiResponse)
def change_password(
    payload: PasswordChangeRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user or not verify_password(payload.current_password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect current password.")

    user.hashed_password = hash_password(payload.new_password)
    db.commit()
    return ApiResponse(success=True, data={"message": "Password updated successfully."})

@router.get("/export-data", response_class=StreamingResponse)
def export_user_data(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Setup CSV in-memory buffer
    output = io.StringIO()
    writer = csv.writer(output)

    # User Info
    writer.writerow(["User Info"])
    writer.writerow(["ID", current_user.id])
    writer.writerow(["Name", current_user.name])
    writer.writerow(["Email", current_user.email])
    writer.writerow(["Age", current_user.age])
    writer.writerow(["Role", current_user.role])
    writer.writerow([])

    # Chat Sessions
    sessions = db.query(models.ChatSession).filter_by(user_id=current_user.id).all()
    writer.writerow(["Chat Sessions"])
    writer.writerow(["Session ID", "Title", "Created At"])
    for s in sessions:
        writer.writerow([s.id, s.title, s.created_at])
    writer.writerow([])

    # Conversations
    writer.writerow(["Conversations"])
    writer.writerow(["Session ID", "Question", "Answer", "Timestamp"])
    for s in sessions:
        convos = db.query(models.Conversation).filter_by(chat_session_id=s.id).all()
        for c in convos:
            writer.writerow([s.id, c.question, c.full_answer, c.timestamp])
    writer.writerow([])

    # Files
    files = db.query(models.UserFile).filter_by(user_id=current_user.id).all()
    writer.writerow(["Uploaded Files"])
    writer.writerow(["Filename", "Uploaded"])
    for f in files:
        writer.writerow([f.filename, f.upload_time])

    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={
        "Content-Disposition": f"attachment; filename=user_data_{current_user.id}.csv"
    })

@router.get("/me", response_model=ApiResponse)
def get_profile_info(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return ApiResponse(success=True, data={
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "age": current_user.age,
        "role": current_user.role,
    })