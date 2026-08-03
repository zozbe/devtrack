from domain.user import User
from api.schemas import UserCreateRequest
from infrastructure.user_repository import MySQLUserRepository
from application.auth_service import AuthService

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

    def create_user(self, request_data: UserCreateRequest) -> User:
        # Aynı email veya kullanıcı adı var mı kontrolü (Aynen kalıyor)
        existing_users = self.repository.get_all()
        for user in existing_users:
            if user.email == request_data.email:
                raise ValueError("Bu email adresi zaten kullanılıyor.")
            if user.username == request_data.username:
                raise ValueError("Bu kullanıcı adı zaten alınmış.")
        
        # YENİ: Kullanıcıyı oluştururken şifreyi hashleyerek atıyoruz
        new_user = User(
            username=request_data.username,
            email=request_data.email,
            full_name=request_data.full_name
        )
        # Şifreyi güvenlikten geçirip Domain nesnemize ekliyoruz
        new_user.hashed_password = AuthService.get_password_hash(request_data.password)
        
        return self.repository.save(new_user)
    
    def get_all_users(self) -> list[User]:
        return self.repository.get_all()