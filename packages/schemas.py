from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
  username: str



class UserCreate(UserBase):
    password: str


class User(BaseModel):
    id: int
    username: str
    hashed_password: str
    is_active: bool
    usertype: str
    class Config:
        orm_mode = True
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None





class UserInDB(User):
    hashed_password: str