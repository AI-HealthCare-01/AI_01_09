from typing import Annotated

from pydantic import AfterValidator, BaseModel, EmailStr, Field

from app.validators.user_validators import validate_password, validate_phone_number, validate_id_card


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


class LoginResponse(BaseModel):
    access_token: str


class TokenRefreshResponse(LoginResponse): ...

class EmailRequest(BaseModel):
    email: EmailStr

class EmailCodeRequest(BaseModel):
    email: EmailStr
    code: str