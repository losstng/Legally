import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from database import SessionLocal
from sqlalchemy.orm import Session
import models

#Secret key for JWT encryption
SECRET_KEY = "your-secret-key" #the key =)))
ALGORITHM = "HS256" #what is the algorithm of the token
ACCESS_TOKEN_EXPIRE_MINUTES = 1  #Token valid for 1 minute

#Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #in which way to has the key and notify when it is outdated

def hash_password(password: str):
    return pwd_context.hash(password) #execute the input password

def verify_password(plain_password, hashed_password): #will be used later
    return pwd_context.verify(plain_password, hashed_password) #verifying the password given and the password in the database

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy() #data from the temporary dictionary
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) #when to expire
    to_encode.update({"exp": expire}) #adding that expire time onto the token
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) #so the JSON Web Token has first the updated expiration time and the data, then the key based on the secret we have =)), and then the algorithm to cryptographically encrypt the signature

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") #a dependency that tells FastAPI how to extract the JWT token from incoming requests for protected routes. and is where the client should send their credentials to get the token

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
