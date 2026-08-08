import uuid
import json
from datetime import datetime, timezone

class AuditLog:
    def __init__(
        self, 
        entity_id: str, 
        action: str, 
        user_id: str, 
        changes: dict | None = None, 
        entity_type: str = "ISSUE", 
        id: str | None = None, 
        created_at: datetime | None = None
    ):
        self.id = id or str(uuid.uuid4())
        self.entity_id = entity_id
        self.entity_type = entity_type
        self.action = action
        self.user_id = user_id
        # Değişiklikleri veritabanına metin (Text) olarak yazabilmek için JSON'a çeviriyoruz
        self.changes = json.dumps(changes, default=str) if changes else None
        self.created_at = created_at or datetime.now(timezone.utc)