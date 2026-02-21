from datetime import date, datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

from app.dtos.base import BaseSerializerModel
from app.validators.user_validators import validate_phone_number
from pydantic import AfterValidator, BaseModel, EmailStr, Field

class UserUpdateRequest(BaseModel):
    nickname: Annotated[str | None, Field(None, min_length=2, max_length=40)]
    phone_number:  Annotated[str, AfterValidator(validate_phone_number)]
    password: Annotated[str | None, Field(None, max_length=128)]
    is_marketing_agreed: bool = Field(default=False)
    chronic_disease: str = None # 추가

class UserInfoResponse(BaseSerializerModel):
    name: str
    email: EmailStr
    phone_number: str
    nickname: str
    id_card: str
    is_marketing_agreed: str
    chronic_disease:str = None

    class Config:
        from_attributes = True # ORM 객체를 자동으로 DTO로 변환 가능케 함