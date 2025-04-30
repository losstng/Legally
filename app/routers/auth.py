from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta
from jose import JWTError, jwt
from app.db.database import get_db
from app.db import models
from app.schemas.user import UserRegister, UserLogin, OTPVerify, EmailOnly, PasswordReset
from app.schemas.ask import ApiResponse
from app.utils.security import hash_password, verify_password, create_refresh_token, SECRET_KEY, ALGORITHM
from app.utils.email_service import send_otp_email
from app.utils.limiter import limiter
import random, time
from app.utils.redis import redis_client
from dotenv import load_dotenv
load_dotenv()
# importing some stuff for the essential authentication process



router = APIRouter() # establish the router to main.py
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False) # later used for token
# get the token & a falseback system

# otp handling and stuff, all can be left here, neatly
def generate_otp(): #standard generation 
    return str(random.randint(100000, 999999))

def store_otp(email, otp): 
    redis_client.setex(f"otp:{email}", 300, otp) # caching and set expiry, leveraging redis
    
def verify_otp(email, otp_input):  #another function
    saved_otp = redis_client.get(f"otp:{email}")
    if not saved_otp:
        return "OTP expired or not found, tough luck!"
    return "OTP verified" if saved_otp == otp_input else "Invalid OTP" # simple stuff

# --- ROUTES --- as defined in main.py

@router.post("/register") # the route
async def register(user: UserRegister, db: Session = Depends(get_db)): # async function
    if db.query(models.User).filter(models.User.email == user.email).first(): # check email 
        raise HTTPException(status_code=400, detail="Email already registered.") # availability

    user.role = "admin" if db.query(models.User).count() == 0 else "user" #default role for 1st user
    hashed_pw = hash_password(user.password) #hashing the password

    new_user = models.User(
        name=user.name,
        age=user.age,
        email=user.email,
        hashed_password=hashed_pw,
        role=user.role
    ) #creating a class within to be then apply in the database

    db.add(new_user)
    db.commit()
    db.refresh(new_user) #connecting to
    return ApiResponse(success=True, data={"message": "User registered successfully"}) # ApiResponse again


@router.post("/login")
@limiter.limit("5/minute") # 5 times per minute 
async def login(request: Request, user: UserLogin, db: Session = Depends(get_db)): #same with normal @app but with async in whihc it will be sorted more efficiently
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password): # checking both gmail & password
        raise HTTPException(status_code=400, detail="Invalid credentials") # will not know which is wrong

    otp = generate_otp()
    store_otp(user.email, otp) # standard
    send_otp_email(user.email, otp) # standard
    return ApiResponse(success=True, data={"message": "OTP sent! Please verify to get your token."}) # advanced security stuff


@router.post("/verify-otp")
async def verify_otp_route(otp_data: OTPVerify, db: Session = Depends(get_db)):
    result = verify_otp(otp_data.email, otp_data.otp)
    if result != "OTP verified":
        raise HTTPException(status_code=400, detail=result)

    user = db.query(models.User).filter(models.User.email == otp_data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    refresh_token = create_refresh_token(
        data={"email": otp_data.email, "role": user.role},
        expires_delta=timedelta(hours=24)
    )

    return ApiResponse(success=True, data={
        "refresh_token": refresh_token,
        "token_type": "bearer"
    })

@router.post("/forgot-password")
async def forgot_password(user: EmailOnly, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Email not found")

    otp = generate_otp()
    store_otp(user.email, otp)
    send_otp_email(user.email, otp)

    return ApiResponse(success=True, data={"message": "OTP sent to email for password reset"})

from app.schemas.user import PasswordReset

@router.post("/reset-password")
async def reset_password(payload: PasswordReset, db: Session = Depends(get_db)):
    # Step 1: Verify OTP
    result = verify_otp(payload.email, payload.otp)
    if result != "OTP verified":
        raise HTTPException(status_code=400, detail=result)

    # Step 2: Find user
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Step 3: Hash and update password
    user.hashed_password = hash_password(payload.new_password)
    db.commit()

    return ApiResponse(success=True, data={"message": "Password has been reset successfully."})