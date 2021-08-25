from typing import Dict, Type, TypeVar

from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from pydantic import BaseModel

T = TypeVar('T')


class BaseStorableEntity(BaseModel):
    id: str
    createdOn: DatetimeWithNanoseconds
    updatedOn: DatetimeWithNanoseconds
    data: Dict

    def convert_to(self, target: Type[T]) -> T:
        try:
            return target(**self.dict())
        except Exception as ex:
            print(f'Failed to convert {self} to {target}: {ex}')


class FirebaseAuthResponse(BaseModel):
    kind: str
    idToken: str
    email: str
    refreshToken: str
    expiresIn: str
    localId: str
    registered: bool
    displayName: str


class DecodedIdToken(BaseModel):
    aud: str
    auth_time: int
    email: str
    email_verified: bool
    exp: int
    firebase: dict
    iat: int
    iss: str
    name: str
    sub: str
    uid: str
    user_id: str
