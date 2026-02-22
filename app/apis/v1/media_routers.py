from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse as Response

from app.dtos.media import ConvertCardnewsRequest, ConvertCardnewsResponse, ConvertTTSRequest, ConvertTTSResponse
from app.services.media import MediaService

media_router = APIRouter(prefix="/media", tags=["media"])


# ==========================================
# [추가된 기능] 선택 1: 시각/음성 콘텐츠 변환 (음성)
# ==========================================
@media_router.post("/convert_tts", response_model=ConvertTTSResponse, status_code=status.HTTP_200_OK)
async def convert_tts(
    request: ConvertTTSRequest,
    media_service: Annotated[MediaService, Depends(MediaService)],
) -> Response:
    """
    생성된 안내 텍스트를 음성(TTS) 형태로 변환하여 제공합니다.
    """
    response_dto = await media_service.convert_text_to_audio(request)
    return Response(content=response_dto.model_dump(), status_code=status.HTTP_200_OK)


# ==========================================
# [추가된 기능] 선택 1: 시각/음성 콘텐츠 변환 (카드뉴스)
# ==========================================
@media_router.post("/convert_cardnews", response_model=ConvertCardnewsResponse, status_code=status.HTTP_200_OK)
async def convert_cardnews(
    request: ConvertCardnewsRequest,
    media_service: Annotated[MediaService, Depends(MediaService)],
) -> Response:
    """
    가이드 텍스트를 분석하여 카드뉴스 혹은 이미지 형태로 정보를 재생산합니다.
    """
    response_dto = await media_service.convert_text_to_cardnews(request)
    return Response(content=response_dto.model_dump(), status_code=status.HTTP_200_OK)
