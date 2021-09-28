from hashlib import md5

from firebase_admin.firestore import firestore

from config.constants import TODOS_COLLECTION
from models.todos import TodoListData, TodoList, TodoListPermission
from services.base_storage_service import BaseStorageService
from services.firestore_storage import FirestoreStorageService


class TodoListService(BaseStorageService):
    _storage_service: FirestoreStorageService

    def get_by_id(self, todolist_id: str) -> TodoList:
        return self._storage_service.get_one_by_id(TODOS_COLLECTION, todolist_id).convert_to(TodoList)

    def create(self, todo_list: TodoListData) -> TodoList:
        return self._storage_service.store(TODOS_COLLECTION, todo_list.dict()).convert_to(TodoList)

    def get_all_of_user(self, owner: str) -> list[TodoList]:
        owner_criteria = [
            ('owner', '==', owner)
        ]
        return [todo_list.convert_to(TodoList) for todo_list in self._storage_service.get_all(
            TODOS_COLLECTION, owner_criteria
        )]

    def delete(self, list_id: str) -> TodoList:
        return self._storage_service.delete(TODOS_COLLECTION, list_id).convert_to(TodoList)

    def update_access_for(self, todo_list_id: str, todolist_permission: TodoListPermission):
        field_id = md5(
            bytes(todolist_permission.email.strip(), 'utf8')
        ).digest().hex()

        update_partial = {
            f'access.{field_id}': todolist_permission.dict()
        }
        return self._storage_service.update(TODOS_COLLECTION, todo_list_id, update_partial)

    def remove_access_for(self, todo_list_id: str, email: str):
        field_id = md5(
            bytes(email.strip(), 'utf8')
        ).digest().hex()
        update_partial = {
            f'access.{field_id}': firestore.DELETE_FIELD
        }
        return self._storage_service.update(TODOS_COLLECTION, todo_list_id, update_partial)
