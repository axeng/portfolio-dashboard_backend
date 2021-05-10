from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional


class TransactionBase(BaseModel):
    timestamp: datetime
    transaction_type_id: int
    asset_id: int
    amount: Decimal
    account_id: int
    transaction_reference_id: int
    platform_transaction_id: Optional[str]


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    pass


class TransactionInDBBase(TransactionBase):
    id: int

    class Config:
        orm_mode = True


class Transaction(TransactionInDBBase):
    pass


class TransactionInDB(TransactionInDBBase):
    pass
