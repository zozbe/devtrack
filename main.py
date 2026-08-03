from infrastructure.database import engine, Base
from infrastructure import models
from fastapi import FastAPI, HTTPException
from api.routes import router as issues_router
from application.user_service import UserService
from application.issue_service import IssueService 
from api.schemas import UserCreateRequest, UserResponse, IssueResponse, IssueUpdateRequest
from fastapi.middleware.cors import CORSMiddleware

# Şeflerimizi başlatalım
user_service = UserService()
# 2. GÖREV ŞEFİMİZ (ISSUE SERVICE) EKLENDİ
issue_service = IssueService() 

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

@app.post("/users/", response_model=UserResponse, tags=["Kullanıcılar (Users)"])
def create_user(request: UserCreateRequest):
    return user_service.create_user(request)

@app.get("/users/", response_model=list[UserResponse], tags=["Kullanıcılar (Users)"])
def get_all_users():
    return user_service.get_all_users()

@app.put("/issues/{issue_id}", response_model=IssueResponse, tags=["Görevler (Issues)"])
def update_issue(issue_id: str, request: IssueUpdateRequest):
    try:
        return issue_service.update_issue(issue_id, request)
    except ValueError as e:
        # Şefimiz "Bulunamadı" diye hata fırlatırsa, Garson kullanıcıya 404 döner.
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/issues/{issue_id}", tags=["Görevler (Issues)"])
def delete_issue(issue_id: str):
    try:
        return issue_service.delete_issue(issue_id)
    except ValueError as e:
        # Şef "Bulamadım" derse, kullanıcıya 404 Not Found dönüyoruz
        raise HTTPException(status_code=404, detail=str(e))