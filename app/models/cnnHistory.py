from tortoise import fields, models

class CNNHistory(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="cnn_histories")
    upload = fields.ForeignKeyField("models.Upload", related_name="cnn_histories")
    model_version = fields.CharField(max_length=50, null=True)
    class_name = fields.CharField(max_length=100, description="식별된 클래스명/약이름")
    confidence = fields.FloatField(description="신뢰도 점수")
    raw_result = fields.JSONField(null=True, description="추론 엔진의 전체 결과 데이터")
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "cnn_history"
