from app.worker import celery_app
import time
import logging

logger = logging.getLogger("sentinel")

@celery_app.task(name="send_email_alert")
def send_email_alert(transaction_id: str, risk_score: float, email: str):
    """
    Simulated background task to send an email alert for high-risk transactions.
    """
    logger.info(f"[Worker] Processing Email Alert for Txn: {transaction_id}")
    
    # Simulate network delay (e.g. SMTP server)
    time.sleep(2) 
    
    message = f"""
    WARNING: HIGH RISK TRANSACTION DETECTED
    ---------------------------------------
    Transaction ID: {transaction_id}
    Risk Score: {risk_score}
    User Email: {email}
    
    Action: Please verify this transaction immediately.
    """
    
    logger.info(f"[Worker] Email Sent to {email}:\n{message}")
    return "Email Sent"
