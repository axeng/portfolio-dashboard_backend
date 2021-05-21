from pydantic import BaseModel

from pydantic.class_validators import validator

from app.database import SessionLocal
from app import crud


class ExternalAPIBase(BaseModel):
    display_name: str


class ExternalAPICreate(ExternalAPIBase):
    account_id: int
    authentication_data: str

    @validator("account_id")
    def account_has_platform(cls, v):
        db = SessionLocal()

        account = crud.account.get(db, v)
        if account is None:
            raise ValueError("The account id is invalid")

        if account.platform_id is None:
            raise ValueError("The account is not linked to any platform")

        return v

    @validator("authentication_data")
    def valid_authentication_data(cls, v, values, **kwargs):
        from app.platforms import platform_to_module

        db = SessionLocal()

        account = crud.account.get(db, values["account_id"])
        platform = crud.platform.get(db, account.platform_id)
        platform_module = platform_to_module[platform.name]

        platform_module.authentication_data_model.parse_raw(v)

        return v


class ExternalAPIUpdate(ExternalAPIBase):
    pass


class ExternalAPIInDBBase(ExternalAPIBase):
    id: int
    account_id: int

    class Config:
        orm_mode = True


class ExternalAPI(ExternalAPIInDBBase):
    pass


class ExternalAPIInDB(ExternalAPIInDBBase):
    authentication_data: str
