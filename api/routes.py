from fastapi import APIRouter, HTTPException, Depends
from api.schemas import IssueCreateRequest, IssueResponse, IssueUpdateRequest
from application.issue_service import IssueService
from api.dependencies import get_current_user_token # 👮‍♂️ GÜVENLİK GÖREVLİMİZ GELDİ!

router = APIRouter(prefix="/issues", tags=["Görevler (Issues)"])

# Mutfağımızı (Servisimizi) kullanıma hazır hale getiriyoruz
issue_service = IssueService()

@router.post("/", response_model=IssueResponse)
async def create_issue(request: IssueCreateRequest, current_user: dict = Depends(get_current_user_token)):
    # Garson (API) sadece siparişi alır, mutfağa (Service) iletir ve sonucu döner.
    created_issue = issue_service.create_issue(request)
    return created_issue

@router.get("/", response_model=list[IssueResponse])
async def get_all_issues(current_user: dict = Depends(get_current_user_token)):
    # Garson (API), mutfaktan (Service) tüm görevleri ister ve müşteriye sunar.
    issues = issue_service.get_all_issues()
    return issues

# {issue_id} kullanımı, URL'den dinamik bir parametre alacağımızı belirtir (Path Parameter)
@router.get("/{issue_id}", response_model=IssueResponse)
async def get_issue(issue_id: str, current_user: dict = Depends(get_current_user_token)):
    # 1. Mutfağa soruyoruz
    issue = issue_service.get_issue_by_id(issue_id)
    
    # 2. Eğer mutfak "Böyle bir görev yok" (None) derse, kullanıcıya 404 dönüyoruz.
    if issue is None:
        raise HTTPException(status_code=404, detail="Aradığınız görev sistemde bulunamadı.")
    
    # 3. Varsa direkt gönderiyoruz.
    return issue

# Güncelleme işlemleri için HTTP standardı PUT veya PATCH metodudur
@router.put("/{issue_id}", response_model=IssueResponse)
async def update_issue(issue_id: str, request: IssueUpdateRequest, current_user: dict = Depends(get_current_user_token)):
    updated_issue = issue_service.update_issue(issue_id, request)
    
    if updated_issue is None:
        raise HTTPException(status_code=404, detail="Güncellenmek istenen görev bulunamadı.")
        
    return updated_issue

# Silme işlemleri için HTTP standardı DELETE metodudur
@router.delete("/{issue_id}")
async def delete_issue(issue_id: str, current_user: dict = Depends(get_current_user_token)):
    success = issue_service.delete_issue(issue_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Silinmek istenen görev bulunamadı.")
        
    return {"message": "Görev başarıyla silindi."}