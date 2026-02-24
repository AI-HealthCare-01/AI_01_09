from tortoise import fields, models

class CurrentMed(models.Model):
    id = fields.IntField(pk=True)
    # 승인된 약물 이름 (여기 데이터가 RAG의 핵심 소스)
    medication_name = fields.CharField(max_length=255)
    added_from = fields.CharField(max_length=20) # 출처 (OCR_PRESCRIPTION, PILL_SCAN 등)
    start_date = fields.DateField()              # 복용 시작 시점
    user = fields.ForeignKeyField("models.User", related_name="current_meds")

    class Meta:
        table = "current_meds"