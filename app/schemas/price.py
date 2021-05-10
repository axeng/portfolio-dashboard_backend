from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class PriceBase(BaseModel):
    timestamp: datetime
    base_asset_id: int
    target_asset_id: int
    price: Decimal


class PriceCreate(PriceBase):
    pass


class PriceUpdate(PriceBase):
    pass


class PriceInDBBase(PriceBase):
    id: int

    class Config:
        orm_mode = True


class Price(PriceInDBBase):
    pass


class PriceInDB(PriceInDBBase):
    pass
