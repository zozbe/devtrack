from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone

# Şifreleri hashlemek (çırpmak) için kullanacağımız algoritma (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Token Ayarları (Gerçek bir projede bu anahtar .env dosyasında gizlenir!)
SECRET_KEY = "devtrack_cok_gizli_anahtar" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 # Token 1 saat sonra geçersiz olacak

class AuthService:
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        # Düz metin şifreyi (örn: 123456) alıp karmaşık bir hash'e çevirir
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        # Kullanıcının girdiği şifre ile veritabanındaki hash eşleşiyor mu kontrol eder
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict) -> str:
        # Kullanıcıya vereceğimiz dijital yaka kartını (Token) oluşturur
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire.timestamp()})
        
        # Gizli anahtarımızla veriyi imzalayıp token'ı basıyoruz
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt