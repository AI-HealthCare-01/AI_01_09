from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse as Response
from pydantic import BaseModel

from app.dependencies.security import get_request_user
from app.dtos.chat import ChatRequest
from app.models.user import User
from app.services.chat import ChatService

chat_router = APIRouter(prefix="/chat", tags=["chat"])


class ChatMessageRequest(BaseModel):
    message: str
    session_id: str | None = None


@chat_router.post("/message", response_model=dict)
async def send_chat_message(
    request: ChatMessageRequest,
) -> Response:
    """
    [CHAT] 챗봇 메시지 전송(세션 유지) - 비로그인 상태에서도 사용 가능.
    """
    chat_service = ChatService()

    # ChatRequest 객체 생성
    from app.dtos.chat import ChatMessage

    chat_request = ChatRequest(
        user_id="guest",  # 비로그인 사용자
        session_id=request.session_id,
        messages=[ChatMessage(role="user", content=request.message)],
    )

    # 챗봇 처리
    response = await chat_service.process_chat(chat_request)

    return Response(
        content={
            "session_id": response.session_id,
            "assistant_message": response.reply,
            "action_type": response.risk_level,
            "question_type": response.question_type,
        }
    )


@chat_router.post("/end")
async def end_chat(session_id: str, user: Annotated[User, Depends(get_request_user)]) -> Response:
    """
    [CHAT] 채팅 종료(대화 내용 초기화).
    """
    return Response(content={"detail": "채팅이 종료되었습니다."})
