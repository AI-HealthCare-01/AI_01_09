from app.dtos.chat import ChatRequest, ChatResponse


class ChatService:
    # ==========================================
    # [추가된 기능] 필수 2: 실시간 챗봇
    # ==========================================
    async def process_chat(self, request: ChatRequest) -> ChatResponse:
        # TODO: 이전 대화 기록(request.messages)을 포함하여 LLM 또는 규칙 기반 챗봇 질의응답 처리
        # 1. 사용자 질문 의도 파악
        # 2. LLM 응답 생성 반환
        recent_msg = request.messages[-1].content if request.messages else ""
        dummy_reply = f"챗봇 응답입니다. (받은 마지막 메시지: {recent_msg})"
        return ChatResponse(reply=dummy_reply)
