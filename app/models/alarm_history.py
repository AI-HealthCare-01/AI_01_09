from tortoise import fields, models

class AlarmHistory(models.Model):
    """
    실제 발송된 알림 내역과 사용자의 복약 확인 여부를 기록하는 모델입니다.
    복약 순응도 분석의 기초 데이터로 활용됩니다.
    """
    id = fields.IntField(pk=True)
    sent_at = fields.DatetimeField(auto_now_add=True)
    is_confirmed = fields.BooleanField(default=False) # 약 먹었음 체크 여부
    alarm = fields.ForeignKeyField("models.Alarm", related_name="histories")

    class Meta:
        table = "alarm_history"
