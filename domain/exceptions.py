class DevTrackException(Exception):
    """DevTrack projesindeki tüm özel hataların atası (Base Exception)"""
    pass

class IssueNotFoundException(DevTrackException):
    """Bir görev veritabanında bulunamadığında fırlatılır."""
    def __init__(self, issue_id: str):
        self.issue_id = issue_id
        self.message = f"Sistemde '{issue_id}' kimliğine sahip bir görev bulunamadı."
        super().__init__(self.message)