from app.dtos.guide import GuideRequest, GuideResponse


class GuideService:
    # ==========================================
    # [추가된 기능] 필수 1: LLM 기반 안내 가이드 생성
    # ==========================================
    async def generate_guide(self, request: GuideRequest) -> GuideResponse:
        """
        사용자의 진료/복약 상세 정보를 결합하여 맞춤형 건강 가이드를 생성합니다.
        멀티모달 에셋 생성을 위한 기본 메타데이터를 포함합니다.
        
        Args:
            request (GuideRequest): 사용자 ID 및 의료 정보 (진료 기록, 복약 정보 등)
            
        Returns:
            GuideResponse: 생성된 가이드 텍스트, 분류, 위험도 및 구조화된 요약 정보
        """
        # TODO: LLM 연동 또는 ai_worker 통신 로직 구현 (진료 기록 + 복약 정보 결합)
        # 1. request.medical_records와 request.medication_info를 바탕으로 프롬프트 생성
        # 2. AI 모델 기반 응답 생성
        dummy_text = f"사용자 {request.user_id}님을 위한 맞춤형 복약 및 생활습관 가이드입니다. (더미 데이터)"
        return GuideResponse(
            id=999,
            guide_type="복약",
            risk_level="Low",
            guide_text=dummy_text,
            structured_content={
                "profile_summary": "30대 남성, 기저 질환 없음",
                "ocr_summary": "감기약 (항생제/소염제)",
                "warnings": ["부작용 주의", "술 금지"]
            },
            multimodal_assets=[]
        )
