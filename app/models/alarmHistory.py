from tortoise import fields, models

class AlarmHistory(models.Model):                                    # REQ-ALERT-002: 복약 확인 로그 (cron 기반 관리)
    id = fields.IntField(pk=True)
    alarm = fields.ForeignKeyField("models.Alarm", related_name="histories")
    sent_at = fields.DatetimeField(auto_now_add=True)
    is_confirmed = fields.BooleanField(default=False, description="복용 이름")                # 복약 완료 버튼 클릭 여부

    class Meta:
        table = "alarm_history"