from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse as Response

from app.dependencies.security import get_request_user
from app.dtos.notification import AlarmCreateRequest, AlarmResponse
from app.services.notification import NotificationService
from app.models.alarm_history import AlarmHistory
from app.models.alarm import Alarm

notification_router = APIRouter(
    prefix="/notifications", 
    tags=["notifications"],
    dependencies=[Depends(get_request_user)]
)


# ==========================================
# [추가된 기능] 선택 3: 알림 기능
# ==========================================
@notification_router.post("/schedule", response_model=AlarmResponse, status_code=status.HTTP_201_CREATED)
async def schedule_notification(
    request: AlarmCreateRequest,
    notification_service: Annotated[NotificationService, Depends(NotificationService)],
) -> Response:
    """
    사용자의 복약 알림 시간 및 내용을 설정합니다.
    
    Args:
        request (AlarmCreateRequest): 알람 시간 및 약품 정보
        notification_service (NotificationService): 알림 서비스
        
    Returns:
        Response: 생성된 알람 정보
    """
    response_dto = await notification_service.create_alarm(request)
    return Response(content=response_dto.model_dump(), status_code=status.HTTP_201_CREATED)


@notification_router.get("/", status_code=status.HTTP_200_OK)
async def get_notifications():
    """
    현재 사용자의 전체 복약 알림 목록을 조회합니다.
    
    Returns:
        list: 활성/비활성 알람 목록
    """
    return await Alarm.all().order_by("-id")

@notification_router.patch("/{id}", status_code=status.HTTP_200_OK)
async def toggle_alarm(id: int):
    """
    특정 알람의 활성화 또는 비활성화 상태를 토글합니다.
    
    Args:
        id (int): 상태를 변경할 알람 ID
        
    Returns:
        dict: 변경된 상태 확인 메시지
    """
    alarm = await Alarm.get(id=id)
    alarm.is_active = not alarm.is_active
    await alarm.save()
    return {"detail": f"알람 {id}번 상태가 {'활성화' if alarm.is_active else '비활성화'}되었습니다."}

@notification_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alarm(id: int):
    """
    특정 복약 알람을 삭제합니다.
    
    Args:
        id (int): 삭제할 알람 ID
        
    Returns:
        Response: 빈 응답 (204)
    """
    alarm = await Alarm.get(id=id)
    await alarm.delete()
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)

@notification_router.post("/{id}/confirm", status_code=status.HTTP_200_OK)
async def confirm_medication(id: int):
    """
    사용자가 특정 알람 시간에 약을 실제 복용했음을 기록합니다.
    
    Args:
        id (int): 복용 확인을 요청한 알람 ID
        
    Returns:
        dict: 확인 완료 메시지
    """
    # 복용 내역 기록
    await AlarmHistory.create(alarm_id=id, is_confirmed=True)
    return {"detail": "복약 확인이 기록되었습니다."}
