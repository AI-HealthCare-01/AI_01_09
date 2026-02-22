from datetime import datetime

from pydantic import BaseModel, Field


# ==========================================
# [추가된 기능] 선택 3: 알림 기능
# ==========================================
class ScheduleNotificationRequest(BaseModel):
    user_id: int = Field(..., description="사용자 ID")
    title: str = Field(..., description="알림 제목 (예: 복약 시간 알림)")
    message: str = Field(..., description="알림 내용")
    schedule_time: datetime = Field(..., description="알림을 발송할 예정 시간")


class ScheduleNotificationResponse(BaseModel):
    notification_id: int = Field(..., description="등록된 알림 ID")
    status: str = Field(..., description="등록 상태 (예: scheduled)")
