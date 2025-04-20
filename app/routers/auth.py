from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta
from jose import JWTError, jwt
from app.db.database import get_db
from app.db import models
from app.schemas.user import UserRegister, UserLogin, OTPVerify
from app.schemas.ask import ApiResponse
from app.utils.security import hash_password, verify_password, create_access_token, create_refresh_token, SECRET_KEY, ALGORITHM
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


@router.post("/verify-otp") # to get the token * no limiter
async def verify_otp_route(otp_data: OTPVerify, db: Session = Depends(get_db)):
    result = verify_otp(otp_data.email, otp_data.otp)
    if result == "OTP verified": # this has been predefined
        user = db.query(models.User).filter(models.User.email == otp_data.email).first() # getting this data for later attributes usage
        access_token = create_access_token(data={"email": otp_data.email, "role": user.role}, expires_delta=timedelta(minutes=5)) # encoding multiple data
        refresh_token = create_refresh_token(data={"email": otp_data.email}) # encoding less data
        return ApiResponse(success=True, data={ # message under JSON
            "access_token": access_token, # short term
            "refresh_token": refresh_token, # multiple, longer validity
            "token_type": "bearer"
        }) #these will be returned in JSON and therefore can be used for later, however these 2 lazter must be separated
    raise HTTPException(status_code=400, detail=result) 
    return ApiResponse(success=False, error=result)

# these 2 requires further review

@router.post("/refresh-token") # for refresh topen
async def refresh_token_route(token: str = Depends(oauth2_scheme)): # again authenitcating the token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=400, detail="Invalid token type.")
        email = payload.get("sub")
        new_access_token = create_access_token(data={"email": email, "role": payload.get("role")})
        return ApiResponse(success=True, data={"access_token": new_access_token, "token_type": "bearer"})
    except JWTError:
        return ApiResponse(success=True, data={"message": "OTP sent! Please verify to get your token."})