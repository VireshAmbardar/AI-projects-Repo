# app/core/celery_app.py
from celery import Celery

celery_app = Celery(
    "bond_scanner",
    broker="amqp://guest:guest@localhost:5672//",  # Your RabbitMQ TCP
    # backend="redis://localhost:6379/0",  # Task result backend (optional)
    include=["app.core.agents.googleADK.runner"]  # Where tasks are defined
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # For long-running agent tasks
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max per agent run
)