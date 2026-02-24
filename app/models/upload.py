from tortoise import fields, models

class Upload(models.Model):
    """
    사용자가 업로드한 원본 파일 정보(처방전, 약품 사진 등)를 관리하는 모델입니다.
    저장소 내 파일 경로와 분류 카테고리를 저장하며 업로드한 사용자와 연결됩니다.
    """
    id = fields.IntField(pk=True)
    file_url = fields.CharField(max_length=512)    # S3 저장소 내 이미지 경로
    file_type = fields.CharField(max_length=20)    # png, jpg 등 확장자
    category = fields.CharField(max_length=50)     # 분류 (prescription, pill_front, pill_back)
    created_at = fields.DatetimeField(auto_now_add=True)
    user = fields.ForeignKeyField("models.User", related_name="uploads")

    class Meta:
        table = "uploads"
