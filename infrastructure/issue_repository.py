from domain.issue import Issue, IssueStatus
from infrastructure.database import SessionLocal
from infrastructure.models import IssueDBModel
from sqlalchemy.orm import joinedload
from domain.user import User

class IssueRepository:
    def __init__(self):
        # Mutfaktaki geçici veritabanımızı (listemizi) gerçek yerine, yani depoya aldık.
        self.fake_database = []

    def save(self, issue: Issue) -> Issue:
        # Gelen Görev (Issue) nesnesini veritabanına kaydeder.
        self.fake_database.append(issue)
        return issue
    
    def get_all(self) -> list[Issue]:
        # Depodaki (listemizdeki) tüm görevleri geri döndürür.
        return self.fake_database

    def get_by_id(self, issue_id: str) -> Issue | None:
        # Veritabanındaki tüm görevleri tek tek dolaşıyoruz
        for issue in self.fake_database:
            if issue.id == issue_id:
                return issue  # Eşleşme bulunursa görevi döndür
        
        return None  # Döngü biter ve eşleşme bulunamazsa None döndür

    def update(self, issue: Issue) -> Issue:
        # Gerçek bir veritabanında (MySQL vb.) burada "UPDATE issues SET..." sorgusu çalışır.
        # Şu an RAM'de (listede) çalıştığımız için nesnenin özellikleri güncellendiğinde liste de güncellenmiş oluyor.
        # Ancak mimariyi bozmamak ve Mutfak şefinin depoya emir verebilmesi için bu metodu yazıyoruz.
        return issue

    def delete(self, issue_id: str) -> bool:
        # 1. Önce sileceğimiz görevi buluyoruz
        issue = self.get_by_id(issue_id)
        
        # 2. Eğer görev varsa, listeden (veritabanından) siliyoruz
        if issue:
            self.fake_database.remove(issue)
            return True # Silme başarılı
            
        return False # Silinecek görev bulunamadı


class MySQLIssueRepository:
    
    def save(self, issue: Issue) -> Issue:
        with SessionLocal() as db:
            db_item = IssueDBModel(
                id=issue.id,
                title=issue.title,
                description=issue.description,
                status=issue.status.value,
                assignee_id=issue.assignee_id,
                created_at=issue.created_at,
                updated_at=issue.updated_at,
                due_date=issue.due_date
            )
            db.add(db_item)
            db.commit() 
            
        # Kayıt bittikten sonra görevi tüm ilişkileriyle (assignee dahil) tekrar çekip dönüyoruz.
        return self.get_by_id(issue.id)

    def get_all(self) -> list[Issue]:
        with SessionLocal() as db:
            # joinedload ile görevleri çekerken, sahiplerini de getiriyoruz
            db_items = db.query(IssueDBModel).options(joinedload(IssueDBModel.assignee)).all()
            
            issues = []
            for item in db_items:
                issue = Issue(
                    title=item.title,
                    description=item.description,
                    assignee_id=item.assignee_id
                )
                issue.id = item.id
                issue.status = IssueStatus(item.status)
                issue.created_at = item.created_at
                issue.updated_at = item.updated_at
                issue.due_date = item.due_date
                
                if item.assignee:
                    user = User(
                        username=item.assignee.username,
                        email=item.assignee.email,
                        full_name=item.assignee.full_name
                    )
                    user.id = item.assignee.id
                    user.created_at = item.assignee.created_at
                    issue.assignee = user
                    
                issues.append(issue)
                
            return issues

    def get_by_id(self, issue_id: str) -> Issue | None:
        with SessionLocal() as db:
            # Görevi ve atanmış kişiyi birlikte çekiyoruz
            item = db.query(IssueDBModel).options(joinedload(IssueDBModel.assignee)).filter(IssueDBModel.id == issue_id).first()
            
            if not item:
                return None
                
            issue = Issue(
                title=item.title,
                description=item.description,
                assignee_id=item.assignee_id
            )
            issue.id = item.id
            issue.status = IssueStatus(item.status)
            issue.created_at = item.created_at
            issue.updated_at = item.updated_at
            issue.due_date = item.due_date
            
            if item.assignee:
                user = User(
                    username=item.assignee.username,
                    email=item.assignee.email,
                    full_name=item.assignee.full_name
                )
                user.id = item.assignee.id
                user.created_at = item.assignee.created_at
                issue.assignee = user
                
            return issue

    def update(self, issue_id: str, update_data: dict) -> Issue | None:
        from datetime import datetime, timezone
        with SessionLocal() as db:
            db_item = db.query(IssueDBModel).filter(IssueDBModel.id == issue_id).first()
            
            if not db_item:
                return None
                
            # Sadece kullanıcının değiştirmek istediği alanları güncelle
            for key, value in update_data.items():
                setattr(db_item, key, value)
                
            # Güncellenme zamanını damgala
            db_item.updated_at = datetime.now(timezone.utc)
            db.commit()
            
        # İşlem bitince güncel görevi tüm detaylarıyla geri döndür
        return self.get_by_id(issue_id)

    def delete(self, issue_id: str) -> bool:
        with SessionLocal() as db:
            db_item = db.query(IssueDBModel).filter(IssueDBModel.id == issue_id).first()
            if db_item:
                db.delete(db_item)
                db.commit() 
                return True
        return False