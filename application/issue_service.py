from domain.issue import Issue
from api.schemas import IssueCreateRequest, IssueUpdateRequest
from datetime import datetime, timezone
from domain.repositories import AbstractIssueRepository
from infrastructure.logger import logger
from domain.audit_log import AuditLog
from infrastructure.audit_log_repository import MySQLAuditLogRepository

class IssueService:
    def __init__(self, repository):
        self.repository = repository
        self.audit_repo = MySQLAuditLogRepository() # YENİ: Kara kutu depomuz

    def create_issue(self, request_data: IssueCreateRequest, user_id: str) -> Issue:
        new_issue = Issue(
            title=request_data.title,
            description=request_data.description,
            assignee_id=user_id, 
            due_date=request_data.due_date
        )
        
        saved_issue = self.repository.save(new_issue)
        
        # LOGGER DOSYASINA KAYIT
        logger.info(f"Yeni görev oluşturuldu! Başlık: '{saved_issue.title}' | Atanan Kişi ID: {user_id}")
        
        # AUDIT LOG VERİTABANINA KAYIT: Kim oluşturdu?
        audit = AuditLog(entity_id=saved_issue.id, action="CREATE", user_id=user_id)
        self.audit_repo.save(audit)
        
        return saved_issue
    
    def get_all_issues(self, skip: int = 0, limit: int = 100, status: str | None = None, search_query: str | None = None, sort_by: str = "created_at", sort_order: str = "desc") -> list[Issue]:
        return self.repository.get_all(skip=skip, limit=limit, status=status, search_query=search_query, sort_by=sort_by, sort_order=sort_order)
    
    def get_issue_by_id(self, issue_id: str) -> Issue | None:
        return self.repository.get_by_id(issue_id)

    # GÜNCELLEME: user_id parametresi eklendi (Kim güncelledi bilmek için)
    def update_issue(self, issue_id: str, request_data: IssueUpdateRequest, user_id: str) -> Issue | None:
        update_data = request_data.model_dump(exclude_unset=True)
        
        if "status" in update_data:
            update_data["status"] = update_data["status"].value
            
        updated_issue = self.repository.update(issue_id, update_data)
        
        if updated_issue:
            # AUDIT LOG VERİTABANINA KAYIT: Kim güncelledi? (Değişiklikleri de kaydediyoruz)
            audit = AuditLog(entity_id=issue_id, action="UPDATE", user_id=user_id, changes=update_data)
            self.audit_repo.save(audit)
            
        return updated_issue

    # GÜNCELLEME: user_id parametresi eklendi (Kim sildi bilmek için) ve çift fonksiyon birleştirildi
    def delete_issue(self, issue_id: str, user_id: str) -> bool:
        logger.info(f"Silme (Soft Delete) isteği alındı. Hedef Görev ID: {issue_id}")
        
        result = self.repository.delete(issue_id)
        
        if result:
            logger.info(f"Görev başarıyla silindi (is_deleted=True). Görev ID: {issue_id}")
            
            # AUDIT LOG VERİTABANINA KAYIT: Kim sildi?
            audit = AuditLog(entity_id=issue_id, action="DELETE", user_id=user_id)
            self.audit_repo.save(audit)
        else:
            logger.warning(f"Silinmek istenen görev bulunamadı veya zaten silinmiş! Görev ID: {issue_id}")
            
        return result

    def get_my_issues(self, user_id: str, skip: int = 0, limit: int = 100, status: str | None = None, search_query: str | None = None, sort_by: str = "created_at", sort_order: str = "desc") -> list[Issue]:
        return self.repository.get_issues_by_assignee(user_id, skip=skip, limit=limit, status=status, search_query=search_query, sort_by=sort_by, sort_order=sort_order)