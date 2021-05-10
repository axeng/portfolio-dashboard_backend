from pydantic import BaseModel


class AssetTypeBase(BaseModel):
    display_name: str


class AssetTypeCreate(AssetTypeBase):
    name: str
    pass


class AssetTypeUpdate(AssetTypeBase):
    pass


class AssetTypeInDBBase(AssetTypeBase):
    id: int
    name: str

    class Config:
        orm_mode = True


class AssetType(AssetTypeInDBBase):
    pass


class AssetTypeInDB(AssetTypeInDBBase):
    pass
