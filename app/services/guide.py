from app.dtos.guide import GuideRequest, GuideResponse


class GuideService:
    # ==========================================
    # [추가된 기능] 필수 1: LLM 기반 안내 가이드 생성
    # ==========================================
    async def generate_guide(self, request: GuideRequest) -> GuideResponse:
        # TODO: LLM 연동 또는 ai_worker 통신 로직 구현 (진료 기록 + 복약 정보 결합)
        # 1. request.medical_records와 request.medication_info를 바탕으로 프롬프트 생성
        # 2. AI 모델 기반 응답 생성
        dummy_text = f"사용자 {request.user_id}님을 위한 맞춤형 복약 및 생활습관 가이드입니다. (더미 데이터)"
        return GuideResponse(guide_text=dummy_text)
