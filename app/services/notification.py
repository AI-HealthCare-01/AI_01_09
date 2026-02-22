from app.dtos.notification import ScheduleNotificationRequest, ScheduleNotificationResponse


class NotificationService:
    # ==========================================
    # [추가된 기능] 선택 3: 알림 기능
    # ==========================================
    async def schedule_notification(self, request: ScheduleNotificationRequest) -> ScheduleNotificationResponse:
        # TODO: 사용자의 복약 시간 및 가이드 확인 목적지 알림을 스케줄러(DB 저장 혹은 Redis Task 등)에 등록
        dummy_id = 12345
        return ScheduleNotificationResponse(notification_id=dummy_id, status="scheduled")
