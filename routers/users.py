from fastapi import APIRouter, Security

from middlewares.auth import get_authorized_user
from models.users import UserLoginResponse, UserLoginRequest, User, UserSignupData, UserSignupRequest
from services.user_service import UserService

user_router = APIRouter(prefix = '/users', tags = ['User'])

user_service = UserService()


@user_router.post('/login', response_model = UserLoginResponse)
async def login(login_credentials: UserLoginRequest) -> UserLoginResponse:
    auth_response = user_service.sign_in_user(login_credentials.email, login_credentials.password)
    return UserLoginResponse(
        token = auth_response.idToken,
        email = login_credentials.email,
        uid = auth_response.localId,
        expiry = auth_response.expiresIn,
        name = auth_response.displayName
    )


@user_router.get('/me', response_model = User)
async def current_user(user: User = Security(get_authorized_user)) -> User:
    return user


@user_router.post('/', response_model = User)
async def signup_user(user_signup_data: UserSignupRequest) -> User:
    return user_service.signup(UserSignupData(
        name = user_signup_data.name,
        email = user_signup_data.email,
        password = user_signup_data.password
    ))
