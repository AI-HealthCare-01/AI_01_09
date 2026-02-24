from tortoise import fields, models

class SystemLog(models.Model):                                       # NFR-PERF-001: 5초 이내 응답 모니터링 (응답 속도 측정)
    id = fields.IntField(pk=True)
    api_path = fields.CharField(max_length=255)
    method = fields.CharField(max_length=10)
    response_ms = fields.IntField()                                  # 응답 속도 측정
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "system_logs"