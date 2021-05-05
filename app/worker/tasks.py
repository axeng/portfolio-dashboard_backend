from celery.utils.log import get_task_logger

from app.worker.main import app

from time import sleep

logger = get_task_logger(__name__)


@app.task
def test():
    logger.info("call worker")

    sleep(10)

    logger.info("worker finish")

    return "test"
