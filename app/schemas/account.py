from typing import Optional

from pydantic import BaseModel
from pydantic.class_validators import validator

from app.database import SessionLocal
from app import crud


class AccountBase(BaseModel):
    parent_account_id: Optional[int]
    display_name: str


class AccountCreate(AccountBase):
    platform_id: Optional[int]
    additional_data: Optional[str]

    @validator("platform_id")
    def valid_platform_id(cls, v):
        db = SessionLocal()

        platform = crud.platform.get(db, v)
        if platform is None:
            raise ValueError("The platform is invalid")

        return v

    @validator("additional_data", always=True)
    def valid_additional_data(cls, v, values, **kwargs):
        from app.platforms import platform_to_module

        if values["platform_id"] is not None:
            if v is None:
                raise ValueError("Additional data must be provided")

            db = SessionLocal()

            platform = crud.platform.get(db, values["platform_id"])
            platform_module = platform_to_module[platform.name]

            platform_module.additional_data_model.parse_raw(v)

            return v

        return None


class AccountUpdate(AccountBase):
    additional_data: Optional[str]


class AccountInDBBase(AccountBase):
    id: int
    platform_id: Optional[int]
    additional_data: Optional[str]

    class Config:
        orm_mode = True


class Account(AccountInDBBase):
    pass


class AccountInDB(AccountInDBBase):
    user_id: int
