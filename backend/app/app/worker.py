import os

from celery import Celery
from celery.utils.log import get_task_logger
from raven import Client

from app.core.config import settings

import mlflow
from ml.training.diabetes_enet_trainer import train_enet_diabetes_dataset

celery_app = Celery(__name__)

# configs
celery_app.conf.broker_url = os.getenv("BROKER_URL", "redis://localhost:6379/0")
celery_app.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
celery_app.conf.task_routes = {
    "app.worker.run_task": "main-queue",
    "app.worker.train_enet_diabetes_model": "main-queue",
}

# other configs
# within the docker stack we use internal port instead of $MLFLOW_PORT
# $MLFLOW_PORT is only for accessing from host
mlflow.set_tracking_uri('http://mlflow:5000')

client_sentry = Client(settings.SENTRY_DSN)

celery_log = get_task_logger(__name__)

@celery_app.task(acks_late=True)
def run_task(word: str) -> str:
    celery_log.info(f"Task picked up")
    # some process
    return f"test task return {word}"

@celery_app.task(acks_late=True)
def train_enet_diabetes_model(alpha: float, l1_ratio: float):
    celery_log.info(f"Task picked up")
    celery_log.info(f"MLFLow connection: {mlflow.get_tracking_uri()}")
    run_id = train_enet_diabetes_dataset(alpha, l1_ratio)

    return run_id
