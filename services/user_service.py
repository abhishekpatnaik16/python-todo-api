from config.constants import USERS_COLLECTION
from models.users import UserSignupData, UserData, User
from services.base_auth_service import BaseAuthService, firebase_sign_in_user, FirebaseAuthResponse
from services.base_storage_service import BaseStorageService


class UserService(BaseStorageService, BaseAuthService):
    def signup(self, user_signup_data: UserSignupData) -> User:
        auth_user_record = self.auth_signup_user(
            user_signup_data.name, user_signup_data.email, user_signup_data.password
        )
        new_user_data = UserData(
            name=user_signup_data.name,
            email=user_signup_data.email,
        )
        return self._storage_service.store_with_id(USERS_COLLECTION, auth_user_record.uid, new_user_data) \
            .convert_to(User)

    def get_user_from_token(self, token: str) -> User:
        decoded_id_token = self.auth_verify_id_token(token)
        return self._storage_service.get_one_by_id(USERS_COLLECTION, decoded_id_token.uid).convert_to(User)

    def get_user_by_id(self, user_id: str) -> User:
        return self._storage_service.get_one_by_id(USERS_COLLECTION, user_id).convert_to(User)

    @staticmethod
    def sign_in_user(email: str, password: str) -> FirebaseAuthResponse:
        return firebase_sign_in_user(email, password)
