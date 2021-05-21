from time import sleep

from celery.utils.log import get_task_logger

from app.platforms import platform_to_module
from app.platforms.commons import DataTypeEnum
from app.workers.main import app
from app import crud
from app.database import SessionLocal

import requests

logger = get_task_logger(__name__)


@app.task
def external_apis_fetch_data(data_type: str, external_api_id: int = None, platform_id: int = None):
    try:
        data_type = DataTypeEnum[data_type]
    except KeyError:
        # TODO details
        raise Exception()

    # Init DB Session
    db = SessionLocal()

    if external_api_id is not None:
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
    elif platform_id is not None:
        external_api_db = None
        platform = crud.platform.get(db, platform_id)
    else:
        # TODO details
        raise Exception()

    # Load module
    platform_module = platform_to_module[platform.name]

    # TODO create loop

    # Get the request
    request = platform_module.get_fetch_data_request(data_type, external_api_db)

    sleep(request.rate_limit / 1000)

    # Send the request
    response = requests.request(
        method=request.method,
        url=request.url,
        params=request.parameters,
        data=request.data,
        headers=request.headers
    )

    account_id = external_api_db.account_id if external_api_db is not None else None
    platform_module.write_results(db, response.content, data_type, account_id)

    # TODO write in DB (re-send to external_api module)

    # logger.info(test)

    db.close()
