from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from app.routers import transaction, auth
from app.database import engine, Base
from app.schemas import HealthCheck
from app.auth import Token, create_access_token

app = FastAPI(
    title="SentinelStream",
    description="Fraud Detection API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup (For Demo Purposes)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth.router)
app.include_router(transaction.router)

@app.get("/health", response_model=HealthCheck, tags=["health"])
async def health_check():
    return HealthCheck(status="ok", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Welcome to SentinelStream API"}
