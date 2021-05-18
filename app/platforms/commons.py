from enum import Enum, unique

from pydantic.main import BaseModel

import importlib

from app.platforms import platform_to_module


@unique
class DataTypeEnum(str, Enum):
    transactions = "transactions"


@unique
class RequestMethodEnum(str, Enum):
    post = "POST"
    get = "GET"


class Endpoint(BaseModel):
    uri_path: str
    method: RequestMethodEnum
    requires_auth: bool


class Request(BaseModel):
    url: str
    method: RequestMethodEnum
    rate_limit: float = 0
    headers: dict = {}
    parameters: dict = {}
    data: dict = {}


def construct_request(endpoint: Endpoint, api_url: str, **kwargs) -> Request:
    return Request(
        url=api_url + endpoint.uri_path,
        method=endpoint.method,
        **kwargs
    )


def get_platform_module(platform_name: str):
    module_name = platform_to_module[platform_name]
    module = importlib.import_module(f"app.platforms.{module_name}")

    return module
