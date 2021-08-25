from services.firebase import get_firestore_client
from services.firestore_storage import FirestoreStorageService


class BaseStorageService:
    _storage_service: FirestoreStorageService

    def __init__(self, storage_service: FirestoreStorageService = None):
        if storage_service is None:
            self._storage_service = FirestoreStorageService(get_firestore_client())
        else:
            self._storage_service = storage_service
