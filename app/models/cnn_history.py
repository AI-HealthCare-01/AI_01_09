from tortoise import fields, models

class CNNHistory(models.Model):
    id = fields.IntField(pk=True)
    model_version = fields.CharField(max_length=50, null=True)
    # [중요] 알약의 외형(모양/색상) 기반 분류 명칭
    class_name = fields.CharField(max_length=100)
    confidence = fields.FloatField()               # AI의 확신도 (예: 0.98)
    raw_result = fields.JSONField(null=True)       # 분석 엔진의 전체 결과 데이터
    created_at = fields.DatetimeField(auto_now_add=True)
    upload = fields.ForeignKeyField("models.Upload", related_name="cnn_histories")
    user = fields.ForeignKeyField("models.User", related_name="cnn_histories")

    class Meta:
        table = "cnn_history"
