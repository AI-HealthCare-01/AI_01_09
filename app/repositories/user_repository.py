from pydantic import EmailStr
from app.models.users import User
from typing import Optional


class UserRepository:
    def __init__(self):
        self._model = User
    
    async def create_user(self, data: dict) -> User:
        # dict 언패킹(**)을 사용하여 간단하게 생성
        return await self._model.create(**data)

    async def find_email_by_info(self, name: str, phone_number: str) -> Optional[User]:
        return await self._model.get_or_none(name=name, phone_number=phone_number)

    async def get_user_for_reset(self, email: str, name: str, phone_number: str) -> Optional[User]:
        return await self._model.get_or_none(email=email, name=name, phone_number=phone_number)

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self._model.get_or_none(email=email)
    
    async def exists_by_phone_number(self, phone_number: str) -> bool:
        return await self._model.filter(phone_number=phone_number).exists()
    
    async def exists_by_id_card(self, id_card: str) -> bool:
        return await self._model.filter(id_card=id_card).exists()
    