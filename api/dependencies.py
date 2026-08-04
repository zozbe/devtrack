from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from application.auth_service import SECRET_KEY, ALGORITHM
# GÜNCELLEME 1: MongoDB yerine MySQLIssueRepository'i dahil ediyoruz
from infrastructure.issue_repository import MySQLIssueRepository
from application.issue_service import IssueService

# Swagger'daki o meşhur "Authorize" (Kilit) butonunu bu kod oluşturur.
# tokenUrl="login" diyerek, Swagger'a token'ı nereden alacağını söylüyoruz.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user_token(token: str = Depends(oauth2_scheme)):
    try:
        # Gelen token'ı mutfaktaki gizli anahtarımızla açıp okumaya çalışıyoruz
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise HTTPException(status_code=401, detail="Yaka kartı okunamadı!")
            
        return payload # Token'ın içindeki veriyi (username ve id) başarıyla dönüyoruz
        
    except jwt.ExpiredSignatureError:
        # Token'ın 1 saatlik süresi dolduysa
        raise HTTPException(status_code=401, detail="Yaka kartının süresi dolmuş, tekrar giriş yap!")
    except jwt.InvalidTokenError:
        # Biri token'da harf değiştirip sahtecilik yapmaya çalışırsa
        raise HTTPException(status_code=401, detail="Sahte veya geçersiz yaka kartı!")
    
# 1. Aşama: Hangi depoyu kullanacağımızı belirliyoruz (Şu an MySQL)
def get_issue_repository():
    # GÜNCELLEME 2: Burada da MySQL deposunu çağırıyoruz
    return MySQLIssueRepository()

# 2. Aşama: Depoyu şefe (servise) verip, çalışmaya hazır şefi döndürüyoruz
def get_issue_service(repository = Depends(get_issue_repository)) -> IssueService:
    return IssueService(repository=repository)