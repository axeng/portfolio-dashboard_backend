from time import sleep

from celery.utils.log import get_task_logger

from app.external_apis import platform_to_module
from app.workers.main import app
from app import crud
from app.database import SessionLocal

import importlib
import requests

logger = get_task_logger(__name__)


@app.task
def external_apis_fetch_data(external_api_id: int, data_type: str):
    # Init DB Session
    db = SessionLocal()

    # Read external api object
    external_api_db = crud.external_api.get(db, external_api_id)
    if external_api_db is None:
        # TODO details
        raise Exception()

    # Read platform object
    platform = external_api_db.account.platform
    if platform is None:
        # TODO details
        raise Exception()

    # Load module
    external_api_module_name = platform_to_module[platform.name]
    external_api = importlib.import_module("app.external_apis." + external_api_module_name)

    # TODO create loop

    # Get the request
    request = external_api.get_fetch_data_request(external_api_db, data_type)

    sleep(request.rate_limit / 1000)

    # Send the request
    response = requests.request(
        method=request.method,
        url=request.url,
        params=request.parameters,
        data=request.data,
        headers=request.headers
    )

    # TODO write in DB (re-send to external_api module)

    logger.info(response.content)

    db.close()
