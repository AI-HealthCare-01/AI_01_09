from tortoise import fields, models

class PillRecognition(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="pill_recognitions") # 분석 결과의 소유자
    front_upload = fields.OneToOneField("models.Upload", related_name="pill_front") # 약 앞면 사진 연결 (두 장 촬영 반영)
    back_upload = fields.OneToOneField("models.Upload", related_name="pill_back")   # 약 뒷면 사진 연결 (두 장 촬영 반영)
    pill_name = fields.CharField(max_length=255)                     # AI가 식별한 약 이름 (REQ-IMG-001)
    pill_description = fields.TextField()                            # 식별 도우미 (색상, 모양, 마크 등 설명문)
    confidence_score = fields.FloatField()                           # REQ-IMG-002: 0.6 미만 시 Fallback 로직용 신뢰도
    is_linked_to_meds = fields.BooleanField(default=False)           # "연동하시겠습니까?" YES 클릭 시 True

    class Meta:
        table = "pill_recognition"