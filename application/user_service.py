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

    def authenticate_user(self, username: str, password: str) -> dict:
        # 1. Veritabanındaki tüm kullanıcıları çekip bizimkini arıyoruz
        users = self.repository.get_all()
        target_user = None
        for u in users:
            if u.username == username:
                target_user = u
                break
        
        # Eğer kullanıcı adı yoksa hata fırlat
        if not target_user:
            raise ValueError("Kullanıcı adı veya şifre hatalı!")
            
        # 2. Şifreyi doğrula (Kripto Şefimize soruyoruz)
        if not AuthService.verify_password(password, target_user.hashed_password):
            raise ValueError("Kullanıcı adı veya şifre hatalı!")
            
        # 3. Her şey doğruysa Token (Yaka Kartı) üret
        # Token'ın içine kullanıcının adını ve ID'sini gizliyoruz
        token_data = {"sub": target_user.username, "id": target_user.id}
        token = AuthService.create_access_token(token_data)
        
        # FastAPI'nin standart Login yanıt formatı budur:
        return {"access_token": token, "token_type": "bearer"}