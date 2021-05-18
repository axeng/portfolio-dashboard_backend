import importlib

from pydantic import BaseModel
from pydantic.class_validators import validator

from app.platforms import platform_to_module


class PlatformBase(BaseModel):
    display_name: str


class PlatformCreate(PlatformBase):
    name: str

    @validator("name")
    def valid_module_name(cls, v):
        if v not in platform_to_module:
            raise ValueError("No valid link to a module")

        module_name = platform_to_module[v]
        module_spec = importlib.util.find_spec(f"app.platforms.{module_name}")

        if module_spec is None:
            raise ValueError("The linked module does not exist")

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
