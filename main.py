from infrastructure.database import engine, Base
from infrastructure import models
from fastapi import FastAPI
from api.routes import router as issues_router

# Veritabanı tablolarını oluştur (Yoksa oluşturur, varsa dokunmaz)
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