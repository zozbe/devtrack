from domain.issue import Issue
from api.schemas import IssueCreateRequest, IssueUpdateRequest
from datetime import datetime, timezone
# İŞTE BURAYI DÜZELTTİK: Yeni sınıfımızı (MySQLIssueRepository) da içeri aktardık.
from infrastructure.issue_repository import IssueRepository, MySQLIssueRepository

class IssueService:
    def __init__(self):
        # Mutfak şefine "Senin depon burasıdır" diyoruz.
        self.repository = MySQLIssueRepository()

    def create_issue(self, request_data: IssueCreateRequest) -> Issue:
        # 1. Mutfak: Entity (Varlık) Üretme
        new_issue = Issue(
            title=request_data.title,
            description=request_data.description,
            assignee_id=request_data.assignee_id,
            due_date=request_data.due_date
        )
        
        # 2. Mutfak depoya "Bunu kaydet" der ve çekilir. MySQL mi, liste mi umursamaz!
        self.repository.save(new_issue)
        
        return new_issue
    
    def get_all_issues(self) -> list[Issue]:
        # Servis, depo sınıfındaki get_all metodunu çağırır.
        return self.repository.get_all()

    def get_issue_by_id(self, issue_id: str) -> Issue | None:
        # Servis sadece depodan veriyi ister
        return self.repository.get_by_id(issue_id)

    def update_issue(self, issue_id: str, update_data: IssueUpdateRequest) -> Issue | None:
        # 1. Önce depodan güncellenecek görevi buluyoruz
        issue = self.repository.get_by_id(issue_id)
        if not issue:
            return None  # Görev yoksa API katmanına None dönüyoruz (404 fırlatması için)
            
        # 2. Sadece kullanıcının gönderdiği (dolu) alanları alıyoruz
        # exclude_unset=True sayesinde kullanıcı göndermediyse boş (None) olan alanları görmezden geliyoruz
        update_dict = update_data.model_dump(exclude_unset=True)
        
        # 3. Gelen yeni verileri varlık (Entity) nesnemizin üzerine yazıyoruz
        for key, value in update_dict.items():
            setattr(issue, key, value)  # Örn: issue.status = "IN_PROGRESS" şeklinde dinamik atama yapar
            
        # 4. Senin kuralın devrede: Güncellenme zamanını sistem otomatik damgalıyor!
        issue.updated_at = datetime.now(timezone.utc)
        
        # 5. Depoya kaydet
        self.repository.update(issue)
        
        return issue

    def delete_issue(self, issue_id: str) -> bool:
        # Servis katmanı depodaki silme işlemini tetikler ve sonucu (True/False) API'ye iletir
        return self.repository.delete(issue_id)

    def update_issue(self, issue_id: str, request_data: IssueUpdateRequest) -> Issue:
        # Pydantic'in harika özelliği: exclude_unset=True sayesinde
        # sadece kullanıcının gönderdiği (doldurduğu) alanları sözlük olarak alırız.
        update_data = request_data.model_dump(exclude_unset=True)
        
        # Eğer 'status' güncelleniyorsa, Enum'ı veritabanının anladığı düz String'e çevir
        if "status" in update_data:
            update_data["status"] = update_data["status"].value
            
        # Depoya güncellemeyi yapmasını söyle
        updated_issue = self.repository.update(issue_id, update_data)
        
        # Eğer depo None döndüyse (öyle bir ID yoksa) hata fırlat
        if not updated_issue:
            raise ValueError(f"{issue_id} ID'li görev bulunamadı!")
            
        return updated_issue

    def delete_issue(self, issue_id: str) -> dict:
        # Depoya "Bu ID'yi sil" diyoruz. Başarılı olursa True, bulamazsa False dönecek.
        is_deleted = self.repository.delete(issue_id)
        
        if not is_deleted:
            # Eğer depo False dönerse, öyle bir görev yoktur. Hata fırlatıyoruz.
            raise ValueError(f"{issue_id} ID'li görev bulunamadı veya zaten silinmiş!")
            
        # Başarılıysa garsona verilecek tatlı bir onay mesajı dönüyoruz
        return {"message": "Görev başarıyla silindi."}