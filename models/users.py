from pydantic import BaseModel

from models.common import BaseStorableEntity


class UserData(BaseModel):
    name: str
    email: str


class User(BaseStorableEntity):
    data: UserData


class UserSignupData(UserData):
    password: str


class UserLoginResponse(BaseModel):
    token: str
    expiry: int
    uid: str
    email: str
    name: str


class UserLoginRequest(BaseModel):
    email: str
    password: str


class UserSignupRequest(UserData):
    password: str
