from enum import Enum, unique

from pydantic.main import BaseModel


@unique
class DataTypeEnum(str, Enum):
    transactions = "transactions"
    assets = "assets"


@unique
class RequestMethodEnum(str, Enum):
    post = "post"
    get = "get"


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
