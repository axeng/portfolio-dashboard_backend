from pydantic import BaseModel
from typing import Optional


class ExternalAPIBase(BaseModel):
    display_name: str


class ExternalAPICreate(ExternalAPIBase):
    authentication_data: Optional[str]
    account_id: int


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
    authentication_data: Optional[str]
