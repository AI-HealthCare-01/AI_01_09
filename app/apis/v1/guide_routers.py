from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies.security import get_request_user
from app.models.user import User

guide_router = APIRouter(prefix="/guides", tags=["guide"])


@guide_router.post("")
async def generate_guide(
    user: Annotated[User, Depends(get_request_user)],
    refresh: bool = False,
):
    """
    [GUIDE] 맞춤 가이드 생성(RAG 핵심).
    """
    return {
        "guide_id": 1,
        "guide_type": "복약",
        "user_current_status": "고혈압/타이레놀 복용 중",
        "generated_content": "가이드 내용...",
        "is_emergency_alert": False,
        "created_at": "2026-02-24T10:10:00",
    }


@guide_router.get("")
async def get_guides(user: Annotated[User, Depends(get_request_user)]):
    """
    [GUIDE] 가이드 목록 조회
    """
    return {"items": []}


@guide_router.get("/{id}")
async def get_guide_detail(id: int, user: Annotated[User, Depends(get_request_user)]):
    """
    [GUIDE] 가이드 상세 조회
    """
    return {"id": id, "guide_type": "복약"}


@guide_router.patch("/{id}")
async def update_guide(id: int, user: Annotated[User, Depends(get_request_user)]):
    """
    [GUIDE] 가이드 업데이트
    """
    return {"guide_id": id, "detail": "갱신되었습니다."}
