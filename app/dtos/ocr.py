
from pydantic import BaseModel, Field


# ==========================================
# [추가된 기능] 필수 3 & 선택 2: OCR 및 약품 이미지 분석
# ==========================================
class OCRExtractResponse(BaseModel):
    extracted_text: str = Field(..., description="이미지/PDF에서 추출된 텍스트")
    confidence: float = Field(..., description="OCR 인식 신뢰도")


class PillAnalyzeResponse(BaseModel):
    pill_name: str = Field(..., description="인식된 약품 이름")
    medication_info: str = Field(..., description="기본 복약 정보 (용법, 부작용 등)")
    confidence: float = Field(..., description="분류 모델 인식 신뢰도")
