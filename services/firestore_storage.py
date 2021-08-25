from typing import cast, Tuple, Any, Type

from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from google.cloud.firestore import Client as FirestoreClient, DocumentSnapshot

from models.common import BaseStorableEntity

Criteria = Tuple[str, str, Any]


class FirestoreStorageException(BaseException):
    pass


class FirestoreStorageService:
    _firestore_client: FirestoreClient

    def __init__(self, firestore_client: FirestoreClient):
        self._firestore_client = firestore_client

    def store_with_id(self, entity_type: str, entity_id: str, data: Any) -> BaseStorableEntity:
        self._firestore_client.collection(entity_type).document(entity_id).set(data)
        return self.get_one_by_id(entity_type, entity_id)

    def get_one_by_id(self, entity_type: str, entity_id: str) -> BaseStorableEntity:
        doc_snapshot = self._firestore_client.collection(entity_type).document(entity_id).get()
        if doc_snapshot.exists:
            return FirestoreStorageService._snapshot_to_entity(doc_snapshot)
        raise FirestoreStorageException(f'Entity:{entity_type} with id={entity_id}) does not exist')

    def get_all(self, entity_type: str, criteria: list[Criteria] = None, limit: int = None) -> list[BaseStorableEntity]:
        docs = []
        query = self._firestore_client.collection(entity_type)

        if criteria is not None:
            for condition in criteria:
                query = query.where(*condition)

        if limit is not None:
            query.limit(limit)

        doc_snapshots: list[DocumentSnapshot] = query.get()
        for snapshot in doc_snapshots:
            docs.append(
                FirestoreStorageService._snapshot_to_entity(snapshot)
            )
        return docs

    def store(self, entity_type: str, data: dict = None) -> BaseStorableEntity:
        stored = self._firestore_client.collection(entity_type).add(data)
        return self.get_one_by_id(entity_type, stored[1].id)

    def delete(self, entity_type: str, entity_id: str) -> BaseStorableEntity:
        data = self.get_one_by_id(entity_type, entity_id)
        self._firestore_client.collection(entity_type).document(entity_id).delete()
        return data

    def update(self, entity_type: str, entity_id: str, partial_data: dict):
        self._firestore_client.collection(entity_type).document(entity_id).update(partial_data)
        return self.get_one_by_id(entity_type, entity_id)

    @staticmethod
    def _snapshot_to_entity(snapshot: DocumentSnapshot, entity_type: Type = BaseStorableEntity) -> BaseStorableEntity:
        data = {
            'id': snapshot.id,
            'createdOn': cast(DatetimeWithNanoseconds, snapshot.create_time),
            'updatedOn': cast(DatetimeWithNanoseconds, snapshot.update_time),
            'data': snapshot.to_dict()
        }
        return entity_type(**data)
