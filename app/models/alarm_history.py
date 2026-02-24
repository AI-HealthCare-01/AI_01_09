from tortoise import fields, models

class AlarmHistory(models.Model):
    id = fields.IntField(pk=True)
    sent_at = fields.DatetimeField(auto_now_add=True)
<<<<<<< HEAD:app/models/alarm_history.py
    is_confirmed = fields.BooleanField(default=False) # 약 먹었음 체크 여부
    alarm = fields.ForeignKeyField("models.Alarm", related_name="histories")
=======
    is_confirmed = fields.BooleanField(default=False, description="복용 이름")                # 복약 완료 버튼 클릭 여부
>>>>>>> d6e51ba2c169e21bc320f74bba97c5fa8af7826c:app/models/alarmHistory.py

    class Meta:
        table = "alarm_history"