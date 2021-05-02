from celery.utils.log import get_task_logger

from app.worker.main import app

logger = get_task_logger(__name__)


@app.task
def test():
    logger.info("call worker")
