from tortoise import fields, models

class Upload(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="uploads") # 업로드 주체
    file_url = fields.CharField(max_length=512)                      # S3 등 스토리지에 저장된 이미지 경로
    file_type = fields.CharField(max_length=20)                      # JPG, PNG, PDF 구분 (REQ-OCR-001)
    category = fields.CharField(max_length=50)                       # 용도 구분 ("PRESCRIPTION", "PILL_FRONT", "PILL_BACK")
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "uploads"