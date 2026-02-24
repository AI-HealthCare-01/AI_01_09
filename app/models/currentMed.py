from tortoise import fields, models

class CurrentMed(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="current_meds") # 현재 복용 중인 확정된 약 목록 (N:1)
    medication_name = fields.CharField(max_length=255)               # 약품명 (OCR이나 알약 식별 YES 클릭 시 여기로 입력됨)
    added_from = fields.CharField(max_length=20)                     # 데이터 출처 구분 ("MANUAL", "OCR", "PILL_ID")
    start_date = fields.DateField(auto_now_add=True)                 # 복용 시작일

    class Meta:
        table = "current_meds"