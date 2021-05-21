from pydantic import BaseModel
from pydantic.class_validators import validator


class PlatformBase(BaseModel):
    display_name: str


class PlatformCreate(PlatformBase):
    name: str

    @validator("name")
    def valid_module_name(cls, v):
        from app.platforms import platform_to_module

        if v not in platform_to_module:
            raise ValueError("No valid link to a module")

        return v


class PlatformUpdate(PlatformBase):
    pass


class PlatformInDBBase(PlatformBase):
    id: int

    class Config:
        orm_mode = True


class Platform(PlatformInDBBase):
    pass


class PlatformInDB(PlatformInDBBase):
    name: str
