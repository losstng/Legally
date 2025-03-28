from fastapi import FastAPI, Depends, HTTPException, Request, Security
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from database import SessionLocal, engine
import models
from models import UserCreate, UserResponse
from security import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from email_service import send_otp_email
from pydantic import BaseModel
from typing import Optional
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import random, time
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse
import logging
#the whole trinity


#uvicorn main:app --reload
#Uvicorn is a lightning-fast ASGI server (Asynchronous Server Gateway Interface) used to run FastAPI apps.


# logging the time, name, and what happened
logging.basicConfig(level=logging.INFO, filename="app.log", format="%(asctime)s - %(levelname)s - %(message)s")

#starting the engine
models.Base.metadata.create_all(bind=engine) 

#declearing the app, and limit the amount of access at the time
app = FastAPI()
limiter = Limiter(key_func=get_remote_address) #where is that address is and tracking them
app.state.limiter = limiter

#help with simplifying the process of limit of failed attempts
@app.exception_handler(RateLimitExceeded)
def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Too many requests! Slow down bro!"}) #JSONResponse to be later convert in the GUI


# Open & closing session
def get_db():
    db = SessionLocal() #a local for that single command or thread
    try:
        yield db
    finally:
        db.close()

class UserRegister(BaseModel): #the model for userregister:
    name: str
    age: int
    email: str
    password: str
    role: Optional[str] = "user"


class UserLogin(BaseModel): #what to expect from the user when they are asked to log in
    email: str
    password: str

class OTPVerify(BaseModel): #the email address and otp
    email: str
    otp: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False) #verifying the token, used after login

# OTP Storage, especially during that time
otp_store = {}

def generate_otp(): #randomly generating that OTP
    return str(random.randint(100000, 999999))

def store_otp(email, otp): #then this program is to store with time on it so the time can be tracked
    otp_store[email] = {"otp": otp, "timestamp": time.time()}

def verify_otp(email, user_input_otp): #verifying that shit
    if email in otp_store: #checking first the email
        saved_otp = otp_store[email]["otp"] #defining variables to use later
        timestamp = otp_store[email]["timestamp"] #
        if user_input_otp == saved_otp: 
            if time.time() - timestamp > 300: #checking the time
                return "OTP expired!" #no
            return "OTP verified!" #yes
        return "Invalid OTP!" #correct email but no OTP
    return "No OTP found!" #incorrect email

# Authentication & Authorization

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)): #defining the function to check the user data using the token
    credentials_exception = HTTPException(status_code=401, detail="Invalid credentials") #user doesn't exist or the token isn't in there
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #checking the payload 
        email = payload.get("sub") #checking if the email is in the token or not
        if email is None:
            raise credentials_exception 
        user = db.query(models.User).filter(models.User.email == email).first() #if the email is vaid then find the user by email
        if user is None:
            raise credentials_exception 
        return user #returning the userinfo
    except JWTError:
        raise credentials_exception #invalid anything then this

@app.get("/")
def read_root():
    return {"message": "Backend is live!"}

@app.post("/login/") #logging in
@limiter.limit("5/minute") #5 times per minute from that address
def login(request: Request, user: UserLogin, db: Session = Depends(get_db)): #defining as request for limiter | defining the user form for the user to log in | getting the session
    db_user = db.query(models.User).filter(models.User.email == user.email).first() #opening session and checking the email
    if not db_user or not verify_password(user.password, db_user.hashed_password): #checking the password matches with the hashed_password or not
        logging.warning(f"Failed login attempt: {user.email}") #logging 
        raise HTTPException(status_code=400, detail="Invalid credentials")
    otp = generate_otp() #generate the otp
    store_otp(user.email, otp)
    send_otp_email(user.email, otp)
    return {"message": "OTP sent! Please verify to get your token."}

@app.post("/verify-otp/") # verify the OTP to get the token
def verify_otp_route(otp_data: OTPVerify, db: Session = Depends(get_db)): #otp data is a class from OTPVerify above
    result = verify_otp(otp_data.email, otp_data.otp) #get the 2 things that are in the otp data
    if result == "OTP verified!": #getting the result from the function above
        access_token = create_access_token(data={"sub": otp_data.email}, expires_delta=timedelta(minutes=5)) #get access token, first data is the email and the expiration time is 1 min
        return {"access_token": access_token, "token_type": "bearer"} #giving the access_token throught the fuction and giving the token type
    raise HTTPException(status_code=400, detail=result) #the result has been defined before

@app.post("/register/")
def register(user: UserRegister, db: Session = Depends(get_db)):
    user_count = db.query(func.count(models.User.id)).scalar()
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    if user_count == 0:
        user.role = "admin"

    hashed_password = hash_password(user.password) #hashing the regester password
    new_user = models.User(name=user.name, age=user.age, email=user.email, hashed_password=hashed_password, role=user.role) #defining everying for the database
    db.add(new_user) #adding into the database
    db.commit() #commit with autoflush disabled
    db.refresh(new_user) #refresh in the database
    #logging.info(f"User registered: {new_user.email} by {current_user.email}") #again loggin the information
    return {"message": "User registered successfully"} 


@app.delete("/users/{user_id}") #delete
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)): #samething as before but now expecting only the user ID
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only!")
    user = db.query(models.User).filter(models.User.id == user_id).first() #get the desired user
    if not user:
        raise HTTPException(status_code=404, detail="User not found!") 
    logging.info(f"User deleted: {user.email} by {current_user.email}") #logging the message
    db.delete(user) #the simple action of deleting
    db.commit()
    return {"message": "User deleted successfully"}
