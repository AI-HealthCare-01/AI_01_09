from app.dtos.chat import ChatRequest, ChatResponse


class ChatService:
    # ==========================================
    # [추가된 기능] 필수 2: 실시간 챗봇
    # ==========================================
    async def process_chat(self, request: ChatRequest) -> ChatResponse:
        """
        사용자의 질문에 대해 LLM 또는 규칙 기반 챗봇의 응답을 생성합니다.
        질문 의도를 분류하고 응급 상황을 감지하는 로직을 포함합니다.

        Args:
            request (ChatRequest): 메시지 내역 및 세션 정보

        Returns:
            ChatResponse: 질문 분류, 위험도, 답변 및 멀티모달 에셋 링크
        """
        # TODO: 이전 대화 기록(request.messages)을 포함하여 LLM 또는 규칙 기반 챗봇 질의응답 처리
        # 1. 사용자 질문 의도 파악 (질문 분류: 복약/증상/일반/시스템)
        # 2. 응급 키워드 감지 (호흡곤란, 흉통 등)
        # 3. LLM 응답 생성 반환
        recent_msg = request.messages[-1].content if request.messages else ""

        # dummy classification & risk detection
        q_type = "일반"
        r_level = "Normal"
        if "숨" in recent_msg or "가슴" in recent_msg:
            q_type = "증상"
            r_level = "Emergency"
            dummy_reply = (
                "호흡곤란이나 흉통이 느껴지신다면 즉시 가까운 응급실을 방문하시거나 119에 연락하시기 바랍니다."
            )
        else:
            dummy_reply = f"챗봇 응답입니다. (받은 마지막 메시지: {recent_msg})"

        return ChatResponse(
            session_id=request.session_id or "new_dummy_session",
            question_type=q_type,
            risk_level=r_level,
            reply=dummy_reply,
            multimodal_assets=[],
        )

    async def stream_chat(self, request: ChatRequest):
        """
        챗봇의 응답을 토큰 단위로 실시간 스트리밍(SSE)하여 제공합니다.

        Args:
            request (ChatRequest): 메시지 내역 및 세션 정보

        Yields:
            str: SSE 형식의 JSON 데이터 문자열
        """
        import asyncio
        import json

        full_text = "이것은 실시간 스트리밍 응답 샘플입니다. 토큰 단위로 데이터가 전송됩니다."
        for word in full_text.split():
            yield f"data: {json.dumps({'text': word + ' '})}\n\n"
            await asyncio.sleep(0.1)
        yield "data: [DONE]\n\n"
