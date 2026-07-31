from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from domain.issue import IssueStatus # Çekirdek katmanımızdan Enum'ı alıyoruz

# 1. Kullanıcıdan gelecek verinin kalıbı (Request DTO)
class IssueCreateRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Görevin başlığı")
    description: str = Field(..., min_length=10, description="Görevin detaylı açıklaması")
    assignee_id: int = Field(..., description="Görevin atandığı kullanıcının ID'si")
    due_date: Optional[datetime] = Field(default=None, description="Son teslim tarihi (opsiyonel)")

# 2. Sistemden dışarı döneceğimiz verinin kalıbı (Response DTO)
class IssueResponse(BaseModel):
    id: str
    title: str
    description: str
    assignee_id: int
    status: IssueStatus
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime] = None

class IssueUpdateRequest(BaseModel):
    # Alanların hepsi Optional çünkü kullanıcı sadece tek bir alanı güncellemek isteyebilir.
    title: Optional[str] = Field(default=None, min_length=3, max_length=100, description="Görevin başlığı")
    description: Optional[str] = Field(default=None, min_length=10, description="Görevin detaylı açıklaması")
    assignee_id: Optional[int] = Field(default=None, description="Görevin atandığı kullanıcının ID'si")
    status: Optional[IssueStatus] = Field(default=None, description="Görevin güncel durumu")
    due_date: Optional[datetime] = Field(default=None, description="Son teslim tarihi (opsiyonel)")    