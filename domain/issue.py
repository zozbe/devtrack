import uuid
from datetime import datetime, timezone
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Any

# Görev durumları için bir Enum (Seçenekler Listesi) oluşturuyoruz.
class IssueStatus(Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

# Çekirdek Varlığımız (Entity)
@dataclass
class Issue:
    title: str
    description: str
    assignee_id: Optional[str] = None # UUID olduğu için str yaptık
    status: IssueStatus = IssueStatus.TODO
    # UUID ve Tarihleri biz elle vermiyoruz, nesne oluşurken otomatik atanıyor
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    due_date: Optional[datetime] = None
    
    # SİHİRLİ DOKUNUŞ: self. yok! Dataclass mantığına uygun tanımladık
    assignee: Optional[Any] = None