from config.constants import TODOLIST_COLLECTION, TODOS_COLLECTION
from models.todos import TodoItem, TodoItemData, TodoItemDataPartial
from services.base_storage_service import BaseStorageService


def _get_collection_path(todo_list_id: str) -> str:
    return f'{TODOLIST_COLLECTION}/{todo_list_id}/{TODOS_COLLECTION}'


class TodoService(BaseStorageService):
    def get_all(self, todo_list: str) -> list[TodoItem]:
        collection = _get_collection_path(todo_list)
        return [each_entity.convert_to(TodoItem) for each_entity in self._storage_service.get_all(collection)]

    def add(self, todo_list: str, todo_text: str) -> TodoItem:
        new_todo: TodoItemData = TodoItemData(
            content = todo_text,
            is_completed = False
        )
        collection = _get_collection_path(todo_list)
        return self._storage_service.store(collection, new_todo.dict()).convert_to(TodoItem)

    def change_status(self, todo_list_id: str, todo_id: str, is_completed: bool) -> TodoItem:
        collection = _get_collection_path(todo_list_id)
        todo_update_partial = TodoItemDataPartial(
            is_completed = is_completed
        )
        return self._storage_service.update(
            collection,
            todo_id,
            todo_update_partial.dict(exclude_defaults = True)).convert_to(TodoItem)

    def delete(self, todo_list_id: str, todo_id: str) -> TodoItem:
        collection = _get_collection_path(todo_list_id)
        return self._storage_service.delete(collection, todo_id).convert_to(TodoItem)
