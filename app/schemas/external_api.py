from pydantic import BaseModel
from typing import Optional


class ExternalAPIBase(BaseModel):
    account_id: int
    authentication_data: Optional[str]
    additional_data: Optional[str]
    display_name: str


class ExternalAPICreate(ExternalAPIBase):
    pass


class ExternalAPIUpdate(ExternalAPIBase):
    pass


class ExternalAPIInDBBase(ExternalAPIBase):
    id: int

    class Config:
        orm_mode = True


class ExternalAPI(ExternalAPIInDBBase):
    pass


class ExternalAPIInDB(ExternalAPIInDBBase):
    pass
