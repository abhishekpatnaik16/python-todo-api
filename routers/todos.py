from typing import List, Literal

from fastapi import APIRouter, Security, HTTPException

from middlewares.auth import get_authorized_user
from models.todos import TodoItem, CreateTodoItemRequest
from models.users import User
from services.todo_service import TodoService
from services.todolist_service import TodoListService

todos_router = APIRouter(prefix='/todos', tags=['Todos'])

todo_list_service = TodoListService()
todos_service = TodoService()


@todos_router.get('/{todo_list_id}', response_model=List[TodoItem])
async def get_all_todos_in_todolist(
        todo_list_id: str,
        authorized_user: User = Security(get_authorized_user)
) -> list[TodoItem]:
    todo_list = todo_list_service.get_by_id(todo_list_id)
    todo_list.with_owner(authorized_user.data.email)
    todos = todos_service.get_all(todo_list.id)
    return todos


@todos_router.post('/{todo_list_id}', response_model=TodoItem)
async def create_todo_in_todolist(
        todo_list_id: str,
        create_todo_item_request: CreateTodoItemRequest,
        authorized_user: User = Security(get_authorized_user)
):
    todo_list = todo_list_service.get_by_id(todo_list_id)
    todo_list.with_owner(authorized_user.data.email)
    created_todo = todos_service.add(
        todo_list.id,
        create_todo_item_request.content
    )
    return created_todo


@todos_router.put('/{todo_list_id}/{todo_id}::{status}', response_model=TodoItem)
async def mark_todo_in_todolist(
        todo_list_id: str,
        todo_id: str,
        status: Literal['incomplete', 'complete'],
        authorized_user: User = Security(get_authorized_user)
) -> TodoItem:
    todo_list = todo_list_service.get_by_id(todo_list_id)
    todo_list.with_owner(authorized_user.data.email)
    if status == 'incomplete':
        return todos_service.change_status(todo_list.id, todo_id, False)
    elif status == 'complete':
        return todos_service.change_status(todo_list.id, todo_id, True)
    else:
        raise HTTPException(status_code=400, detail='Status can have one of these values: incomplete, complete')


@todos_router.delete('/{todo_list_id}/{todo_id}', response_model=TodoItem)
async def delete_todo_in_todolist(
        todo_list_id: str,
        todo_id: str,
        authorized_user: User = Security(get_authorized_user)
) -> TodoItem:
    todo_list = todo_list_service.get_by_id(todo_list_id)
    todo_list.with_owner(authorized_user.data.email)
    return todos_service.delete(todo_list.id, todo_id)
