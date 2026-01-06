from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas import TransactionCreate, TransactionResponse
from app.database import get_db
from app.models import Transaction, IdempotencyKey, User
from datetime import datetime
import uuid
import logging
import time

# Basic Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sentinel")

from app.rule_engine import RuleEngine
from app.ml_model import FraudMLModel
from app.auth import get_current_user, get_password_hash

# Initialize Intelligence Layer
rule_engine = RuleEngine()
ml_service = FraudMLModel()

router = APIRouter(
    prefix="/transaction",
    tags=["transactions"]
)

@router.post("/", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionCreate,
    idempotency_key: str = Header(..., description="Unique key to prevent duplicate processing"),
    current_user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    start_time = time.time()

    # --- 1. Idempotency Check ---
    stmt = select(IdempotencyKey).where(IdempotencyKey.key == idempotency_key)
    result = await db.execute(stmt)
    existing_key = result.scalar_one_or_none()

    if existing_key:
        stmt_tx = select(Transaction).where(Transaction.id == existing_key.transaction_id)
        result_tx = await db.execute(stmt_tx)
        existing_tx = result_tx.scalar_one_or_none()
        
        if existing_tx:
            logger.info(f"Idempotent hit: {idempotency_key}")
            return TransactionResponse(
                transaction_id=existing_tx.id,
                status=existing_tx.status,
                risk_score=existing_tx.risk_score,
                timestamp=existing_tx.created_at
            )

    # --- 2. User Handling (Auto-create for Demo) ---
    stmt_user = select(User).where(User.id == transaction.user_id)
    result_user = await db.execute(stmt_user)
    user = result_user.scalar_one_or_none()

    if not user:
        user = User(
            id=transaction.user_id, 
            username=f"user_{transaction.user_id}", 
            email=f"user_{transaction.user_id}@example.com",
            hashed_password=get_password_hash("123456")
        )
        db.add(user)
        await db.flush()

    # --- 3. Intelligence Layer (Week 3) ---
    # A. ML Model Prediction (Simulation)
    # We pass basic features: [user_id, amount]
    ml_score = ml_service.predict([transaction.user_id, transaction.amount])
    logger.info(f"ML Model Score: {ml_score:.4f} (Isolation Forest Simulated)")
    
    # B. Rule Engine Evaluation
    txn_data = {"amount": transaction.amount, "currency": transaction.currency}
    rule_result = rule_engine.evaluate(txn_data)
    
    status = rule_result["status"]
    risk_score = rule_result["risk_score"]
    
    # --- 4. Persistence ---
    new_tx_id = str(uuid.uuid4())
    new_tx = Transaction(
        id=new_tx_id,
        user_id=user.id,
        amount=transaction.amount,
        currency=transaction.currency,
        status=status,
        risk_score=risk_score
    )
    db.add(new_tx)
    await db.flush() 

    # Save Idempotency Key
    new_key = IdempotencyKey(key=idempotency_key, transaction_id=new_tx_id)
    db.add(new_key)

    await db.commit()
    await db.refresh(new_tx)

    # --- 5. Async Tasks (Celery) ---
    if status == "flagged":
        # Offload email sending to background worker
        # Note: If Redis is not running, this might fail or hang depending on config.
        # Wrapped in try/except for demo stability if Redis is missing.
        try:
            from app.tasks import send_email_alert
            send_email_alert.delay(new_tx.id, risk_score, user.email)
            logger.info(f"Queued email alert for {new_tx.id}")
        except Exception as e:
            logger.error(f"Failed to queue Celery task: {e}")

    process_time = (time.time() - start_time) * 1000
    logger.info(f"Processed Request | Time: {process_time:.2f}ms | Status: {status} | Score: {risk_score}")

    return TransactionResponse(
        transaction_id=new_tx.id,
        status=new_tx.status,
        risk_score=new_tx.risk_score,
        timestamp=new_tx.created_at
    )
