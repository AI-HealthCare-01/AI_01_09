from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse as Response

from app.dependencies.security import get_request_user
from app.dtos.guide import GuideRequest, GuideResponse
from app.services.guide import GuideService

guide_router = APIRouter(
    prefix="/guide", 
    tags=["guide"],
    dependencies=[Depends(get_request_user)]
)


# ==========================================
# [추가된 기능] 필수 1: LLM 기반 안내 가이드 생성
# ==========================================
@guide_router.post("/generate", response_model=GuideResponse, status_code=status.HTTP_200_OK)
async def generate_guide(
    request: GuideRequest,
    guide_service: Annotated[GuideService, Depends(GuideService)],
) -> Response:
    """
    사용자 진료 기록 및 복약 정보를 기반으로 맞춤형 가이드를 자동 생성합니다.
    
    Args:
        request (GuideRequest): 가이드 생성에 필요한 사용자 정보 및 OCR 요약
        guide_service (GuideService): 건강 가이드 서비스
        
    Returns:
        Response: 생성된 맞춤형 가이드 정보
    """
    response_dto = await guide_service.generate_guide(request)
    return Response(content=response_dto.model_dump(), status_code=status.HTTP_200_OK)

@guide_router.get("/history", status_code=status.HTTP_200_OK)
async def get_guide_history():
    """
    사용자의 전체 건강 가이드 생성 내역을 조회합니다.
    
    Returns:
        list: 가이드 내역 목록
    """
    from app.models.llm_life_guide import LLMLifeGuide
    return await LLMLifeGuide.all().order_by("-created_at")

@guide_router.get("/history/{id}", status_code=status.HTTP_200_OK)
async def get_guide_detail(id: int):
    """
    특정 가이드의 상세 내용과 멀티모달 에셋 정보를 조회합니다.
    
    Args:
        id (int): 상세 조회를 요청한 가이드 ID
        
    Returns:
        LLMLifeGuide: 가이드 상세 정보
    """
    from app.models.llm_life_guide import LLMLifeGuide
    return await LLMLifeGuide.filter(id=id).first()
