from sqlalchemy import Column, String, Text, Integer, DateTime
from infrastructure.database import Base
from datetime import datetime, timezone

class IssueDBModel(Base):
    __tablename__ = "issues" # MySQL'de oluşacak tablonun adı

    # Tablodaki sütunları (kolonları) tanımlıyoruz
    id = Column(String(36), primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="TODO")
    assignee_id = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    due_date = Column(DateTime, nullable=True)