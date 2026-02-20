from typing import Annotated

from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.responses import JSONResponse as Response

from app.dtos.ocr import OCRExtractResponse, PillAnalyzeResponse
from app.services.ocr import OCRService

ocr_router = APIRouter(prefix="/ocr", tags=["ocr"])


# ==========================================
# [추가된 기능] 필수 3: OCR 기반 의료정보 인식
# ==========================================
@ocr_router.post("/extract_record", response_model=OCRExtractResponse, status_code=status.HTTP_200_OK)
async def extract_medical_record(
    ocr_service: Annotated[OCRService, Depends(OCRService)],
    file: UploadFile = File(...),
) -> Response:
    """
    처방전, 약봉투 등 이미지/PDF를 업로드하여 주요 텍스트 정보를 자동 추출합니다.
    """
    image_bytes = await file.read()
    response_dto = await ocr_service.extract_text_from_image(image_bytes)
    return Response(content=response_dto.model_dump(), status_code=status.HTTP_200_OK)


# ==========================================
# [추가된 기능] 선택 2: 이미지 분류 기반 복약 분석
# ==========================================
@ocr_router.post("/analyze_pill", response_model=PillAnalyzeResponse, status_code=status.HTTP_200_OK)
async def analyze_pill(
    ocr_service: Annotated[OCRService, Depends(OCRService)],
    file: UploadFile = File(...),
) -> Response:
    """
    약품 이미지를 통해 약품 종류를 인식하고, 기본 복약 정보를 제공합니다.
    """
    image_bytes = await file.read()
    response_dto = await ocr_service.analyze_pill_image(image_bytes)
    return Response(content=response_dto.model_dump(), status_code=status.HTTP_200_OK)
