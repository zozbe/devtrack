import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class User:
    username: str
    email: str
    hashed_password: str = ""  # GÜVENLİK İÇİN EKLENDİ!
    full_name: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))