from infrastructure.database import engine, Base
from infrastructure import models
from fastapi import FastAPI, HTTPException
from api.routes import router as issues_router
from application.user_service import UserService
from api.schemas import UserCreateRequest, UserResponse, IssueResponse, IssueUpdateRequest
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from api.dependencies import get_current_user_token
from fastapi import Request
from fastapi.responses import JSONResponse
from domain.exceptions import IssueNotFoundException

# Şeflerimizi başlatalım
user_service = UserService()


#Base.metadata.drop_all(bind=engine)
# Yeni ilişkisel (Foreign Key'li) yapıyı sıfırdan kur
Base.metadata.create_all(bind=engine)

# Uygulamamızın ana örneğini (instance) oluşturuyoruz.
app = FastAPI(
    title="DevTrack API",
    description="Geliştirici Görev ve Hata Takip Sistemi",
    version="1.0.0"
)

@app.exception_handler(IssueNotFoundException)
async def issue_not_found_exception_handler(request: Request, exc: IssueNotFoundException):
    # Bu fonksiyon, içeride IssueNotFoundException fırlatıldığında otomatik devreye girer
    return JSONResponse(
        status_code=404,
        content={
            "error_type": "IssueNotFound",
            "message": exc.message,
            "requested_path": request.url.path
        }
    )

app.include_router(issues_router)

# CORS Ayarları (React gibi dış uygulamaların API'ye erişmesine izin verir)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme aşamasında tüm kaynaklara izin veriyoruz (*). Canlıda burası sınırlandırılır.
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE vb. tüm HTTP metodlarına izin ver.
    allow_headers=["*"],  # Tüm isteklere (özellikle ileride ekleyeceğimiz Token başlıklarına) izin ver.
)

# /health endpoint'i: Sistemin ayakta olup olmadığını kontrol eder.
@app.get("/health")
async def health_check():
    return {
        "service": "DevTrack",
        "status": "Running",
        "message": "Sistem sağlıklı bir şekilde çalışıyor!"
    }

@app.get("/users/", response_model=list[UserResponse], tags=["Kullanıcılar (Users)"])
def get_all_users():
    return user_service.get_all_users()

@app.post("/users/", response_model=UserResponse, tags=["Kullanıcılar (Users)"])
def create_user(request: UserCreateRequest):
    try:
        return user_service.create_user(request)
    except ValueError as e:
        # Kullanıcı zaten varsa 500 çökmesi yerine 400 hatası dönüyoruz
        raise HTTPException(status_code=400, detail=str(e))

# Login (Giriş Yap) Kapısı
@app.post("/login", tags=["Güvenlik (Auth)"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        # FastAPI'nin standart formu bize 'username' ve 'password' verir
        return user_service.authenticate_user(form_data.username, form_data.password)
    except ValueError as e:
        # Eğer şefimiz "Hatalı" derse, kullanıcıya 401 Unauthorized (Yetkisiz) dönüyoruz
        raise HTTPException(status_code=401, detail=str(e))

# SADECE YAKA KARTI OLANLARIN GİREBİLECEĞİ VIP ODA
@app.get("/me", tags=["Güvenlik (Auth)"])
def get_my_profile(current_user: dict = Depends(get_current_user_token)):
    return {
        "message": "İçeri girmeyi başardın! Güvenlik kontrolünden geçtin.",
        "user_info": current_user
    }