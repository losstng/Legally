from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.requests import Request
from starlette.responses import JSONResponse
#slowapi is an extension of fastapi
#starlette is the engine that fastapi is build upon
limiter = Limiter(key_func=get_remote_address) #key_function is who is the target

def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded): #detecting the amount of the reequest, and execute when limited
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests! Slow down bro!"}
    )