from domain.audit_log import AuditLog
from infrastructure.database import SessionLocal
from infrastructure.models import AuditLogDBModel

class MySQLAuditLogRepository:
    
    def save(self, audit_log: AuditLog) -> AuditLog:
        with SessionLocal() as db:
            db_item = AuditLogDBModel(
                id=audit_log.id,
                entity_id=audit_log.entity_id,
                entity_type=audit_log.entity_type,
                action=audit_log.action,
                user_id=audit_log.user_id,
                changes=audit_log.changes,
                created_at=audit_log.created_at
            )
            db.add(db_item)
            db.commit()
            
        return audit_log