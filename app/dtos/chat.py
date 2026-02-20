from pydantic import BaseModel, Field


# ==========================================
# [추가된 기능] 필수 2: 실시간 챗봇
# ==========================================
class ChatMessage(BaseModel):
    role: str = Field(..., description="system, user, assistant 중 하나")
    content: str = Field(..., description="대화 내용")


class ChatRequest(BaseModel):
    user_id: int = Field(..., description="사용자 ID")
    messages: list[ChatMessage] = Field(..., description="이전 대화 맥락을 포함한 메시지 목록")


class ChatResponse(BaseModel):
    reply: str = Field(..., description="챗봇(LLM)의 실시간 응답 내용")
