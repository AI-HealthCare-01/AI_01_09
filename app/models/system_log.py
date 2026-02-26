from tortoise import fields, models


class SystemLog(models.Model):
    """
    서비스 API의 성능 및 에러 여부를 모니터링하기 위한 로그 모델입니다.
    호출 경로, 메서드, 소요 시간(ms) 등을 기록합니다.
    """

    id = fields.IntField(pk=True)
    api_path = fields.CharField(max_length=255)
    method = fields.CharField(max_length=10)
    response_ms = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "system_logs"
