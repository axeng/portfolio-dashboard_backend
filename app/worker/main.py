from celery import Celery

app = Celery("app.worker",
             include=["app.worker.tasks"])

app.conf.update(
    worker_concurrency=1
)