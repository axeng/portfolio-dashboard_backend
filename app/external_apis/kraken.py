import base64
import hashlib
import hmac
import time
import urllib
from enum import Enum

from pydantic.main import BaseModel
from pydantic.types import PositiveInt

from app.external_apis import commons


class DataTypeEnum(str, Enum):
    transactions = commons.DataTypeEnum.transactions.value


class UserTierEnum(str, Enum):
    starter = "starter"
    intermediate = "intermediate"
    pro = "pro"


class APIInfo(BaseModel):
    user_tier: UserTierEnum


class Endpoint(commons.Endpoint):
    counter_value: PositiveInt


api_url = "https://api.kraken.com"
api_endpoints = {
    "trades_history":
        Endpoint(
            uri_path="/0/private/TradesHistory",
            method=commons.RequestMethodEnum.post,
            counter_value=2
        ),
    "ledgers":
        Endpoint(
            uri_path="/0/private/Ledgers",
            method=commons.RequestMethodEnum.post,
            counter_value=2
        )
}
api_default_headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}


def get_rate_limit(user_tier: UserTierEnum, counter_value: int) -> float:
    if user_tier == UserTierEnum.starter:
        counter_decay = 0.33
    elif user_tier == UserTierEnum.intermediate:
        counter_decay = 0.5
    elif user_tier == UserTierEnum.pro:
        counter_decay = 1
    else:
        # FIXME error
        return 0

    return (counter_value / counter_decay) * 1000


def get_fetch_transactions_request() -> (Endpoint, dict):
    endpoint = api_endpoints["ledgers"]
    data = {
        "type": "trade"
    }

    return endpoint, data


def get_signature(uri_path, data, private_key):
    post_data = urllib.parse.urlencode(data)
    encoded = (str(data["nonce"]) + post_data).encode()
    message = uri_path.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(private_key), message, hashlib.sha512)
    sigd_igest = base64.b64encode(mac.digest())

    return sigd_igest.decode()


def get_fetch_data_request(data_type: str, user) -> commons.Request:
    data_type = DataTypeEnum[data_type]

    if data_type == DataTypeEnum.transactions:
        endpoint, data = get_fetch_transactions_request()
    else:
        # TODO details
        raise Exception()

    data["nonce"] = int(1000 * time.time())
    headers = {
        **api_default_headers,
        "API-Key": api_key,
        "API-Sign": get_signature(endpoint.uri_path, data, private_key)
    }

    return commons.construct_request(
        endpoint=endpoint,
        api_url=api_url,
        rate_limit=get_rate_limit(api_info.user_tier, endpoint.counter_value),
        data=data,
        headers=headers
    )
