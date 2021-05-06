from time import sleep

from celery.utils.log import get_task_logger
from app.workers.main import app

import importlib
import requests

logger = get_task_logger(__name__)


@app.task
def external_apis_fetch_data(external_api_id, data_type):
    # external_api = get_external_api(external_api_id)
    # user = external_api.user

    user = None
    external_api_name = "kraken"

    external_api = importlib.import_module("app.external_apis." + external_api_name)

    request = external_api.get_fetch_data_request(data_type, user)

    sleep(request.rate_limit / 1000)

    response = requests.request(
        method=request.method,
        url=request.url,
        params=request.parameters,
        data=request.data,
        headers=request.headers
    )

    logger.info(response.content)
