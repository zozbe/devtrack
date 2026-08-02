import uuid
from datetime import datetime, timezone

class User:
    def __init__(self, username: str, email: str, full_name: str = None):
        self.id = str(uuid.uuid4()) # Her kullanıcıya benzersiz bir kimlik veriyoruz
        self.username = username
        self.email = email
        self.full_name = full_name
        
        # Sisteme kayıt olduğu anı otomatik damgalıyoruz
        self.created_at = datetime.now(timezone.utc)