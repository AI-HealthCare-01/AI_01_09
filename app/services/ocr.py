from app.dtos.ocr import OCRExtractResponse, PillAnalyzeResponse


class OCRService:
    # ==========================================
    # [추가된 기능] 필수 3: OCR 기반 의료정보 인식
    # ==========================================
    async def extract_text_from_image(self, image_bytes: bytes) -> OCRExtractResponse:
        # TODO: 업로드된 이미지/PDF(처방전, 약봉투) 바이트에서 텍스트 자동 추출 처리
        dummy_text = "처방전 분석 결과: 타이레놀 1정 식후 30분 복용 (더미 데이터)"
        return OCRExtractResponse(extracted_text=dummy_text, confidence=0.95)

    # ==========================================
    # [추가된 기능] 선택 2: 이미지 분류 기반 복약 분석
    # ==========================================
    async def analyze_pill_image(self, image_bytes: bytes) -> PillAnalyzeResponse:
        # TODO: 약품 이미지를 분류 모델에 통과 시켜 약품명과 복약 기본 정보를 반환
        dummy_name = "테스트정"
        dummy_info = "진통소염제, 위장장애 주의 (더미 데이터)"
        return PillAnalyzeResponse(pill_name=dummy_name, medication_info=dummy_info, confidence=0.88)
