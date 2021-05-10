from typing import Optional

from pydantic import BaseModel


class AccountBase(BaseModel):
    user_id: int
    platform_id: Optional[int]
    parent_account_id: Optional[int]
    display_name: str


class AccountCreate(AccountBase):
    pass


class AccountUpdate(AccountBase):
    pass


class AccountInDBBase(AccountBase):
    id: int

    class Config:
        orm_mode = True


class Account(AccountInDBBase):
    pass


class AccountInDB(AccountInDBBase):
    pass
