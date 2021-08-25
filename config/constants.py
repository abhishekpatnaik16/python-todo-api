from pydantic import BaseSettings

TODOLIST_COLLECTION = 'todo_lists'
TODOS_COLLECTION = 'todos'
USERS_COLLECTION = 'users'


class ApplicationConfig(BaseSettings):
    firebase_api_key: str
    firebase_service_account_json_path: str
