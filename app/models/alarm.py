from tortoise import fields, models

class Alarm(models.Model):
    id = fields.IntField(pk=True)
    drug_name = fields.CharField(max_length=255)
    alarm_time = fields.TimeField()
    is_active = fields.BooleanField(default=True)
    user = fields.ForeignKeyField("models.User", related_name="alarms")

    class Meta:
        table = "alarms"