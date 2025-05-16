from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.db import models
from app.db.database import get_db
from app.schemas.user import UserRegister, PasswordChangeRequest, EmailRequest
from app.schemas.ask import ApiResponse
from app.utils.security import hash_password, get_current_user, verify_password
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
from app.utils.redis import redis_client
from app.utils.email_service import send_otp_email
import csv
import io
import random
load_dotenv()

import logging

def generate_otp(): #standard generation 
    return str(random.randint(100000, 999999))

def store_otp(email, otp): 
    redis_client.setex(f"otp:{email}", 300, otp) # caching and set expiry, leveraging redis
    
def verify_otp(email, otp_input):  #another function
    saved_otp = redis_client.get(f"otp:{email}")
    if not saved_otp:
        return "OTP expired or not found, tough luck!"
    return "OTP verified" if saved_otp == otp_input else "Invalid OTP" # simple stuff

router = APIRouter() # again establishing routers

@router.post("/register", response_model=ApiResponse)
def register(user: UserRegister, db: Session = Depends(get_db)):
    print("Incoming user:", user.dict())  # Add this
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    # Assign admin if first user
    if db.query(func.count(models.User.id)).scalar() == 0:
        user.role = "admin"

    hashed_pw = hash_password(user.password)
    new_user = models.User(
        name=user.name,
        age=user.age,
        email=user.email,
        hashed_password=hashed_pw,
        role=user.role or "user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return ApiResponse(success=True, data={"message": "User registered successfully"})

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
    return ApiResponse(success=True, data={"message": "User deleted"})

@router.post("/request-password-change", response_model=ApiResponse)
def request_password_change(
    payload: PasswordChangeRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user or not verify_password(payload.current_password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect current password.")

    # Generate OTP
    otp = generate_otp()
    store_otp(user.email, otp)

    # Temporarily store new password in Redis (or pass as query param if minimal risk)
    redis_client.setex(f"pending_password:{user.email}", 300, hash_password(payload.new_password))

    # Send OTP
    send_otp_email(user.email, otp)

    return ApiResponse(success=True, data={"email": user.email, "message": "OTP sent to confirm password change."})

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

@router.post("/request-delete", response_model=ApiResponse)
def request_account_deletion(payload: EmailRequest, db: Session = Depends(get_db)):
    email = payload.email
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="No user with this email.")

    otp = generate_otp()
    store_otp(email, otp)
    send_otp_email(email, otp)

    return ApiResponse(success=True, data={"message": f"OTP sent to {email} for account deletion confirmation."})