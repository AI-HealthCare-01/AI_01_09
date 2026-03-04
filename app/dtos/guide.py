from pydantic import BaseModel, Field


# ==========================================
# [추가된 기능] 필수 1: LLM 기반 안내 가이드 생성
# ==========================================
class GuideRequest(BaseModel):
    user_id: str = Field(..., description="사용자 ID (이메일)")
    medical_records: str = Field(..., description="진료 기록 또는 증상 내용")
    medication_info: str = Field(..., description="현재 복용 중인 약품 정보")


class GuideResponse(BaseModel):
    id: int = Field(..., description="가이드 ID")
    guide_data: dict = Field(..., description="구조화된 가이드 데이터 (4개 섹션 포함)")
    created_at: str = Field(..., description="생성 일시")
    multimodal_assets: list[dict] | None = Field(None, description="카드뉴스/이미지/음성(TTS) 등 변환 에셋 정보")


class GuideHistoryResponse(BaseModel):
    guides: list[GuideResponse]
