import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# .env dosyasındaki gizli şifreleri sisteme yüklüyoruz
load_dotenv()

# Şifreyi artık kodun içine değil, işletim sisteminden (çevre değişkeninden) alıyoruz
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()