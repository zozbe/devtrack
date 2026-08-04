from fastapi import APIRouter, HTTPException, Depends
from api.schemas import IssueCreateRequest, IssueResponse, IssueUpdateRequest
from application.issue_service import IssueService
# GÜNCELLEME 1: get_issue_service import edildi
from api.dependencies import get_current_user_token, get_issue_service 
from domain.exceptions import IssueNotFoundException

router = APIRouter(prefix="/issues", tags=["Görevler (Issues)"])

@router.post("/", response_model=IssueResponse)
async def create_issue(
    request: IssueCreateRequest, 
    current_user: dict = Depends(get_current_user_token),
    issue_service: IssueService = Depends(get_issue_service) # GÜNCELLEME 2: Kurye şefi getirdi!
):
    # 1. GÜVENLİK: Yaka kartından (Token) kullanıcının GÜVENLİ ID'sini çekiyoruz
    user_id = current_user.get("id")
    
    # 2. Şefe siparişi ve siparişi verenin ID'sini iletiyoruz
    created_issue = issue_service.create_issue(request, user_id)
    return created_issue

@router.get("/", response_model=list[IssueResponse])
async def get_all_issues(
    current_user: dict = Depends(get_current_user_token),
    issue_service: IssueService = Depends(get_issue_service)
):
    issues = issue_service.get_all_issues()
    return issues

@router.get("/me", response_model=list[IssueResponse])
async def get_my_issues(
    current_user: dict = Depends(get_current_user_token),
    issue_service: IssueService = Depends(get_issue_service)
):
    # 1. Yaka kartından kullanıcının ID'sini okuyoruz
    user_id = current_user.get("id")
    
    # 2. Şefe sadece bu ID'ye ait görevleri getirmesini söylüyoruz
    my_issues = issue_service.get_my_issues(user_id)
    return my_issues

@router.get("/{issue_id}", response_model=IssueResponse)
async def get_issue(
    issue_id: str, 
    current_user: dict = Depends(get_current_user_token),
    issue_service: IssueService = Depends(get_issue_service)
):
    issue = issue_service.get_issue_by_id(issue_id)
    if issue is None:
        # ESKİ HALİ: raise HTTPException(status_code=404, detail="Aradığınız görev sistemde bulunamadı.")
        # YENİ VE KURUMSAL HALİ:
        raise IssueNotFoundException(issue_id=issue_id)
        
    return issue

@router.put("/{issue_id}", response_model=IssueResponse)
async def update_issue(
    issue_id: str, 
    request: IssueUpdateRequest, 
    current_user: dict = Depends(get_current_user_token),
    issue_service: IssueService = Depends(get_issue_service)
):
    updated_issue = issue_service.update_issue(issue_id, request)
    if updated_issue is None:
        raise HTTPException(status_code=404, detail="Güncellenmek istenen görev bulunamadı.")
    return updated_issue

@router.delete("/{issue_id}")
async def delete_issue(
    issue_id: str, 
    current_user: dict = Depends(get_current_user_token),
    issue_service: IssueService = Depends(get_issue_service)
):
    success = issue_service.delete_issue(issue_id)
    if not success:
        raise HTTPException(status_code=404, detail="Silinmek istenen görev bulunamadı.")
    return {"message": "Görev başarıyla silindi."}