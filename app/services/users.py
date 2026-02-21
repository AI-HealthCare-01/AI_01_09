from tortoise.transactions import in_transaction

from app.dtos.users import UserUpdateRequest
from app.models.users import User
from app.repositories.user_repository import UserRepository
from app.services.auth import AuthService
from app.utils.common import normalize_phone_number
from typing import Optional, Union
from pydantic import EmailStr
from passlib.context import CryptContext

class UserManageService:
    def __init__(self):
        self.repo = UserRepository()
        self.auth_service = AuthService()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # 회원수정
    async def update_user(self, user: User, data: UserUpdateRequest) -> User:
        update_data = data.model_dump(exclude_unset=True)

        if 'phone_number' in update_data:
            normalized_phone = normalize_phone_number(update_data['phone_number'])
            if normalized_phone != user.phone_number:
                await self.auth_service.check_phone_number_exists(normalized_phone)
            update_data['phone_number'] = normalized_phone
            
        user.update_from_dict(update_data)
        await user.save()
        return user

    # 로그인
    async def login(self, email: str, password: str) -> Optional[User]:
        user = await self.repo.get_by_email(email=email)
        if user and self.pwd_context.verify(password, user.password):
            return user
        return None
    
    # 이메일 찾기
    async def find_email(self, name: str, phone_number: str) -> Optional[str]:
        user = await self.repo.find_email_by_info(name=name, phone_number=phone_number)
        return user.email if user else None
    
    # 패스워드 찾기
    async def reset_password(self, email: str, name: str, phone_number: str, new_password: str) -> bool:
        user = await self.repo.get_user_for_reset(email=email, name=name, phone_number=phone_number)
        if user:
            user.password = self.pwd_context.hash(new_password)
            await user.save()
            return True
        return False
    
    # 패스워드 수정
    async def change_password(self, email: str, old_password: str, new_password: str) -> bool:
        user = await self.repo.get_by_email(email=email)
        if user and self.pwd_context.verify(old_password, user.password):
            user.password = self.pwd_context.hash(new_password)
            await user.save()
            return True
        return False
    
    # 회원 탈퇴
    async def delete_user(self, email: str, password: str) -> bool:
        user = await self.repo.get_by_email(email=email)
        if user and self.pwd_context.verify(password, user.password):
            await user.delete()
            return True
        return False
    
    