import re

from fastapi.exceptions import HTTPException
from starlette import status


def validate_password(password: str) -> str:
    if len(password) < 8:
        text = "비밀번호는 8자 이상이어야 합니다."
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=text)

    # 대문자를 포함하고 있는지
    if not re.search(r"[A-Z]", password):
        text = "비밀번호에는 대문자, 소문자, 특수문자, 숫자가 각 하나씩 포함되어야 합니다."
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=text)

    # 소문자를 포함하고 있는지
    if not re.search(r"[a-z]", password):
        text = "비밀번호에는 대문자, 소문자, 특수문자, 숫자가 각 하나씩 포함되어야 합니다."
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=text)

    # 숫자를 포함하고 있는지
    if not re.search(r"[0-9]", password):
        text = "비밀번호에는 대문자, 소문자, 특수문자, 숫자가 각 하나씩 포함되어야 합니다."
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=text)

    # 특수문자를 포함하고 있는지
    if not re.search(r"[^a-zA-Z0-9]", password):
        text = "비밀번호에는 대문자, 소문자, 특수문자, 숫자가 각 하나씩 포함되어야 합니다."
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=text)

    return password


def validate_phone_number(phone_number: str) -> str:
    patterns = [
        r"010-\d{4}-\d{4}",  # 010-1234-5678
        r"010\d{8}",  # 01012345678
        r"\+8210\d{8}",  # +821012345678
    ]

    if not any(re.fullmatch(p, phone_number) for p in patterns):
        text = "유효하지 않은 휴대폰 번호 형식입니다."
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=text)

    return phone_number

def validate_id_card(value: str) -> str:
    if len(value) != 14:
        text = "주민번호는 14자리여야 합니다."
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=text)

    if "-" not in value:
        text = "주민번호 형식이 올바르지 않습니다. (xxxxxx-xxxxxxx)"
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=text)

    return value
