from pydantic import BaseModel


class AssetTypeBase(BaseModel):
    display_name: str


class AssetTypeCreate(AssetTypeBase):
    pass


class AssetTypeUpdate(AssetTypeBase):
    pass


class AssetTypeInDBBase(AssetTypeBase):
    id: int

    class Config:
        orm_mode = True


class AssetType(AssetTypeInDBBase):
    pass


class AssetTypeInDB(AssetTypeInDBBase):
    pass
