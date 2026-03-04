from pydantic import BaseModel, EmailStr


class EmailRequest(BaseModel):
    email: EmailStr


class EmailCodeRequest(BaseModel):
    email: EmailStr
    code: str
