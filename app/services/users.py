from datetime import UTC, datetime, timedelta

from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from pydantic import EmailStr
from starlette import status
from tortoise.transactions import in_transaction

from app.core import config
from app.dtos.users import LoginRequest, SignUpRequest, UserUpdateRequest
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.utils.common import normalize_phone_number, redis_client
from app.utils.security import create_access_token, create_refresh_token, hash_password, verify_password


class UserManageService:
    """
    사용자 계정 관리(회원가입, 로그인, 정보 수정, 탈퇴)를 담당하는 서비스 클래스입니다.
    """
    def __init__(self):
        self.user_repo = UserRepository()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # 회원가입
    async def signup(self, data: SignUpRequest) -> User:
        """
        새로운 사용자를 등록합니다. 필수 약관 동의 및 중복 검사를 수행합니다.
        
        Args:
            data (SignUpRequest): 회원가입에 필요한 사용자 정보
            
        Returns:
            User: 생성된 사용자 DB 객체
        """
        if not data.is_terms_agreed or not data.is_privacy_agreed:
            raise HTTPException(status_code=400, detail="필수 약관에 동의해야 합니다.")

        # ID(Email) 중복 체크
        await self.check_id_exists(data.id)

        # 전화번호 정규화 및 중복 체크
        normalized_phone = normalize_phone_number(data.phone_number)
        await self.check_phone_number_exists(normalized_phone)

        await self.check_resident_registration_number_exists(data.resident_registration_number)

        # Pydantic → dict 변환
        user_data = data.model_dump()

        # 데이터 가공
        user_data["phone_number"] = normalized_phone
        user_data["password"] = hash_password(data.password)

        async with in_transaction():
            return await self.user_repo.create_user(user_data)

    async def login(self, data: LoginRequest, remember_me: bool = False) -> dict:
        """
        사용자 아이디와 비밀번호를 검증하고 액세스 및 리프레시 토큰을 생성합니다.
        
        Args:
            data (LoginRequest): 로그인 아이디(이메일) 및 비밀번호
            remember_me (bool): 토큰 만료 시간 연장 여부
            
        Returns:
            dict: 액세스 토큰, 리프레시 토큰 및 사용자 ID 정보
        """
        # ID(Email)로 사용자 조회
        user = await self.user_repo.get_by_id(data.id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 올바르지 않습니다.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 비밀번호 검증
        if not verify_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 올바르지 않습니다.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Generate tokens
        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        if remember_me:
            refresh_token_expires = timedelta(minutes=config.REFRESH_TOKEN_EXPIRE_MINUTES)
        else:
            refresh_token_expires = timedelta(minutes=config.REFRESH_TOKEN_EXPIRE_MINUTES_SHORT)

        access_token = create_access_token(
            data={"user_id": user.id}, expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(
            data={"user_id": user.id}, expires_delta=refresh_token_expires
        )

        # Redis에 세션 저장
        await redis_client.setex(
            f"session:{user.id}", 
            int(access_token_expires.total_seconds()), 
            access_token
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "id": user.id,
            "token_type": "bearer"
        }

    async def check_id_exists(self, id: str | EmailStr) -> None:
        return await self.user_repo.get_by_id(id)

    async def check_phone_number_exists(self, phone_number: str) -> None:
        if await self.user_repo.exists_by_phone_number(phone_number):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 사용중인 휴대폰 번호입니다.")

    async def check_resident_registration_number_exists(self, resident_registration_number: str) -> None:
        if await self.user_repo.exists_by_resident_registration_number(resident_registration_number):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 등록된 주민번호입니다.")

    async def update_user(self, user: User, data: UserUpdateRequest) -> User:
        update_data = data.model_dump(exclude_unset=True)

        if 'phone_number' in update_data and update_data['phone_number']:
            normalized_phone = normalize_phone_number(update_data['phone_number'])
            if normalized_phone != user.phone_number:
                await self.check_phone_number_exists(normalized_phone)
            update_data['phone_number'] = normalized_phone

        user.update_from_dict(update_data)
        await user.save()
        return user

    async def delete_user(self, id: str, password: str = "") -> None:
        user = await self.user_repo.get_by_id(id=id)
        if not user:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다.")

        # If password is provided, verify it (for me-delete, might need verification or just session check)
        if password and not verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="비밀번호가 일치하지 않습니다.")

        await redis_client.delete(f"session:{id}")
        await user.delete()

    async def logout(self, id: str) -> None:
        await redis_client.delete(f"session:{id}")

    async def social_login(self, data) -> dict:
        """
        소셜 로그인 처리 (간소화)
        """
        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"user_id": data.id}, expires_delta=access_token_expires)

        await redis_client.setex(f"session:{data.id}", int(access_token_expires.total_seconds()), access_token)

        return {
            "access_token": access_token,
            "id": data.id,
            "is_new_user": False # Logic to check if user existed can be added
        }
