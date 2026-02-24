from tortoise import fields, models

class OCRResult(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="ocr_results") # 분석 결과의 소유자
    upload = fields.OneToOneField("models.Upload", related_name="ocr_result") # 원본 사진과의 1:1 연결 (증거 보존)
    raw_text = fields.TextField()                                    # 분석 전 가공되지 않은 텍스트
    standard_drug_name = fields.CharField(max_length=255)            # OCR로 추출된 약 이름 (REQ-OCR-002: 정규화된 이름)
    dosage_amount = fields.FloatField(null=True)                     # 1회 복용량 (숫자 데이터)
    dosage_unit = fields.CharField(max_length=20, null=True)          # REQ-OCR-003: mg, ml 등 단위 통일
    daily_frequency = fields.IntField(null=True)                     # 1일 복용 횟수
    duration_days = fields.IntField(null=True)                       # 총 복용 일수
    is_linked_to_meds = fields.BooleanField(default=False)           # REQ-OCR-004: 사용자가 'YES' 클릭 시 True로 변경

    class Meta:
        table = "ocr_results"