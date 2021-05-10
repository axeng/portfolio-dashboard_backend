from pydantic import BaseModel


class TransactionTypeBase(BaseModel):
    display_name: str


class TransactionTypeCreate(TransactionTypeBase):
    pass


class TransactionTypeUpdate(TransactionTypeBase):
    pass


class TransactionTypeInDBBase(TransactionTypeBase):
    id: int

    class Config:
        orm_mode = True


class TransactionType(TransactionTypeInDBBase):
    pass


class TransactionTypeInDB(TransactionTypeInDBBase):
    pass
