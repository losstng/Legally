from fastapi import FastAPI
from app.utils.limiter import limiter, rate_limit_exceeded_handler
from app.routers import auth, users
from app.api import ask_routes
from app.db.database import engine
from app.schemas.ask import ApiResponse
from app.db import models
from app.routers import misc

#  export PYTHONPATH=$(pwd)
#  python3 -m app.main
#  python3 -m uvicorn app.main:app --reload

# =>. python3 -m uvicorn app.main:app --reload --log-level debug
# redis-server

# Create all DB tables (primitive), will be discarded or modified
models.Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI()

# Rate limiter, in that we are modifying the app
app.state.limiter = limiter
app.add_exception_handler(429, rate_limit_exceeded_handler)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend origin explicitly for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers, like adding those routers and modifying the app to have them
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(ask_routes.router, prefix="/ask", tags=["Q&A"])
app.include_router(misc.router, prefix="/misc", tags=["Misc"])

print("everything is working")

from fastapi.routing import APIRoute

for route in app.routes:
    if isinstance(route, APIRoute):
        print(f"{route.path} -> {route.methods}")

@app.get("/")
def root():
    return ApiResponse(success=True, data={"message": "Backend is live!"}) #checking system