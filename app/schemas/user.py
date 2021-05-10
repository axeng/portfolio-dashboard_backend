from pydantic import BaseModel


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    keycloak_user_id: str


class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: int
    keycloak_user_id: str

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    pass
