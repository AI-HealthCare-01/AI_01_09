import random
import re
import string

import redis.asyncio as redis  # 비동기 redis 라이브러리
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.core import config

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
    """
    다양한 형식의 휴대폰 번호를 숫자만 포함된 표준 형식으로 정규화합니다.
    국가번호(+82)를 0으로 변환하고 기호를 제거합니다.
    
    Args:
        phone_number (str): 정규화되지 않은 휴대폰 번호 입력값
        
    Returns:
        str: 숫자만 남은 정규화된 휴대폰 번호
    """
    if phone_number.startswith("+82"):
        phone_number = "0" + phone_number[3:]
    phone_number = re.sub(r"\D", "", phone_number)

    return phone_number

class Email:
    """
    SMTP 프로토콜을 사용하여 이메일 인증 코드를 발송하고 검증하는 클래스입니다.
    """

    # 1. 이메일 인증 번호 발송
    async def send_verification(self, email: str):
        """
        6자리 랜덤 숫자를 생성하여 지정된 이메일 주소로 발송하고 Redis에 저장합니다.
        유효 기간은 5분(300초)입니다.
        
        Args:
            email (str): 인증 번호를 받을 이메일 주소
            
        Returns:
            bool: 발송 성공 여부
        """
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
        """
        사용자가 입력한 코드가 Redis에 저장된 코드와 일치하는지 확인합니다.
        
        Args:
            email (str): 인증을 진행 중인 이메일 주소
            code (str): 사용자가 입력한 6자리 코드
            
        Returns:
            bool: 인증 일치 여부
        """
        saved_code = await redis_client.get(f"auth:{email}")
        return saved_code == code
