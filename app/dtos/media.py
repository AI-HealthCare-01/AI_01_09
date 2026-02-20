from pydantic import BaseModel, Field


# ==========================================
# [추가된 기능] 선택 1: 시각/음성 콘텐츠 변환
# ==========================================
class ConvertTTSRequest(BaseModel):
    text: str = Field(..., description="음성으로 변환할 텍스트 가이드")


class ConvertTTSResponse(BaseModel):
    audio_url: str = Field(..., description="생성된 음성 파일(TTS)의 다운로드/재생 URL")


class ConvertCardnewsRequest(BaseModel):
    text: str = Field(..., description="카드뉴스로 변환할 안내 텍스트")


class ConvertCardnewsResponse(BaseModel):
    image_urls: list[str] = Field(..., description="생성된 카드뉴스 이미지들의 URL 목록")
