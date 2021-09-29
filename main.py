import uvicorn
from fastapi import FastAPI

from middlewares.request_utils import AddRequestIdMiddleware
from routers.todo_lists import todo_list_router
from routers.todos import todos_router
from routers.users import user_router


def app():
    todo_api_app = FastAPI(
        title='Python Todo App'
    )

    todo_api_app.add_middleware(AddRequestIdMiddleware)

    todo_api_app.include_router(user_router)
    todo_api_app.include_router(todo_list_router)
    todo_api_app.include_router(todos_router)
    return todo_api_app


if __name__ == '__main__':
    uvicorn.run(
        app(),
        server_header=False
    )
