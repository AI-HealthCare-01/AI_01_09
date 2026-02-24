from datetime import UTC, datetime, timedelta

from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from pydantic import EmailStr
from starlette import status
from tortoise.transactions import in_transaction

from app.core import config
from app.dtos.users import LoginRequest, SignUpRequest, UserUpdateRequest, SocialLoginRequest
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.utils.common import normalize_phone_number, redis_client
from app.utils.security import create_access_token, create_refresh_token, hash_password, verify_password


class UserManageService:
    """
    사용자 계정 관리(회원가입, 로그인, 정보 수정, 탈퇴)를 담당하는 서비스 클래스입니다.
    """
    def __init__(self):
        self.repo = UserRepository()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.user_repo = UserRepository()

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

        # ID 중복 체크
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
        # ID로 사용자 조회
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

        # Redis에 세션 저장 (액세스 토큰 만료 시간과 동일하게 설정)
        await redis_client.setex(
            f"session:{user.id}", 
            int(access_token_expires.total_seconds()), 
            access_token
        )

        # Calculate expiration time
        access_expires_at = int((datetime.now(UTC) + access_token_expires).timestamp())
        refresh_expires_at = int((datetime.now(UTC) + refresh_token_expires).timestamp())

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "id": user.id,
            "token_type": "bearer",
            "access_expires_at": access_expires_at,
            "refresh_expires_at": refresh_expires_at
        }

    async def update_session(self, id: str, access_token: str, expires_in_seconds: int) -> None:
        """
        액세스 토큰 갱신 시 Redis의 세션 정보를 업데이트합니다.
        
        Args:
            id (str): 사용자 아이디
            access_token (str): 새로 발급된 액세스 토큰
            expires_in_seconds (int): 토큰 만료 시간(초)
        """
        await redis_client.setex(
            f"session:{id}",
            expires_in_seconds,
            access_token
        )

    async def check_id_exists(self, id: str | EmailStr) -> None:
        """
        아이디(이메일)가 이미 존재하는지 확인합니다.
        
        Args:
            id (str): 확인할 아이디
        """
        if await self.user_repo.get_by_id(id):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 사용중인 아이디입니다.")

    async def check_phone_number_exists(self, phone_number: str) -> None:
        """
        휴대폰 번호가 이미 등록되어 있는지 확인합니다.
        
        Args:
            phone_number (str): 확인할 휴대폰 번호
        """
        if await self.user_repo.exists_by_phone_number(phone_number):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 사용중인 휴대폰 번호입니다.")

    async def check_resident_registration_number_exists(self, resident_registration_number: str) -> None:
        """
        주민등록번호가 이미 등록되어 있는지 확인합니다.
        
        Args:
            resident_registration_number (str): 확인할 주민등록번호
        """
        if await self.user_repo.exists_by_resident_registration_number(resident_registration_number):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 등록된 주민번호입니다.")

    async def get_user(self, id: str) -> User:
        """
        아이디로 사용자 정볼를 조회합니다.
        
        Args:
            id (str): 조회할 사용자 아이디
            
        Returns:
            User: 사용자 객체
        """
        user = await self.user_repo.get_by_id(id=id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다.")
        return user

    async def update_user(self, user: User, data: UserUpdateRequest) -> User:
        """
        사용자의 정보를 업데이트합니다.
        
        Args:
            user (User): 현재 사용자 객체
            data (UserUpdateRequest): 수정할 데이터
            
        Returns:
            User: 수정된 사용자 객체
        """
        update_data = data.model_dump(exclude_unset=True)

        if 'phone_number' in update_data:
            normalized_phone = normalize_phone_number(update_data['phone_number'])
            if normalized_phone != user.phone_number:
                await self.check_phone_number_exists(normalized_phone)
            update_data['phone_number'] = normalized_phone

        user.update_from_dict(update_data)
        await user.save()
        return user

    async def find_id(self, name: str, phone_number: str) -> str:
        """
        이름과 연락처로 가입된 아이디를 찾습니다.
        
        Args:
            name (str): 이름
            phone_number (str): 휴대폰 번호
            
        Returns:
            str: 찾은 아이디
        """
        normalized_phone = normalize_phone_number(phone_number)
        user = await self.user_repo.find_id_by_info(name=name, phone_number=normalized_phone)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="일치하는 회원 정보가 없습니다.")
        return user.id

    async def verify_user_for_reset(self, id: str, name: str, phone_number: str) -> User:
        """
        비밀번호 재설정을 위해 입력된 사용자 정보를 검증합니다.
        
        Args:
            id (str): 아이디
            name (str): 이름
            phone_number (str): 휴대폰 번호
            
        Returns:
            User: 검증된 사용자 객체
        """
        normalized_phone = normalize_phone_number(phone_number)
        user = await self.user_repo.get_user_for_reset(id=id, name=name, phone_number=normalized_phone)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="입력하신 정보가 일치하지 않습니다.")
        return user

    async def change_password(self, id: str, old_password: str, new_password: str) -> None:
        """
        로그인된 사용자의 비밀번호를 변경합니다.
        
        Args:
            id (str): 사용자 아이디
            old_password (str): 기존 비밀번호
            new_password (str): 새로운 비밀번호
        """
        user = await self.user_repo.get_by_id(id=id)
        if not user or not verify_password(old_password, user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="기존 비밀번호가 일치하지 않습니다.")

        user.password = hash_password(new_password)
        await user.save()

    async def reset_password(self, id: str, new_password: str) -> None:
        """
        아이디를 기준으로 비밀번호를 강제 재설정합니다 (비밀번호 찾기용).
        
        Args:
            id (str): 사용자 아이디
            new_password (str): 새로운 비밀번호
        """
        user = await self.user_repo.get_by_id(id=id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다.")
        
        user.password = hash_password(new_password)
        await user.save()

    async def delete_user(self, id: str, password: str) -> None:
        """
        사용자 본인 확인 후 계정을 삭제(탈퇴)합니다.
        
        Args:
            id (str): 사용자 아이디
            password (str): 본인 확인용 비밀번호
        """
        user = await self.repo.get_by_id(id=id)
        if not user or not self.pwd_context.verify(password, user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="비밀번호가 일치하지 않습니다.")

        # Redis 세션 삭제
        await redis_client.delete(f"session:{id}")
        await user.delete()

    async def logout(self, id: str) -> None:
        """
        Redis 세션을 삭제하여 로그아웃 처리합니다.
        
        Args:
            id (str): 사용자 아이디
        """
        await redis_client.delete(f"session:{id}")

    async def social_login(self, data: SocialLoginRequest) -> dict:
        """
        소셜 로그인 정보를 바탕으로 인증을 수행하고 토큰을 발급합니다.
        
        Args:
            data (SocialLoginRequest): 소셜 제공자로부터 받은 사용자 정보
            
        Returns:
            dict: 액세스 및 리프레시 토큰 정보
        """
        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(minutes=config.REFRESH_TOKEN_EXPIRE_MINUTES)

        access_token = create_access_token(
            data={"user_id": data.id}, expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(
            data={"user_id": data.id}, expires_delta=refresh_token_expires
        )

        await redis_client.setex(
            f"session:{data.id}", 
            int(access_token_expires.total_seconds()), 
            access_token
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "id": data.id,
            "token_type": "bearer",
            "access_expires_at": int((datetime.now(UTC) + access_token_expires).timestamp()),
            "refresh_expires_at": int((datetime.now(UTC) + refresh_token_expires).timestamp())
        }
