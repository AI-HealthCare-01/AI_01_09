from pydantic import BaseModel, Field


# ==========================================
# [추가된 기능] 필수 1: LLM 기반 안내 가이드 생성
# ==========================================
class GuideRequest(BaseModel):
    user_id: int = Field(..., description="사용자 ID")
    medical_records: str = Field(..., description="진료 기록 또는 증상 내용")
    medication_info: str = Field(..., description="현재 복용 중인 약품 정보")


class GuideResponse(BaseModel):
    id: int = Field(..., description="가이드 ID")
    guide_type: str = Field(..., description="복약/생활/응급/방문권고")
    risk_level: str = Field(..., description="위험도 (Low, Medium, High, Emergency)")
    guide_text: str = Field(..., description="LLM이 생성한 맞춤형 가이드 텍스트")
    structured_content: dict = Field(..., description="사용자 프로필 및 OCR 요약 정보 (JSON 구조)")
    safety_disclaimer: str = Field(default="본 서비스의 결과는 의학적 전문 상담을 대체할 수 없으며, 정확한 판단을 위해 반드시 전문가와 상담하시기 바랍니다.")
    multimodal_assets: list[dict] | None = Field(None, description="카드뉴스/이미지/음성(TTS) 등 변환 에셋 정보")

class GuideHistoryResponse(BaseModel):
    guides: list[GuideResponse]
