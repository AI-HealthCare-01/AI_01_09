from tortoise import fields, models

class SystemLog(models.Model):
    id = fields.IntField(pk=True)
    api_path = fields.CharField(max_length=255)
    method = fields.CharField(max_length=10)
    response_ms = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "system_logs"