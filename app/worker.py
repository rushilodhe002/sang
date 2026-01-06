import os
from celery import Celery

# Redis Broker URL (Default to local)
BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "sentinel_worker",
    broker=BROKER_URL,
    backend=BROKER_URL
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

# For Windows Support (optional, usually needed if running natively)
# os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
