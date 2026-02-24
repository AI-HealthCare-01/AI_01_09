from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse as Response

from app.dependencies.security import get_request_user
from app.dtos.chat import ChatRequest, ChatResponse
from app.services.chat import ChatService

chat_router = APIRouter(
    prefix="/chat", 
    tags=["chat"],
    dependencies=[Depends(get_request_user)]
)


# ==========================================
# [추가된 기능] 필수 2: 실시간 챗봇
# ==========================================
@chat_router.post("/message", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def process_chat_message(
    request: ChatRequest,
    chat_service: Annotated[ChatService, Depends(ChatService)],
) -> Response:
    """
    이전 대화 맥락을 포함하여 실시간 챗봇(LLM) 응답을 제공합니다. (단일 응답)
    
    Args:
        request (ChatRequest): 대화 세션 ID 및 메시지 내용
        chat_service (ChatService): 챗봇 서비스
        
    Returns:
        Response: 챗봇 응답 데이터
    """
    response_dto = await chat_service.process_chat(request)
    return Response(content=response_dto.model_dump(), status_code=status.HTTP_200_OK)

@chat_router.post("/message/stream")
async def process_chat_stream(
    request: ChatRequest,
    chat_service: Annotated[ChatService, Depends(ChatService)],
):
    """
    실시간 토큰 단위 Streaming 응답을 제공합니다. (SSE)
    
    Args:
        request (ChatRequest): 대화 세션 ID 및 메시지 내용
        chat_service (ChatService): 챗봇 서비스
        
    Returns:
        StreamingResponse: 실시간 텍스트 스트림
    """
    from fastapi.responses import StreamingResponse
    return StreamingResponse(
        chat_service.stream_chat(request),
        media_type="text/event-stream"
    )

@chat_router.get("/sessions", status_code=status.HTTP_200_OK)
async def get_chat_sessions():
    """
    현재 사용자의 전체 대화 세션 목록을 조회합니다.
    
    Returns:
        list: 세션 ID 목록
    """
    from app.models.chat_message import ChatMessage
    # session_id별로 그루핑하여 최신 메시지 하나씩 보여주는 로직이 필요하나
    # 여기서는 간단히 전체 세션 ID 목록을 반환하는 플레이스홀더로 작성
    return await ChatMessage.all().distinct().values("session_id")

@chat_router.get("/sessions/{id}", status_code=status.HTTP_200_OK)
async def get_chat_history(id: str):
    """
    특정 세션의 전체 대화 내역을 조회합니다.
    
    Args:
        id (str): 조회를 요청한 세션 ID
        
    Returns:
        list: 대화 메시지 내역 목록
    """
    from app.models.chat_message import ChatMessage
    return await ChatMessage.filter(session_id=id).order_by("created_at")
