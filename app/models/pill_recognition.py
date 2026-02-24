from tortoise import fields, models

class PillRecognition(models.Model):
    id = fields.IntField(pk=True)
    # CNN(외형)과 OCR(각인)을 조합해 도출한 최종 이름
    pill_name = fields.CharField(max_length=255)
    pill_description = fields.TextField() # 약의 상세 효능 및 주의사항
    # [핵심] 사용자가 내 약이 맞다고 승인 시 True로 변경
    is_linked_to_meds = fields.BooleanField(default=False)
    user = fields.ForeignKeyField("models.User", related_name="pill_recognitions")
    
    # 분석 근거 추적을 위한 연결 (0번 수정사항 반영)
    cnn_history = fields.ForeignKeyField("models.CNNHistory", related_name="pill_recognitions")
    ocr_history = fields.ForeignKeyField("models.OCRHistory", related_name="pill_recognitions")
    
    # 앞/뒷면 사진 매칭
    front_upload = fields.OneToOneField("models.Upload", related_name="pill_front_asset")
    back_upload = fields.OneToOneField("models.Upload", related_name="pill_back_asset")

    class Meta:
        table = "pill_recognition"