from app.dtos.ocr import DrugInfo, OCRExtractResponse, PillAnalyzeResponse, PillCandidate


class OCRService:
    # ==========================================
    # [추가된 기능] 필수 3: OCR 기반 의료정보 인식
    # ==========================================
    async def extract_text_from_image(self, image_bytes: bytes) -> OCRExtractResponse:
        """
        처방전 및 진료비 계산서 이미지에서 의료 텍스트를 추출하고 정규화합니다.
        병원명, 처방일자, 개별 약품명 및 복약 정보를 구조화하여 반환합니다.

        Args:
            image_bytes (bytes): 분석할 이미지 또는 PDF 바이너리 데이터

        Returns:
            OCRExtractResponse: 정규화된 의료 정보 및 추출된 약품 상세 리스트
        """
        # 1. 이미지/PDF에서 텍스트 자동 추출 (더미 로직)
        # 2. 정규화 처리 (mg/ml, YYYY-MM-DD)
        dummy_drugs = [
            DrugInfo(drug_name="타이레놀정500mg", dosage="500mg", frequency="1일 3회", duration="3"),
            DrugInfo(drug_name="아모디핀정", dosage="5mg", frequency="1일 1회", duration="30"),
        ]
        return OCRExtractResponse(
            hospital_name="서울대학교병원",
            prescribed_date="2024-02-24",
            drugs=dummy_drugs,
            extracted_text="[처방전] 서울대학교병원 ... 타이레놀정 500밀리그램 ...",
            confidence=0.98,
            multimodal_assets=[],
        )

    # ==========================================
    # [추가된 기능] 선택 2: 이미지 분류 기반 복약 분석 (CNN)
    # ==========================================
    async def analyze_pill_image(self, image_bytes: bytes) -> PillAnalyzeResponse:
        """
        단일 약품 이미지를 분석하여 CNN 모델 기반으로 약품명을 식별합니다.
        식별 신뢰도가 낮을 경우 재촬영 안내 메시지를 포함합니다.

        Args:
            image_bytes (bytes): 분석할 약품 사진 바이너리 데이터

        Returns:
            PillAnalyzeResponse: 식별된 후보군 리스트와 최적 후보 정보
        """
        # 1. CNN Transfer Learning 모델 기반 인식 (더미)
        # 2. 상위 3개 후보 추출 및 신뢰도 판단
        candidates = [
            PillCandidate(pill_name="타이레놀정500mg", confidence=0.85, medication_info="진통제"),
            PillCandidate(pill_name="에어탈정", confidence=0.10, medication_info="소염제"),
            PillCandidate(pill_name="노바스크정", confidence=0.03, medication_info="혈압약"),
        ]

        top = candidates[0]
        suggestion = None
        if top.confidence < 0.60:
            suggestion = "약품 인식 신뢰도가 낮습니다. 직접 입력하시거나 다시 촬영해 주세요."

        return PillAnalyzeResponse(
            candidates=candidates, top_candidate=top, suggestion=suggestion, multimodal_assets=[]
        )
