import base64
import hashlib
import hmac
import json
import time
import urllib
from decimal import Decimal
from enum import Enum, unique
from typing import Optional, Dict

from pydantic.main import BaseModel
from pydantic.types import PositiveInt

from sqlalchemy.orm import Session

from app import crud
from app.models import ExternalAPI
from app.platforms.base import PlatformBase
from app.platforms.commons import DataTypeEnum, RequestMethodEnum, construct_request, Request
from app.platforms.commons import Endpoint as CommonsEndpoint
from app.schemas import TransactionCreate, AssetCreate

supported_data_types = {
    DataTypeEnum.transactions,
    DataTypeEnum.assets
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


class Endpoint(CommonsEndpoint):
    counter_value: Optional[PositiveInt]


api_url = "https://api.kraken.com"
api_endpoints = {
    "trades_history":
        Endpoint(
            uri_path="/0/private/TradesHistory",
            method=RequestMethodEnum.post,
            requires_auth=True,
            counter_value=2
        ),
    "ledgers":
        Endpoint(
            uri_path="/0/private/Ledgers",
            method=RequestMethodEnum.post,
            requires_auth=True,
            counter_value=2
        ),
    "assets":
        Endpoint(
            uri_path="/0/public/Assets",
            method=RequestMethodEnum.get,
            requires_auth=False
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


def get_fetch_transactions_request() -> Endpoint:
    return api_endpoints["ledgers"]


def get_fetch_assets_request() -> Endpoint:
    return api_endpoints["assets"]


def get_signature(uri_path, data, private_key):
    post_data = urllib.parse.urlencode(data)
    encoded = (str(data["nonce"]) + post_data).encode()
    message = uri_path.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(private_key), message, hashlib.sha512)
    sigd_igest = base64.b64encode(mac.digest())

    return sigd_igest.decode()


# TODO delete
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


class Kraken(PlatformBase[AdditionalData, AuthenticationData]):
    def get_fetch_data_request(self, data_type: DataTypeEnum, external_api: ExternalAPI = None) -> Request:
        data = {}

        # Get endpoint corresponding to the data_type
        if data_type == DataTypeEnum.transactions:
            endpoint = get_fetch_transactions_request()
        elif data_type == DataTypeEnum.assets:
            endpoint = get_fetch_assets_request()
        else:
            # TODO details
            raise Exception()

        # Initialize default request parameters
        headers = api_default_headers.copy()
        rate_limit = api_rate_limit

        # Add authentication if needed
        if endpoint.requires_auth:
            if external_api is None or external_api.account.additional_data is None:
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

        return construct_request(
            endpoint=endpoint,
            api_url=api_url,
            rate_limit=rate_limit,
            data=data,
            headers=headers
        )

    def write_results(self, db: Session, results: str, data_type: DataTypeEnum, account_id: int = None):
        results = json.loads(results)

        if len(results["error"]) > 0:
            # TODO details
            raise Exception()

        data = results["result"]

        if data_type == DataTypeEnum.transactions:
            self.write_transactions(db, data, account_id)
        elif data_type == DataTypeEnum.assets:
            self.write_assets(db, data)
        else:
            # TODO details
            raise Exception()

    def write_transactions(self, db: Session, data: Dict, account_id: int):
        if account_id is None:
            # TODO details
            raise Exception()

        data = data["ledger"]

        transaction_types = crud.transaction_type.get_dict(db)

        for ledger_id, ledger_data in data.items():
            transaction_in = TransactionCreate(
                timestamp=ledger_data["time"],
                transaction_type_id=transaction_types["trade"],

                # TODO
                asset_id=-1,

                amount=Decimal(ledger_data["amount"]),
                account_id=account_id,

                # TODO
                transaction_reference_id=-1,

                platform_transaction_id=ledger_id
            )

            # crud.transaction.create(db, transaction_in)

    def write_assets(self, db: Session, data: Dict):
        platform = crud.platform.get_by_name(db, self.platform_name)
        asset_types = crud.asset_type.get_dict(db)

        for asset_id, asset in data.items():
            asset_in = AssetCreate(
                # TODO handle fiat
                asset_type_id=asset_types["cryptocurrency"],
                platform_id=platform.id,
                # TODO handle parent asset
                code=asset_id,
                display_name=asset["altname"]
            )

            if crud.asset.get_by_code(db, asset_id, platform.id) is None:
                crud.asset.create(db, asset_in)


kraken = Kraken("kraken",
                AdditionalData,
                AuthenticationData,
                supported_data_types)
