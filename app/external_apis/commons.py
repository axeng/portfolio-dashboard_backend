from enum import Enum

from pydantic.main import BaseModel


class DataTypeEnum(str, Enum):
    transactions = "transactions"


class RequestMethodEnum(str, Enum):
    post = "POST"
    get = "GET"


class Endpoint(BaseModel):
    uri_path: str
    method: RequestMethodEnum


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
