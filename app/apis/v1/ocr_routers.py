from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.responses import JSONResponse as Response

from app.dtos.ocr import OCRExtractResponse, PillAnalyzeResponse
from app.services.ocr import OCRService

ocr_router = APIRouter(prefix="/ai", tags=["ai"])

@ocr_router.post("/analyze-ocr", response_model=OCRExtractResponse, status_code=status.HTTP_200_OK)
async def analyze_ocr(
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
@ocr_router.post("/analyze-pill", response_model=PillAnalyzeResponse, status_code=status.HTTP_200_OK)
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


@ocr_router.get("/prescriptions", status_code=status.HTTP_200_OK)
async def get_prescriptions():
    """
    저장된 처방전 내역을 가져옵니다.
    """
    from app.models.prescription import Prescription
    return await Prescription.all().prefetch_related("drugs")

@ocr_router.get("/pills", status_code=status.HTTP_200_OK)
async def get_pill_recognitions():
    """
    저장된 알약 식별 내역을 가져옵니다.
    """
    from app.models.pill_recognition import PillRecognition
    return await PillRecognition.all()
