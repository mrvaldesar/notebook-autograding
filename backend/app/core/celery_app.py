from celery import Celery
from app.core.config import settings

celery_app = Celery("worker", broker=settings.CELERY_BROKER_URL)

celery_app.conf.task_routes = {"app.worker.autograde_notebook": "main-queue"}
