from tortoise import fields, models


class CurrentMed(models.Model):
    """
    사용자가 현재 실제로 복용 중인 약물 목록을 관리하는 모델입니다.
    처방전 분석 또는 직접 입력을 통해 등록되며 AI 가이드 생성의 핵심 소스입니다.
    """

    id = fields.IntField(pk=True)
    # 승인된 약물 이름 (여기 데이터가 RAG의 핵심 소스)
    medication_name = fields.CharField(max_length=255)
    added_from = fields.CharField(max_length=20)  # 출처 (OCR_PRESCRIPTION, PILL_SCAN 등)
    start_date = fields.DateField()  # 복용 시작 시점
    user = fields.ForeignKeyField("models.User", related_name="current_meds")

    class Meta:
        table = "current_meds"
