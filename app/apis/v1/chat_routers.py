from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse as Response

from app.dependencies.security import get_request_user
from app.dtos.chat import ChatRequest, ChatResponse
from app.models.user import User
from app.services.chat import ChatService

chat_router = APIRouter(prefix="/chat", tags=["chat"])


@chat_router.post("/message", response_model=dict)
async def send_chat_message(
    user: Annotated[User, Depends(get_request_user)],
    message: str,
    session_id: str | None = None,
) -> Response:
    """
    [CHAT] 챗봇 메시지 전송(세션 유지).
    """
    chat_service = ChatService()
    
    # ChatRequest 객체 생성
    from app.dtos.chat import ChatMessage
    chat_request = ChatRequest(
        user_id=user.id,
        session_id=session_id,
        messages=[ChatMessage(role="user", content=message)]
    )
    
    # 챗봇 처리
    response = await chat_service.process_chat(chat_request)
    
    return Response(content={
        "session_id": response.session_id,
        "assistant_message": response.reply,
        "action_type": response.risk_level,
        "question_type": response.question_type,
    })


@chat_router.post("/end")
async def end_chat(session_id: str, user: Annotated[User, Depends(get_request_user)]) -> Response:
    """
    [CHAT] 채팅 종료(대화 내용 초기화).
    """
    return Response(content={"detail": "채팅이 종료되었습니다."})
