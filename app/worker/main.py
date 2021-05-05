from celery import Celery
from pydantic.tools import lru_cache

from app import config


@lru_cache()
def get_celery_settings():
    return config.Settings().celery


app = Celery("app.worker",
             broker=get_celery_settings().broker_address,
             backend=get_celery_settings().backend_address,
             include=["app.worker.tasks"])

app.conf.update(
    worker_concurrency=1
)
