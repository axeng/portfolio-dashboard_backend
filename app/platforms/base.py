from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, Set

from pydantic.main import BaseModel

from sqlalchemy.orm import Session

from app.models import ExternalAPI
from app.platforms.commons import DataTypeEnum, Request

AdditionalDataModelType = TypeVar("AdditionalDataModelType", bound=BaseModel)
AuthenticationDataModelType = TypeVar("AuthenticationDataModelType", bound=BaseModel)


class PlatformBase(ABC, Generic[AdditionalDataModelType, AuthenticationDataModelType]):
    def __init__(self,
                 platform_name: str,
                 additional_data_model: Type[AdditionalDataModelType],
                 authentication_data_model: Type[AuthenticationDataModelType],
                 supported_data_types: Set[DataTypeEnum]):
        self.platform_name = platform_name

        self.additional_data_model = additional_data_model
        self.authentication_data_model = authentication_data_model

        self.supported_data_types = supported_data_types

    @abstractmethod
    def get_fetch_data_request(self, data_type: DataTypeEnum, external_api: ExternalAPI = None) -> Request:
        pass

    @abstractmethod
    def write_results(self, db: Session, results: str, data_type: DataTypeEnum, account_id: int = None):
        pass
