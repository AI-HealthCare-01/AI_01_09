from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse as Response

from app.dtos.notification import ScheduleNotificationRequest, ScheduleNotificationResponse
from app.services.notification import NotificationService

notification_router = APIRouter(prefix="/notifications", tags=["notifications"])


# ==========================================
# [추가된 기능] 선택 3: 알림 기능
# ==========================================
@notification_router.post("/schedule", response_model=ScheduleNotificationResponse, status_code=status.HTTP_200_OK)
async def schedule_notification(
    request: ScheduleNotificationRequest,
    notification_service: Annotated[NotificationService, Depends(NotificationService)],
) -> Response:
    """
    사용자를 위해 복약 시간 및 가이드 확인 알림을 설정합니다.
    """
    response_dto = await notification_service.schedule_notification(request)
    return Response(content=response_dto.model_dump(), status_code=status.HTTP_200_OK)
