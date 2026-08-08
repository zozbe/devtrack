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
    skip: int = 0, 
    limit: int = 100, 
    status: str | None = None,
    search: str | None = None,
    sort_by: str = "created_at", # YENİ PARAMETRE
    sort_order: str = "desc",    # YENİ PARAMETRE
    current_user: dict = Depends(get_current_user_token),
    issue_service: IssueService = Depends(get_issue_service)
):
    issues = issue_service.get_all_issues(
        skip=skip, limit=limit, status=status, search_query=search, sort_by=sort_by, sort_order=sort_order
    )
    return issues

@router.get("/me", response_model=list[IssueResponse])
async def get_my_issues(
    skip: int = 0, 
    limit: int = 100,
    status: str | None = None,
    search: str | None = None,
    sort_by: str = "created_at", # YENİ PARAMETRE
    sort_order: str = "desc",    # YENİ PARAMETRE
    current_user: dict = Depends(get_current_user_token),
    issue_service: IssueService = Depends(get_issue_service)
):
    user_id = current_user.get("id")
    my_issues = issue_service.get_my_issues(
        user_id, skip=skip, limit=limit, status=status, search_query=search, sort_by=sort_by, sort_order=sort_order
    )
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
    # KİM GÜNCELLİYOR? ID'sini alıyoruz
    user_id = current_user.get("id")
    
    # Şefe user_id'yi de gönderiyoruz
    updated_issue = issue_service.update_issue(issue_id, request, user_id)
    
    if not updated_issue:
        raise HTTPException(status_code=404, detail="Görev bulunamadı")
    return updated_issue

@router.delete("/{issue_id}", status_code=204)
async def delete_issue(
    issue_id: str, 
    current_user: dict = Depends(get_current_user_token),
    issue_service: IssueService = Depends(get_issue_service)
):
    # KİM SİLİYOR? ID'sini alıyoruz
    user_id = current_user.get("id")
    
    # Şefe user_id'yi de gönderiyoruz
    result = issue_service.delete_issue(issue_id, user_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Görev bulunamadı")
    return None