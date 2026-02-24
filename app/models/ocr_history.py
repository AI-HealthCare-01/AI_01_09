from tortoise import fields, models

class OCRHistory(models.Model):
    id = fields.IntField(pk=True)
    # [중요] 처방전 글자 혹은 알약 표면의 각인(문자/숫자) 원본 결과
    raw_text = fields.TextField()
    inference_metadata = fields.JSONField(null=True) # 분석 소요 시간, 모델 버전 등
    created_at = fields.DatetimeField(auto_now_add=True)
    upload = fields.ForeignKeyField("models.Upload", related_name="ocr_histories") # 어떤 이미지에서 읽었는가
    user = fields.ForeignKeyField("models.User", related_name="ocr_histories")

    class Meta:
        table = "ocr_history"
