import base64
import hashlib
import hmac
import time
import urllib
from enum import Enum, unique
from typing import Optional

from pydantic.main import BaseModel
from pydantic.types import PositiveInt

from app.platforms import commons
from app.schemas import ExternalAPIInDB

supported_data_types = {
    commons.DataTypeEnum.transactions
}


@unique
class UserTierEnum(str, Enum):
    starter = "starter"
    intermediate = "intermediate"
    pro = "pro"


class AdditionalData(BaseModel):
    user_tier: UserTierEnum


class AuthenticationData(BaseModel):
    api_key: str
    private_key: str


class Endpoint(commons.Endpoint):
    counter_value: Optional[PositiveInt]


api_url = "https://api.kraken.com"
api_endpoints = {
    "trades_history":
        Endpoint(
            uri_path="/0/private/TradesHistory",
            method=commons.RequestMethodEnum.post,
            requires_auth=True,
            counter_value=2
        ),
    "ledgers":
        Endpoint(
            uri_path="/0/private/Ledgers",
            method=commons.RequestMethodEnum.post,
            requires_auth=True,
            counter_value=2
        )
}
api_default_headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}
api_rate_limit = 1000


def get_private_rate_limit(user_tier: UserTierEnum, counter_value: int) -> float:
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


def get_fetch_data_request(external_api: ExternalAPIInDB, data_type: str) -> commons.Request:
    # Get endpoint corresponding to the data_type
    if data_type == commons.DataTypeEnum.transactions:
        endpoint, data = get_fetch_transactions_request()
    else:
        # TODO details
        raise Exception()

    # Initialize default request parameters
    headers = api_default_headers.copy()
    rate_limit = api_rate_limit

    # Add authentication if needed
    if endpoint.requires_auth:
        if external_api.authentication_data is None or external_api.account.additional_data is None:
            # TODO details
            raise Exception()

        authentication_data = AuthenticationData.parse_raw(external_api.authentication_data)

        # Compute signature
        data["nonce"] = int(1000 * time.time())
        headers = {
            "API-Key": authentication_data.api_key,
            "API-Sign": get_signature(endpoint.uri_path, data, authentication_data.private_key)
        }

        # Compute rate limit
        additional_data = AdditionalData.parse_raw(external_api.account.additional_data)
        rate_limit = get_private_rate_limit(additional_data.user_tier, endpoint.counter_value)

    return commons.construct_request(
        endpoint=endpoint,
        api_url=api_url,
        rate_limit=rate_limit,
        data=data,
        headers=headers
    )
