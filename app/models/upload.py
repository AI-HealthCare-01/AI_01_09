from enum import Enum
from tortoise import fields, models

class UploadCategory(str, Enum):
    PRESCRIPTION = "PRESCRIPTION"
    PILL_FRONT = "PILL_FRONT"
    PILL_BACK = "PILL_BACK"

class Upload(models.Model):
    id = fields.IntField(pk=True)
    file_url = fields.CharField(max_length=512)    # S3 저장소 내 이미지 경로
    file_type = fields.CharField(max_length=20)    # png, jpg 등 확장자
    category = fields.CharEnumField(UploadCategory, description='용도 구분 ("PRESCRIPTION", "PILL_FRONT", "PILL_BACK")')     # 분류 (prescription, pill_front, pill_back)
    created_at = fields.DatetimeField(auto_now_add=True)
    user = fields.ForeignKeyField("models.User", related_name="uploads")

    class Meta:
        table = "uploads"