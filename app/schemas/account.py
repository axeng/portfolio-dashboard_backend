from typing import Optional

from pydantic import BaseModel


class AccountBase(BaseModel):
    parent_account_id: Optional[int]
    display_name: str
    additional_data: Optional[str]


class AccountCreate(AccountBase):
    platform_id: Optional[int]


class AccountUpdate(AccountBase):
    pass


class AccountInDBBase(AccountBase):
    id: int
    platform_id: Optional[int]

    class Config:
        orm_mode = True


class Account(AccountInDBBase):
    pass


class AccountInDB(AccountInDBBase):
    user_id: int
