from typing import Union

import firebase_admin
from firebase_admin import firestore, auth
from google.cloud.firestore_v1.services.firestore import FirestoreClient

from config.constants import ApplicationConfig

app: Union[firebase_admin.App, None] = None
application_config = ApplicationConfig()


def init_firebase() -> firebase_admin.App:
    global app
    cred = firebase_admin.credentials.Certificate(application_config.firebase_service_account_json_path)
    app = firebase_admin.initialize_app(cred)
    return app


def get_firebase_app() -> firebase_admin.App:
    global app
    if app is None:
        return init_firebase()
    else:
        return app


def get_firestore_client() -> FirestoreClient:
    firebase_app = get_firebase_app()
    firebase_client: FirestoreClient = firestore.client(firebase_app)
    return firebase_client


def get_firebase_auth_client() -> auth.Client:
    firebase_app = get_firebase_app()
    auth_client = auth.Client(firebase_app)
    return auth_client
