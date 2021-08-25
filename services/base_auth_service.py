import requests
from firebase_admin.auth import UserRecord

from config.constants import ApplicationConfig
from models.common import FirebaseAuthResponse, DecodedIdToken
from services.firebase import get_firebase_auth_client

application_config = ApplicationConfig()


def firebase_sign_in_user(email: str, password: str) -> FirebaseAuthResponse:
    payload = {
        'email': email,
        'password': password,
        'returnSecureToken': True
    }
    response = requests.post(
        f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?'
        f'key={application_config.firebase_api_key}',
        payload
    )
    json = response.json()
    if response.ok:
        return FirebaseAuthResponse(
            kind = json['kind'],
            idToken = json['idToken'],
            email = json['email'],
            refreshToken = json['refreshToken'],
            expiresIn = json['expiresIn'],
            localId = json['localId'],
            registered = json['registered'],
            displayName = json['displayName']
        )
    raise Exception(json)


class BaseAuthService:
    _auth_client = get_firebase_auth_client()

    def auth_signup_user(self, display_name: str, email: str, password: str) -> UserRecord:
        return self._auth_client.create_user(
            display_name = display_name,
            email = email,
            password = password
        )

    def auth_verify_id_token(self, id_token: str) -> DecodedIdToken:
        return DecodedIdToken(**self._auth_client.verify_id_token(id_token, True))
