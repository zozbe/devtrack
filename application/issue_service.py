from domain.issue import Issue
from api.schemas import IssueCreateRequest, IssueUpdateRequest
from datetime import datetime, timezone
from infrastructure.issue_repository import IssueRepository, MySQLIssueRepository

class IssueService:
    def __init__(self):
        # Mutfak şefine "Senin depon burasıdır" diyoruz.
        self.repository = MySQLIssueRepository()

    # GÜVENLİK GÜNCELLEMESİ: Artık parametre olarak 'user_id' de alıyor!
    def create_issue(self, request_data: IssueCreateRequest, user_id: str) -> Issue:
        # 1. Mutfak: Entity (Varlık) Üretme
        new_issue = Issue(
            title=request_data.title,
            description=request_data.description,
            assignee_id=user_id, 
            due_date=request_data.due_date
        )
        
        # Deponun bize döndüğü o içi tamamen dolu (assignee bilgileri olan) görevi yakalıyoruz!
        saved_issue = self.repository.save(new_issue)
        
        # Ve API'ye o dolu görevi gönderiyoruz (new_issue'yu DEĞİL)
        return saved_issue
    
    def get_all_issues(self) -> list[Issue]:
        # Servis, depo sınıfındaki get_all metodunu çağırır.
        return self.repository.get_all()

    def get_issue_by_id(self, issue_id: str) -> Issue | None:
        # Servis sadece depodan veriyi ister
        return self.repository.get_by_id(issue_id)

    # Çift yazılan update fonksiyonu temizlendi ve en iyi hali bırakıldı
    def update_issue(self, issue_id: str, request_data: IssueUpdateRequest) -> Issue | None:
        # Pydantic'in harika özelliği: exclude_unset=True
        update_data = request_data.model_dump(exclude_unset=True)
        
        # Eğer 'status' güncelleniyorsa, Enum'ı veritabanının anladığı düz String'e çevir
        if "status" in update_data:
            update_data["status"] = update_data["status"].value
            
        # Depoya güncellemeyi yapmasını söyle
        updated_issue = self.repository.update(issue_id, update_data)
        
        return updated_issue # Bulunamazsa None dönecek, API katmanı 404 fırlatacak

    # Çift yazılan delete fonksiyonu temizlendi ve en iyi hali bırakıldı
    def delete_issue(self, issue_id: str) -> bool:
        # Depoya "Bu ID'yi sil" diyoruz. Başarılı olursa True, bulamazsa False dönecek.
        return self.repository.delete(issue_id)

    def get_my_issues(self, user_id: str) -> list[Issue]:
        # Servis katmanı, yaka kartından okunan ID'yi depoya iletir ve sadece o kişinin görevlerini ister.
        return self.repository.get_issues_by_assignee(user_id)