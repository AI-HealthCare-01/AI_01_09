from app.dtos.notification import AlarmCreateRequest, AlarmResponse


class NotificationService:
    # ==========================================
    # [추가된 기능] 선택 3: 알림 기능
    # ==========================================
    async def create_alarm(self, request: AlarmCreateRequest) -> AlarmResponse:
        """
        사용자의 복약 시간 및 관련 알림 정보를 스케줄링하여 DB에 등록합니다.

        Args:
            request (AlarmCreateRequest): 알림 시간, 약품명 등의 요청 데이터

        Returns:
            AlarmResponse: 생성된 알림 정보 및 고유 ID
        """
        # TODO: 사용자의 복약 시간 및 가이드 확인 목적지 알림을 스케줄러(DB 저장 혹은 Redis Task 등)에 등록
        dummy_id = 12345
        return AlarmResponse(
            id=dummy_id, drug_name=request.drug_name, alarm_time=request.alarm_time, is_active=request.is_active
        )
