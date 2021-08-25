from config.constants import TODOS_COLLECTION
from models.todos import TodoListData, TodoList
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