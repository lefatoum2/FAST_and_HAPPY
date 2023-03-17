from pydantic import BaseModel
from typing import List


class House(BaseModel):
    title: str
    content: str
    published: bool

    class Config():
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str
    password: str


class UserDisplay(BaseModel):
    username: str
    email: str
    items: List[House] = []

    class Config():
        orm_mode = True


# User inside ArticleDisplay
class User(BaseModel):
    id: int
    username: str

    class Config():
        orm_mode = True


class HouseBase(BaseModel):
    nbstreet: int
    street : str
    postal : str
    city : str
    creator_id: int


class HouseDisplay(BaseModel):
    nbstreet: int
    street: str
    postal: str
    city: str
    user: User

    class Config():
        orm_mode = True
