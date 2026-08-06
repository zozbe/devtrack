from domain.issue import Issue, IssueStatus
from infrastructure.database import SessionLocal
from infrastructure.models import IssueDBModel
from sqlalchemy.orm import joinedload
from domain.user import User
from domain.repositories import AbstractIssueRepository
from datetime import datetime, timezone
from sqlalchemy import or_, desc, asc

class MySQLIssueRepository(AbstractIssueRepository):
    
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

    # GÜNCELLEME: sort_by ve sort_order parametreleri eklendi
    def get_all(self, skip: int = 0, limit: int = 100, status: str | None = None, search_query: str | None = None, sort_by: str = "created_at", sort_order: str = "desc") -> list[Issue]:
        with SessionLocal() as db:
            query = db.query(IssueDBModel).options(joinedload(IssueDBModel.assignee))
            
            # Filtreleme mantığı
            if status:
                query = query.filter(IssueDBModel.status == status)

            # Arama mantığı
            if search_query:
                search_term = f"%{search_query}%"
                query = query.filter(
                    or_(
                        IssueDBModel.title.ilike(search_term),
                        IssueDBModel.description.ilike(search_term)
                    )
                )
                
            # YENİ: Sıralama (Sorting) mantığı
            # Hangi sütuna göre sıralayacağımızı dinamik olarak alıyoruz
            sort_column = getattr(IssueDBModel, sort_by, IssueDBModel.created_at)
            
            if sort_order == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))
                
            db_items = query.offset(skip).limit(limit).all()
            
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
        with SessionLocal() as db:
            db_item = db.query(IssueDBModel).filter(IssueDBModel.id == issue_id).first()
            
            if not db_item:
                return None
                
            for key, value in update_data.items():
                setattr(db_item, key, value)
                
            db_item.updated_at = datetime.now(timezone.utc)
            db.commit()
            
        return self.get_by_id(issue_id)

    def delete(self, issue_id: str) -> bool:
        with SessionLocal() as db:
            db_item = db.query(IssueDBModel).filter(IssueDBModel.id == issue_id).first()
            if db_item:
                db.delete(db_item)
                db.commit() 
                return True
        return False

    # GÜNCELLEME: sort_by ve sort_order parametreleri eklendi
    def get_issues_by_assignee(self, user_id: str, skip: int = 0, limit: int = 100, status: str | None = None, search_query: str | None = None, sort_by: str = "created_at", sort_order: str = "desc") -> list[Issue]:
        with SessionLocal() as db:
            query = db.query(IssueDBModel).options(joinedload(IssueDBModel.assignee)).filter(IssueDBModel.assignee_id == user_id)
            
            # Filtreleme mantığı
            if status:
                query = query.filter(IssueDBModel.status == status)
                
            # Arama mantığı
            if search_query:
                search_term = f"%{search_query}%"
                query = query.filter(
                    or_(
                        IssueDBModel.title.ilike(search_term),
                        IssueDBModel.description.ilike(search_term)
                    )
                )

            # YENİ: Sıralama (Sorting) mantığı
            sort_column = getattr(IssueDBModel, sort_by, IssueDBModel.created_at)
            
            if sort_order == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))
                
            db_items = query.offset(skip).limit(limit).all()
            
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