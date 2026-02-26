from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies.security import get_request_user
from app.models.user import User

medication_router = APIRouter(tags=["medication"])


@medication_router.patch("/medications/confirm/drug/{id}")
async def confirm_drug(id: int, user: Annotated[User, Depends(get_request_user)]):
    """
    [CONFIRM] 처방전 약물 승인.
    """
    return {"detail": "승인되었습니다.", "current_meds_id": 1001}


@medication_router.patch("/medications/confirm/pill/{id}")
async def confirm_pill(id: int, user: Annotated[User, Depends(get_request_user)]):
    """
    [CONFIRM] 알약 인식 승인.
    """
    return {"detail": "승인되었습니다.", "current_meds_id": 1002}


@medication_router.get("/current-meds")
async def get_current_meds(user: Annotated[User, Depends(get_request_user)]):
    """
    [MEDS] 현재 복용약 목록 조회(RAG 핵심 소스)
    """
    return {"items": []}


@medication_router.post("/current-meds", status_code=status.HTTP_201_CREATED)
async def create_current_med(medication_name: str, user: Annotated[User, Depends(get_request_user)]):
    """
    [MEDS] 현재 복용약 수기 등록
    """
    return {"id": 1003}


@medication_router.delete("/current-meds/{id}")
async def delete_current_med(id: int, user: Annotated[User, Depends(get_request_user)]):
    """
    [MEDS] 현재 복용약 삭제
    """
    return {"detail": "삭제되었습니다."}
