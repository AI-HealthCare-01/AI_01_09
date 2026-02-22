from tortoise import fields, models


class User(models.Model):
    email = fields.CharField(primary_key=True, max_length=100, description="이메일 (필수)")
    nickname = fields.CharField(max_length=40, description="닉네임 (필수)")
    name = fields.CharField(max_length=20, description="이름 (필수)")
    password = fields.CharField(max_length=128, description="패스워드 (필수)")
    phone_number = fields.CharField(max_length=11, description="휴대폰 번호 (필수)")
    id_card = fields.CharField(max_length=14, description="주민번호 (필수)")

    is_terms_agreed = fields.BooleanField(default=False, description="이용약관 (필수)")
    is_privacy_agreed = fields.BooleanField(default=False, description="개인정보 (필수)")
    is_marketing_agreed = fields.BooleanField(default=False, description="마케팅 (선택)")
    chronic_disease = fields.TextField(null=True, description="만성 질환 정보")

    class Meta:
        table = "users"
