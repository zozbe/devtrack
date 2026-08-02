from domain.user import User
from api.schemas import UserCreateRequest
from infrastructure.user_repository import MySQLUserRepository

class UserService:
    def __init__(self):
        # Kullanıcı şefimize yeni deposunu veriyoruz
        self.repository = MySQLUserRepository()

    def create_user(self, request_data: UserCreateRequest) -> User:
        # 1. Gelen verilerle saf bir User (Kullanıcı) nesnesi yarat
        new_user = User(
            username=request_data.username,
            email=request_data.email,
            full_name=request_data.full_name
        )
        
        # 2. Depoya kaydet
        self.repository.save(new_user)
        
        return new_user
    
    def get_all_users(self) -> list[User]:
        return self.repository.get_all()