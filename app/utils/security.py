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
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 1440))
#Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #in which way to has the key and notify when it is outdated

def hash_password(password: str):
    return pwd_context.hash(password) #execute the input password

def verify_password(plain_password, hashed_password): #will be used later
    return pwd_context.verify(plain_password, hashed_password) #verifying the password given and the password in the database

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES) #time delta is like setting the time
    to_encode.update({
        "exp": expire,
        "sub": data.get("email"),
        "type": "refresh",
        "iat": datetime.utcnow(),
        "iss": "immigration.app"
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login") 
#a parser + validator for authentication header
# tell fastapit to expect a bearer token in 'bear <access_token>
#create a dependency that can be injectted 

#another session and decrypting the token, taking from the token, standard stuff
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print("TOKEN RECEIVED:", token) 

    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(models.User).filter(models.User.email == email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception as e:
        print("EXCEPTION:", e)
        raise HTTPException(status_code=401, detail="Invalid or missing token")
