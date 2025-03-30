from fastapi import FastAPI
from app.utils.limiter import limiter, rate_limit_exceeded_handler
from app.routers import auth, users
from app.api import ask_routes
from app.db.database import engine
from app.db import models

#python -m app.main


# Create all DB tables
models.Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI()

# Rate limiter
app.state.limiter = limiter
app.add_exception_handler(429, rate_limit_exceeded_handler)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(ask_routes.router, prefix="/ask", tags=["Q&A"])

print("everything is working")

@app.get("/")
def root():
    return {"message": "Backend is live!"}