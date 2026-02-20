from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse as Response

from app.dtos.chat import ChatRequest, ChatResponse
from app.services.chat import ChatService

chat_router = APIRouter(prefix="/chat", tags=["chat"])


# ==========================================
# [추가된 기능] 필수 2: 실시간 챗봇
# ==========================================
@chat_router.post("/message", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def process_chat_message(
    request: ChatRequest,
    chat_service: Annotated[ChatService, Depends(ChatService)],
) -> Response:
    """
    이전 대화 맥락을 포함하여 실시간 챗봇(LLM) 응답을 제공합니다.
    """
    response_dto = await chat_service.process_chat(request)
    return Response(content=response_dto.model_dump(), status_code=status.HTTP_200_OK)
