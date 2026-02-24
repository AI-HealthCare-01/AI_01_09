from tortoise import fields, models

class OCRHistory(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="ocr_histories")
    upload = fields.ForeignKeyField("models.Upload", related_name="ocr_histories") # Use ForeignKey to allow multiple attempts per upload if needed, or OneToOne if preferred.
    raw_text = fields.TextField(description="가공되지 않은 원본 텍스트")
    inference_metadata = fields.JSONField(null=True, description="추론 관련 메타데이터 (시간, 모델 버전 등)")
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "ocr_history"
