from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from app.dependencies.security import get_request_user
from app.models.user import User

chat_router = APIRouter(prefix="/chat", tags=["chat"])

@chat_router.post("/message")
async def send_chat_message(
    user: Annotated[User, Depends(get_request_user)],
    message: str,
    session_id: str | None = None,
    reference_guide_id: int | None = None,
):
    """
    [CHAT] 챗봇 메시지 전송(세션 유지).
    """
    return {
        "session_id": session_id or "new_session_123",
        "assistant_message": "안녕하세요. 무엇을 도와드릴까요?",
        "action_type": "NONE"
    }

@chat_router.post("/end")
async def end_chat(
    session_id: str,
    user: Annotated[User, Depends(get_request_user)]
):
    """
    [CHAT] 채팅 종료(대화 내용 초기화).
    """
    return {"detail": "채팅이 종료되었습니다."}
