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
    안내 텍스트 또는 처방 가이드를 음성(TTS) 파일로 변환합니다.
    
    Args:
        request (ConvertTTSRequest): 변환할 텍스트 및 관련 ID 정보
        media_service (MediaService): 미디어 변환 서비스
        
    Returns:
        Response: 생성된 오디오 파일 경로 및 메타데이터
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
    텍스트 기반 가이드를 시각적으로 보기 쉬운 카드뉴스 이미지 형태로 변환합니다.
    
    Args:
        request (ConvertCardnewsRequest): 변환할 가이드 텍스트 및 레이아웃 정보
        media_service (MediaService): 미디어 변환 서비스
        
    Returns:
        Response: 생성된 카드뉴스 이미지 경로 및 리스트
    """
    response_dto = await media_service.convert_text_to_cardnews(request)
    return Response(content=response_dto.model_dump(), status_code=status.HTTP_200_OK)
