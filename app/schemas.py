from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class HealthCheck(BaseModel):
    status: str = "ok"
    version: str = "1.0.0"

class TransactionCreate(BaseModel):
    user_id: int
    amount: float = Field(..., gt=0, description="Transaction amount must be positive")
    currency: str = "USD"

class TransactionResponse(BaseModel):
    transaction_id: str
    status: str
    risk_score: float
    timestamp: datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=4)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    
    class Config:
        orm_mode = True
