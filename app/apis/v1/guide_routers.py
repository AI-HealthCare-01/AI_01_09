from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse as Response

from app.dtos.guide import GuideRequest, GuideResponse
from app.services.guide import GuideService

guide_router = APIRouter(prefix="/guide", tags=["guide"])


# ==========================================
# [추가된 기능] 필수 1: LLM 기반 안내 가이드 생성
# ==========================================
@guide_router.post("/generate", response_model=GuideResponse, status_code=status.HTTP_200_OK)
async def generate_guide(
    request: GuideRequest,
    guide_service: Annotated[GuideService, Depends(GuideService)],
) -> Response:
    """
    사용자 진료 기록 및 복약 정보를 기반으로 맞춤형 복약/생활습관 가이드를 자동 생성합니다.
    """
    response_dto = await guide_service.generate_guide(request)
    return Response(content=response_dto.model_dump(), status_code=status.HTTP_200_OK)
