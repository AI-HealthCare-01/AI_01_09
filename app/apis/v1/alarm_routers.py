from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from app.dependencies.security import get_request_user
from app.models.user import User

alarm_router = APIRouter(prefix="/alarms", tags=["alarm"])

@alarm_router.get("")
async def get_alarms(
    user: Annotated[User, Depends(get_request_user)]
):
    """
    [ALARM] 복약 알람 목록 조회
    """
    return {"items": []}

@alarm_router.post("", status_code=status.HTTP_201_CREATED)
async def create_alarm(
    drug_name: str,
    alarm_time: str,
    user: Annotated[User, Depends(get_request_user)]
):
    """
    [ALARM] 복약 알람 생성
    """
    return {"id": 1}

@alarm_router.patch("/{id}")
async def update_alarm(
    id: int,
    user: Annotated[User, Depends(get_request_user)]
):
    """
    [ALARM] 복약 알람 수정
    """
    return {"detail": "수정되었습니다."}

@alarm_router.delete("/{id}")
async def delete_alarm(
    id: int,
    user: Annotated[User, Depends(get_request_user)]
):
    """
    [ALARM] 복약 알람 삭제
    """
    return {"detail": "삭제되었습니다."}

@alarm_router.get("/{id}/history")
async def get_alarm_history(
    id: int,
    user: Annotated[User, Depends(get_request_user)]
):
    """
    [ALARM] 복약 알람 발송/확인 이력 조회
    """
    return {"items": []}

@alarm_router.patch("/history/{id}")
async def confirm_alarm_history(
    id: int,
    user: Annotated[User, Depends(get_request_user)]
):
    """
    [ALARM] 복약 완료 체크
    """
    return {"detail": "복약 확인 되었습니다."}

@alarm_router.post("/history/{id}/confirm-link")
async def confirm_alarm_link(
    id: int,
    confirm_token: str
):
    """
    [ALARM] 카카오 버튼/링크 기반 복약완료 체크.
    """
    return {"detail": "복약 확인 완료"}