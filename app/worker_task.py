# app/worker_task.py
from celery import Celery

celery = Celery(
    "worker_task",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery.task
def translate_text(text: str) -> str:
    return f"Traducción simulada de: {text}"
