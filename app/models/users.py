from tortoise import fields, models

class User(models.Model):
    email = fields.CharField(primary_key=True, max_length=100)
    nickname = fields.CharField(max_length=40)
    name = fields.CharField(max_length=20)
    password = fields.CharField(max_length=128)
    phone_number = fields.CharField(max_length=11)
    id_card = fields.CharField(max_length=14)

    is_terms_agreed = fields.BooleanField(default=False)    # 이용약관 (필수)
    is_privacy_agreed = fields.BooleanField(default=False)  # 개인정보 (필수)
    is_marketing_agreed = fields.BooleanField(default=False) # 마케팅 (선택)
    chronic_disease = fields.TextField(null=True, description="만성 질환 정보")

    class Meta:
        table = "users"
