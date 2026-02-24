from pydantic import BaseModel, EmailStr


class EmailRequest(BaseModel):
    id: EmailStr

class EmailCodeRequest(BaseModel):
    id: EmailStr
    code: str
