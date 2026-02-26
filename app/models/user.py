from tortoise import fields, models


class User(models.Model):
    """
    서비스의 사용자 계정 정보를 관리하는 모델입니다.
    성명, 연락처, 암호화된 비밀번호 및 필수 약관 동의 상태를 포함합니다.
    """

    # 사용자 ID (이메일 주소): 모든 데이터 연결의 중심
    id = fields.CharField(max_length=100, pk=True, description="사용자 ID (이메일 주소)")
    nickname = fields.CharField(max_length=40)  # 앱에서 활동할 닉네임
    name = fields.CharField(max_length=20)  # 사용자 본명
    password = fields.CharField(max_length=128)  # 보안용 암호화 비밀번호
    phone_number = fields.CharField(max_length=11)  # 연락처
    resident_registration_number = fields.CharField(max_length=14)  # 연령 및 성별 분석용 주민번호
    is_terms_agreed = fields.BooleanField(default=False)  # 약관 동의 여부
    is_privacy_agreed = fields.BooleanField(default=False)  # 개인정보 동의 여부
    is_marketing_agreed = fields.BooleanField(default=False)  # 마케팅 수신 동의

    class Meta:
        table = "users"
