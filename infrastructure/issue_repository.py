from domain.issue import Issue

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