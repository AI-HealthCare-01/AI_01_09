from app.dtos.chat import ChatRequest, ChatResponse


class ChatService:
    async def process_chat(self, request: ChatRequest) -> ChatResponse:
        """
        사용자의 질문에 대해 LLM 또는 규칙 기반 챗봇의 응답을 생성합니다.
        질문 의도를 분류하고 응급 상황을 감지하는 로직을 포함합니다.

        Args:
            request (ChatRequest): 메시지 내역 및 세션 정보

        Returns:
            ChatResponse: 질문 분류, 위험도, 답변 및 멀티모달 에셋 링크
        """
        from openai import OpenAI  # type: ignore[import-not-found]

        from app.core import config

        client = OpenAI(api_key=config.OPENAI_API_KEY)

        recent_msg = request.messages[-1].content if request.messages else ""

        # 응급 키워드 감지
        emergency_keywords = ["숨", "가슴", "호흡곤란", "흉통", "의식", "어지러움", "경련"]
        is_emergency = any(keyword in recent_msg for keyword in emergency_keywords)

        if is_emergency:
            q_type = "증상"
            r_level = "Emergency"
            reply = "호흡곤란이나 흉통이 느껴지신다면 즉시 가까운 응급실을 방문하시거나 119에 연락하시기 바랍니다."
        else:
            # OpenAI API 호출
            system_prompt = """당신은 Cloud9 Care의 건강 상담 AI 비서입니다.
사용자의 복약 관리, 건강 상담, 증상 문의에 친절하고 정확하게 답변해주세요.
의학적 진단은 하지 말고, 필요시 전문의와 상담을 권유하세요.
답변은 간결하고 친근하게 작성해주세요."""

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": recent_msg},
                    ],
                    max_tokens=500,
                    temperature=0.7,
                )

                reply = response.choices[0].message.content

                # 질문 분류
                if any(word in recent_msg for word in ["약", "복용", "복약", "처방"]):
                    q_type = "복약"
                elif any(word in recent_msg for word in ["증상", "아프", "통증", "아픔"]):
                    q_type = "증상"
                else:
                    q_type = "일반"

                r_level = "Normal"

            except Exception:
                reply = "죄송합니다. 일시적인 오류가 발생했습니다. 다시 시도해주세요."
                q_type = "일반"
                r_level = "Normal"

        return ChatResponse(
            session_id=request.session_id or "new_session",
            question_type=q_type,
            risk_level=r_level,
            reply=reply,
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
