from database.user_repisitory import UserRepository
from core.exceptions import UserNotFoundError, EmailAlreadyExistsError
from models.user_models import UserModel


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository: UserRepository = repository
    
    def register_user(self, user_name: str, email: str) -> UserModel:
        if self.repository.get_user_by_email(email):
            raise EmailAlreadyExistsError("Пользователь с данным email уже существует.")
        
        return self.repository.register_user(user_name=user_name, email=email)

    def create_user(self, user_name: str, email: str) -> UserModel:
        if self.repository.get_user_by_email(email):
            raise EmailAlreadyExistsError("Пользователь с данным email уже существует.")
        
        return self.repository.create_user(user_name=user_name, email=email)
    
    def get_user_by_id(self, user_id: int,) -> UserModel:
        user: UserModel | None = self.repository.get_user_by_id(user_id=user_id)
        if user == None:
            raise UserNotFoundError("Пользователь не найден.")
        return user
    
    def get_all_users(self) -> list[UserModel]:
        return self.repository.get_all_users()

    def update_user_name(self, user_id: int, user_name: str) -> None:
        updated = self.repository.update_user_name(user_id=user_id, user_name=user_name)

        if updated == 0:
            raise UserNotFoundError("Пользователь не найден.")

    def delete_user(self, user_id: int) -> None:
        deleted = self.repository.delete_user(user_id)

        if deleted == 0:
            raise UserNotFoundError("Пользователь не найден.")
    
    def _get_existing_user(self, user_id: int) -> UserModel:
        user = self.repository.get_user_by_id(user_id)

        if user is None:
            raise UserNotFoundError("Пользователь не найден.")

        return user