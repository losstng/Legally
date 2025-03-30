import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.db.database import SessionLocal, get_db
from sqlalchemy.orm import Session
import app.db.models as models
import os
from dotenv import load_dotenv
load_dotenv()

#Secret key for JWT encryption
SECRET_KEY = os.getenv("SECRET_KEY") #the key =)))
ALGORITHM = os.getenv("ALGORITHM") #what is the algorithm of the token
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1))  #Token valid for 1 minute
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 1440))
#Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #in which way to has the key and notify when it is outdated

def hash_password(password: str):
    return pwd_context.hash(password) #execute the input password

def verify_password(plain_password, hashed_password): #will be used later
    return pwd_context.verify(plain_password, hashed_password) #verifying the password given and the password in the database

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy() #data from the temporary dictionary
    to_encode.update({
    "sub": data.get("email"),
    "role": data.get("role"),
    "iat": datetime.utcnow(),
    "iss": "immigration.app",
}) #adding that expire time onto the token
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) #so the JSON Web Token has first the updated expiration time and the data, then the key based on the secret we have =)), and then the algorithm to cryptographically encrypt the signature

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp": expire,
        "sub": data.get("email"),
        "type": "refresh",
        "iat": datetime.utcnow(),
        "iss": "immigration.app"
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") #a dependency that tells FastAPI how to extract the JWT token from incoming requests for protected routes. and is where the client should send their credentials to get the token


#another session

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)): #the dependency to read the token and opening session to the DB
    credentials_exception = HTTPException(status_code=401, detail="Invalid credentials") 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub") #getting the email from the payload or the data | sub stands for subject—that is, the identity the token is about
        if email is None: 
            raise credentials_exception
        user = db.query(models.User).filter(models.User.email == email).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception
