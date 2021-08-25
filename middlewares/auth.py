from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from config.application_logging import get_app_logger
from models.users import User
from services.user_service import UserService

logger = get_app_logger(__name__)

user_service = UserService()

http_bearer_scheme = HTTPBearer(
    description = 'FirebaseAuth JWT Bearer Token'
)


def get_authorized_user(
        authorization: HTTPAuthorizationCredentials = Depends(http_bearer_scheme)
) -> User:
    try:
        token = authorization.credentials
        return user_service.get_user_from_token(token)
    except Exception as ex:
        logger.exception(f'Failed to authorize user', exc_info = ex)
        raise HTTPException(403, 'Failed to authorize request')
