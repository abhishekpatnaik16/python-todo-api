from typing import List

from fastapi import APIRouter, HTTPException, Security

from middlewares.auth import get_authorized_user
from models.todos import TodoList, TodoListData, CreateTodoListRequest, TodoListPermission, EmailFieldRequest
from models.users import User
from services.firestore_storage import FirestoreStorageException
from services.todolist_service import TodoListService

todo_list_router = APIRouter(prefix='/todolists', tags=['Todo List'])

todolist_service = TodoListService()


@todo_list_router.get('/', response_model=List[TodoList])
async def get_all_todolists_of_user(authorized_user: User = Security(get_authorized_user)) -> List[TodoList]:
    return todolist_service.get_all_of_user(authorized_user.data.email)


@todo_list_router.post('/', response_model=TodoList)
async def create_todolist(
        new_todo_config: CreateTodoListRequest,
        authorized_user: User = Security(get_authorized_user)
) -> TodoList:
    new_todo_list_data = TodoListData(
        name=new_todo_config.name,
        owner=authorized_user.data.email
    )
    created_todo_list = todolist_service.create(new_todo_list_data)
    return created_todo_list


@todo_list_router.get('/{todo_list_id}', response_model=TodoList)
async def get_todolist_of_user(
        todo_list_id: str,
        authorized_user: User = Security(get_authorized_user)
) -> TodoList:
    todo_list = todolist_service.get_by_id(todo_list_id)
    todo_list.with_owner(authorized_user.data.email)
    return todo_list


@todo_list_router.delete('/{todo_list_id}', response_model=TodoList)
async def get_todolist_of_user(
        todo_list_id: str,
        authorized_user: User = Security(get_authorized_user)
) -> TodoList:
    try:
        todo_list = todolist_service.get_by_id(todo_list_id)
        todo_list.with_owner(authorized_user.data.email)
        return todolist_service.delete(todo_list.id)
    except FirestoreStorageException:
        raise HTTPException(404, f'Todo list with {todo_list_id} not found')


@todo_list_router.put('/{todo_list_id}::share', response_model=TodoList)
async def update_access_for_todolist(
        todo_list_id: str,
        todolist_permission: TodoListPermission,
        authorized_user: User = Security(get_authorized_user)
) -> TodoList:
    todo_list = todolist_service.get_by_id(todo_list_id)
    todo_list.with_owner(authorized_user.data.email)
    return todolist_service.update_access_for(
        todo_list.id, todolist_permission
    )


@todo_list_router.delete('/{todo_list_id}::share', response_model=TodoList)
async def delete_access_for_todolist(
        todo_list_id: str,
        email_field_request: EmailFieldRequest,
        authorized_user: User = Security(get_authorized_user)
) -> TodoList:
    todo_list = todolist_service.get_by_id(todo_list_id)
    todo_list.with_owner(authorized_user.data.email)
    return todolist_service.remove_access_for(todo_list.id, email_field_request.email)
