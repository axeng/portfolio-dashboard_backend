from typing import Optional

from pydantic import BaseModel


class AssetBase(BaseModel):
    asset_type_id: int
    platform_id: Optional[int]
    platform_asset_id: Optional[str]
    parent_asset_id: Optional[int]


class AssetCreate(AssetBase):
    code: str


class AssetUpdate(AssetBase):
    pass


class AssetInDBBase(AssetBase):
    id: int
    code: str

    class Config:
        orm_mode = True


class Asset(AssetInDBBase):
    pass


class AssetInDB(AssetInDBBase):
    pass
