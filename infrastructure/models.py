from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from infrastructure.database import Base

# YENİ EKLENEN KULLANICI TABLOSU (Şifreli Güncel Versiyon)
class UserDBModel(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False) # GÜVENLİK İÇİN YENİ EKLENDİ!
    full_name = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True))
    
    # Kullanıcının üstlendiği görevlere tek tıkla ulaşmak için ilişki (Relationship)
    issues = relationship("IssueDBModel", back_populates="assignee")


# GÖREV TABLOSU
class IssueDBModel(Base):
    __tablename__ = "issues"

    id = Column(String(36), primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    status = Column(String(20), nullable=False)
    
    # düz bir sayı değil, users tablosundaki id'ye (Yabancı Anahtar) bağlı!
    assignee_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    due_date = Column(DateTime)

    # SQLAlchemy'nin bu görevi kimin aldığını (User objesi olarak) otomatik getirmesi için ilişki
    assignee = relationship("UserDBModel", back_populates="issues")

    is_deleted = Column(Boolean, default=False)

    comments = relationship("CommentDBModel", back_populates="issue", cascade="all, delete-orphan")

    is_deleted = Column(Boolean, default=False)

class CommentDBModel(Base):
    __tablename__ = "comments"

    id = Column(String(36), primary_key=True, index=True)
    issue_id = Column(String(36), ForeignKey("issues.id", ondelete="CASCADE"), nullable=False)
    author_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime)

    # İlişkiler: Bu yorum hangi göreve ve hangi kullanıcıya ait?
    issue = relationship("IssueDBModel", back_populates="comments")
    author = relationship("UserDBModel")

class AuditLogDBModel(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, index=True)
    entity_id = Column(String(36), nullable=False, index=True) # Hangi göreve işlem yapıldı? (issue_id)
    entity_type = Column(String(50), default="ISSUE") # Şimdilik sadece görevler ama ileride "USER" da olabilir
    action = Column(String(50), nullable=False) # CREATE, UPDATE, DELETE
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False) # İşlemi KİM yaptı?
    changes = Column(Text, nullable=True) # Ne değişti? (Eski ve yeni değerleri JSON olarak tutabiliriz)
    created_at = Column(DateTime)
    
    # İlişkiler
    user = relationship("UserDBModel")