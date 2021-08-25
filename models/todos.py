from typing import Optional

from pydantic import BaseModel

from models.common import BaseStorableEntity


class TodoItemData(BaseModel):
    content: str
    is_completed: bool


class TodoItemDataPartial(TodoItemData):
    content: Optional[str]
    is_completed: Optional[bool]


class TodoItem(BaseStorableEntity):
    data: TodoItemData


class TodoListData(BaseModel):
    name: str
    owner: str


class TodoList(BaseStorableEntity):
    data: TodoListData

    def with_owner(self, email: str):
        if self.data.owner != email:
            raise Exception(f'TodoList({self.id}) is not owner by {email}')


class CreateTodoListRequest(BaseModel):
    name: str


class CreateTodoItemRequest(BaseModel):
    content: str
