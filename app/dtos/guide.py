from pydantic import BaseModel, Field


# ==========================================
# [추가된 기능] 필수 1: LLM 기반 안내 가이드 생성
# ==========================================
class GuideRequest(BaseModel):
    user_id: int = Field(..., description="사용자 ID")
    medical_records: str = Field(..., description="진료 기록 또는 증상 내용")
    medication_info: str = Field(..., description="현재 복용 중인 약품 정보")


class GuideResponse(BaseModel):
    guide_text: str = Field(..., description="LLM이 생성한 맞춤형 복약/생활습관 가이드 텍스트")
