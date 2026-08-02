from infrastructure.database import engine, Base
from infrastructure import models
from fastapi import FastAPI
from api.routes import router as issues_router
from application.user_service import UserService
from api.schemas import UserCreateRequest, UserResponse

# Kullanıcı şefimizi başlatalım
user_service = UserService()

# Eski yapıyı komple sil
#Base.metadata.drop_all(bind=engine)
# Yeni ilişkisel (Foreign Key'li) yapıyı sıfırdan kur
Base.metadata.create_all(bind=engine)

# Uygulamamızın ana örneğini (instance) oluşturuyoruz.
app = FastAPI(
    title="DevTrack API",
    description="Geliştirici Görev ve Hata Takip Sistemi",
    version="1.0.0"
)
app.include_router(issues_router)
# /health endpoint'i: Sistemin ayakta olup olmadığını kontrol eder.
@app.get("/health")
async def health_check():
    return {
        "service": "DevTrack",
        "status": "Running",
        "message": "Sistem sağlıklı bir şekilde çalışıyor!"
    }

@app.post("/users/", response_model=UserResponse, tags=["Kullanıcılar (Users)"])
def create_user(request: UserCreateRequest):
    return user_service.create_user(request)

@app.get("/users/", response_model=list[UserResponse], tags=["Kullanıcılar (Users)"])
def get_all_users():
    return user_service.get_all_users()