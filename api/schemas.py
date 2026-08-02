from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from domain.issue import IssueStatus # Çekirdek katmanımızdan Enum'ı alıyoruz

# ----------------------------------------------------
# 1. KULLANICI (USER) ŞEMALARI (ÜSTE TAŞINDI!)
# ----------------------------------------------------
class UserCreateRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Kullanıcı adı (Örn: berfin_zozan)")
    email: str = Field(..., description="E-posta adresi (Örn: berfin@devtrack.com)")
    full_name: str | None = Field(default=None, description="Kullanıcının tam adı (Örn: Berfin Zozan İnanç)")

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    full_name: str | None
    created_at: datetime 

# ----------------------------------------------------
# 2. GÖREV (ISSUE) ŞEMALARI 
# ----------------------------------------------------
class IssueCreateRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Görevin başlığı")
    description: str = Field(..., min_length=10, description="Görevin detaylı açıklaması")
    assignee_id: str = Field(..., description="Görevin atandığı kullanıcının ID'si")
    due_date: Optional[datetime] = Field(default=None, description="Son teslim tarihi (opsiyonel)")

# İKİYE BÖLÜNMÜŞ SINIF TEK BİR ÇATI ALTINDA BİRLEŞTİRİLDİ
class IssueResponse(BaseModel):
    id: str
    title: str
    description: str
    assignee_id: str | None
    assignee: UserResponse | None = None  # Python artık UserResponse'u tanıyor çünkü üstte tanımladık!
    status: IssueStatus
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime] = None

class IssueUpdateRequest(BaseModel):
    # Alanların hepsi Optional çünkü kullanıcı sadece tek bir alanı güncellemek isteyebilir.
    title: Optional[str] = Field(default=None, min_length=3, max_length=100, description="Görevin başlığı")
    description: Optional[str] = Field(default=None, min_length=10, description="Görevin detaylı açıklaması")
    assignee_id: Optional[str] = Field(default=None, description="Görevin atandığı kullanıcının ID'si")
    status: Optional[IssueStatus] = Field(default=None, description="Görevin güncel durumu")
    due_date: Optional[datetime] = Field(default=None, description="Son teslim tarihi (opsiyonel)")