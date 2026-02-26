from tortoise import fields, models


class Alarm(models.Model):
    """
    사용자가 설정한 정기적인 복약 알림 정보를 관리하는 모델입니다.
    특정 약품명과 알림 시간을 포함하며 활성/비활성 상태를 가집니다.
    """

    id = fields.IntField(pk=True)
    drug_name = fields.CharField(max_length=255)
    alarm_time = fields.TimeField()
    is_active = fields.BooleanField(default=True)
    user = fields.ForeignKeyField("models.User", related_name="alarms")

    class Meta:
        table = "alarms"
