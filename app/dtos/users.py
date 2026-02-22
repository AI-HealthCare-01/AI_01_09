from typing import Annotated

from pydantic import AfterValidator, BaseModel, EmailStr, Field

from app.dtos.base import BaseSerializerModel
from app.validators.user_validators import validate_id_card, validate_password, validate_phone_number


class SignUpRequest(BaseModel):
    email: Annotated[
        EmailStr,
        Field(max_length=40),
    ]
    password: Annotated[str, Field(min_length=8), AfterValidator(validate_password)]
    name: Annotated[str, Field(max_length=20)]
    nickname: Annotated[str, Field(max_length=20)]
    phone_number: Annotated[str, AfterValidator(validate_phone_number)]
    id_card: Annotated[str, AfterValidator(validate_id_card)]
    is_terms_agreed: bool = Field(..., description="이용약관 동의 여부")
    is_privacy_agreed: bool = Field(..., description="개인정보 처리방침 동의 여부")
    is_marketing_agreed: bool = Field(default=False, description="마케팅 동의 여부")
    chronic_disease: Annotated[str, Field(None, description="만성 질환")]

class LoginRequest(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(..., description="패스워드")]


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class LoginResponse(Token):
    email: str
    refresh_token: str | None = None # 쿠키로 내려줄 수도 있고 바디에 포함할 수도 있음

class TokenRefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserUpdateRequest(BaseModel):
    nickname: Annotated[str | None, Field(None, min_length=2, max_length=40)]
    phone_number:  Annotated[str, AfterValidator(validate_phone_number)]
    id_card: Annotated[str, AfterValidator(validate_id_card)]
    chronic_disease: str = None
    is_marketing_agreed: bool = Field(default=False)

class UserInfoResponse(BaseSerializerModel):
    name: str
    email: EmailStr
    phone_number: str
    nickname: str
    id_card: str
    is_terms_agreed: bool
    is_privacy_agreed: bool
    is_marketing_agreed: bool
    chronic_disease: str | None = None

    class Config:
        from_attributes = True # ORM 객체를 자동으로 DTO로 변환 가능케 함
