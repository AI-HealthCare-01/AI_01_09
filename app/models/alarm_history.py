from tortoise import fields, models

class AlarmHistory(models.Model):
    id = fields.IntField(pk=True)
    sent_at = fields.DatetimeField(auto_now_add=True)
    is_confirmed = fields.BooleanField(default=False) # 약 먹었음 체크 여부
    alarm = fields.ForeignKeyField("models.Alarm", related_name="histories")

    class Meta:
        table = "alarm_history"