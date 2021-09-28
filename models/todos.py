from typing import Optional

from pydantic import BaseModel
from pydantic.types import Dict

from models.common import BaseStorableEntity


class TodoItemData(BaseModel):
    content: str
    is_completed: bool


class TodoItemDataPartial(TodoItemData):
    content: Optional[str]
    is_completed: Optional[bool]


class TodoItem(BaseStorableEntity):
    data: TodoItemData


class TodoListPermission(BaseModel):
    email: str
    read_only: bool = True


class TodoListData(BaseModel):
    name: str
    owner: str
    access: Dict[str, TodoListPermission] = {}


class TodoList(BaseStorableEntity):
    data: TodoListData

    def with_owner(self, email: str):
        if self.data.owner != email:
            raise Exception(f'TodoList({self.id}) is not owner by {email}')

    def with_write_user(self, email: str):
        pass

    def with_read_user(self, email: str):
        pass


class CreateTodoListRequest(BaseModel):
    name: str


class CreateTodoItemRequest(BaseModel):
    content: str


class EmailFieldRequest(BaseModel):
    email: str
