from pydantic import BaseModel


# Source: https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app/schemas/user.py


# Share properties
class TransactionBase(BaseModel):
    # TODO
    pass


# Properties to receive on item creation
class TransactionCreate(TransactionBase):
    pass


# Properties to receive on item update
class TransactionUpdate(TransactionBase):
    pass


# Properties shared by models stored in DB
class TransactionInDBBase(TransactionBase):
    id: int

    # TODO

    class Config:
        orm_mode = True


# Properties to return to client
class Transaction(TransactionInDBBase):
    pass


# Properties stored in DB
class TransactionInDB(TransactionInDBBase):
    pass
