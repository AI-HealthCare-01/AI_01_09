from tortoise import fields, models

class Alarm(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="alarms")
    drug_name = fields.CharField(max_length=255, description="알약 이름")
    alarm_time = fields.TimeField(description="날짜/시간")        # REQ-ALERT-001: 시간 및 기간 설정 DB 저장
    is_active = fields.BooleanField(default=True, description="알람 여부")

    class Meta:
        table = "alarms"