from pydantic import BaseModel
from typing import Optional


class TransactionReferenceBase(BaseModel):
    platform_transaction_reference_id: Optional[str]


class TransactionReferenceCreate(TransactionReferenceBase):
    pass


class TransactionReferenceUpdate(TransactionReferenceBase):
    pass


class TransactionReferenceInDBBase(TransactionReferenceBase):
    id: int

    class Config:
        orm_mode = True


class TransactionReference(TransactionReferenceInDBBase):
    pass


class TransactionReferenceInDB(TransactionReferenceInDBBase):
    pass
