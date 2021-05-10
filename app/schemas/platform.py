from pydantic import BaseModel


class PlatformBase(BaseModel):
    display_name: str


class PlatformCreate(PlatformBase):
    pass


class PlatformUpdate(PlatformBase):
    pass


class PlatformInDBBase(PlatformBase):
    id: int

    class Config:
        orm_mode = True


class Platform(PlatformInDBBase):
    pass


class PlatformInDB(PlatformInDBBase):
    pass
