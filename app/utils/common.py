import re
import random
import string
from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from app.core import config
import redis.asyncio as redis  # 비동기 redis 라이브러리

redis_client = redis.from_url("redis://172.17.0.1:6379", decode_responses=True)

conf = ConnectionConfig(
    MAIL_USERNAME=config.SMTP_USER,         # 네이버 이메일 주소 전체
    MAIL_PASSWORD=config.SMTP_PASSWORD,   # 16자리 앱 비밀번호
    MAIL_FROM=config.SMTP_USER,             # 반드시 네이버 메일 주소와 일치해야 함
    MAIL_PORT=config.SMTP_PORT,                             # 네이버 SMTP SSL 포트
    MAIL_SERVER=config.SMTP_HOST,              # 네이버 SMTP 서버 주소
    MAIL_STARTTLS=config.MAIL_STARTTLS,                       # 465 포트 사용 시 False
    MAIL_SSL_TLS=config.MAIL_SSL_TLS,                         # 465 포트 사용 시 True
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

def normalize_phone_number(phone_number: str) -> str:
    if phone_number.startswith("+82"):
        phone_number = "0" + phone_number[3:]
    phone_number = re.sub(r"\D", "", phone_number)

    return phone_number

class Email:

    # 1. 이메일 인증 번호 발송
    async def send_verification(self, email: str):
        # 6자리 랜덤 코드 생성
        code = "".join(random.choices(string.digits, k=6))
        
        # 기존 인증코드 삭제 후 새로 저장
        await redis_client.setex(f"auth:{email}", 300, code)

        # 이메일 발송
        message = MessageSchema(
            subject="인증 번호",
            recipients=[email],
            body=f"인증 번호는 [{code}] 입니다.",
            subtype=MessageType.plain
        )

        fm = FastMail(conf)

        await fm.send_message(message)

        return True

    async def verify_code(self, email: str, code: str) -> bool:
        """사용자가 입력한 코드가 Redis에 있는 코드와 일치하는지 확인"""
        saved_code = await redis_client.get(f"auth:{email}")
        return saved_code == code