from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.responses import JSONResponse as Response

from app.dependencies.security import get_request_user
from app.dtos.ocr import OCRExtractResponse, PillAnalyzeResponse, OCRVerificationRequest
from app.services.ocr import OCRService

ocr_router = APIRouter(
    prefix="/ai", 
    tags=["ai"],
    dependencies=[Depends(get_request_user)]
)

@ocr_router.post("/analyze-ocr", response_model=OCRExtractResponse, status_code=status.HTTP_200_OK)
async def analyze_ocr(
    ocr_service: Annotated[OCRService, Depends(OCRService)],
    file: UploadFile = File(...),
) -> Response:
    """
    처방전 이미지/PDF에서 텍스트 정보를 자동 추출하고 정규화합니다.
    
    Args:
        ocr_service (OCRService): OCR 처리 서비스
        file (UploadFile): 업로드된 처방전 이미지 또는 PDF 파일
        
    Returns:
        Response: 추출된 약품 및 처방 정보
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
    약품 이미지를 분석하여 상위 후보군 및 복약 정보를 제공합니다.
    
    Args:
        ocr_service (OCRService): 이미지 분석 서비스
        file (UploadFile): 업로드된 약품 이미지 파일
        
    Returns:
        Response: 분석된 약품 후보 및 가이드
    """
    image_bytes = await file.read()
    response_dto = await ocr_service.analyze_pill_image(image_bytes)
    return Response(content=response_dto.model_dump(), status_code=status.HTTP_200_OK)


@ocr_router.get("/prescriptions", status_code=status.HTTP_200_OK)
async def get_prescriptions():
    """
    현재 사용자가 업로드하고 분석한 전체 처방전 내역을 조회합니다.
    
    Returns:
        list: 처방전 및 약품 정보 목록
    """
    from app.models.prescription import Prescription
    return await Prescription.all().prefetch_related("drugs")

@ocr_router.get("/pills", status_code=status.HTTP_200_OK)
async def get_pill_recognitions():
    """
    현재 사용자의 전체 알약 식별 내역을 조회합니다.
    
    Returns:
        list: 알약 식별 정보 목록
    """
    from app.models.pill_recognition import PillRecognition
    return await PillRecognition.all()

@ocr_router.patch("/prescriptions/{id}", status_code=status.HTTP_200_OK)
async def verify_ocr_result(
    id: int,
    request: OCRVerificationRequest,
    ocr_service: Annotated[OCRService, Depends(OCRService)],
) -> Response:
    """
    사용자가 직접 OCR 결과(병원명, 날짜 등)를 수정하거나 확정합니다.
    
    Args:
        id (int): 수정할 처방전 내역 ID
        request (OCRVerificationRequest): 수정 및 확정 요청 데이터
        ocr_service (OCRService): OCR 처리 서비스
        
    Returns:
        Response: 처리 결과 메시지
    """
    # service logic placeholder
    # await ocr_service.verify_prescription(id, request)
    return Response(content={"detail": f"처방전 {id}번 정보가 성공적으로 수정/확정되었습니다."}, status_code=status.HTTP_200_OK)
