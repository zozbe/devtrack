from domain.user import User
from infrastructure.database import SessionLocal
from infrastructure.models import UserDBModel

class MySQLUserRepository:
    
    def save(self, user: User) -> User:
        with SessionLocal() as db:
            db_item = UserDBModel(
                id=user.id,
                username=user.username,
                email=user.email,
                hashed_password=user.hashed_password, # GÜVENLİK İÇİN EKLENDİ!
                full_name=user.full_name,
                created_at=user.created_at
            )
            db.add(db_item)
            db.commit() # Veritabanına kaydet (INSERT)
        return user

    def get_all(self) -> list[User]:
        with SessionLocal() as db:
            db_items = db.query(UserDBModel).all()
            
            users = []
            for item in db_items:
                # Veritabanı modelini saf User nesnesine çeviriyoruz
                user = User(
                    username=item.username, 
                    email=item.email, 
                    full_name=item.full_name
                )
                user.id = item.id
                user.created_at = item.created_at
                user.hashed_password = item.hashed_password # GÜVENLİK İÇİN EKLENDİ!
                users.append(user)
                
            return users