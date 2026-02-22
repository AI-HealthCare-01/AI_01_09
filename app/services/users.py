from datetime import UTC, datetime, timedelta

from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from pydantic import EmailStr
from starlette import status
from tortoise.transactions import in_transaction

from app.core import config
from app.dtos.users import LoginRequest, SignUpRequest, UserUpdateRequest
from app.models.users import User
from app.repositories.user_repository import UserRepository
from app.utils.common import normalize_phone_number, redis_client
from app.utils.security import create_access_token, create_refresh_token, hash_password, verify_password


class UserManageService:
    def __init__(self):
        self.repo = UserRepository()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.user_repo = UserRepository()

    # 회원가입
    async def signup(self, data: SignUpRequest) -> User:

        if not data.is_terms_agreed or not data.is_privacy_agreed:
            raise HTTPException(status_code=400, detail="필수 약관에 동의해야 합니다.")

        # 이메일 중복 체크
        await self.check_email_exists(data.email)

        # 전화번호 정규화 및 중복 체크
        normalized_phone = normalize_phone_number(data.phone_number)
        await self.check_phone_number_exists(normalized_phone)

        await self.check_id_card_exists(data.id_card)

        # Pydantic → dict 변환
        user_data = data.model_dump()

        # 데이터 가공
        user_data["phone_number"] = normalized_phone
        user_data["password"] = hash_password(data.password)

        async with in_transaction():
            return await self.user_repo.create_user(user_data)

    async def login(self, data: LoginRequest, remember_me: bool = False) -> dict:
        # 이메일로 사용자 조회
        user = await self.user_repo.get_by_email(data.email)
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
            data={"user_id": user.email}, expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(
            data={"user_id": user.email}, expires_delta=refresh_token_expires
        )

        # Redis에 세션 저장 (액세스 토큰 만료 시간과 동일하게 설정)
        # 키 형식: session:email, 값: access_token
        await redis_client.setex(
            f"session:{user.email}", 
            int(access_token_expires.total_seconds()), 
            access_token
        )

        # Calculate expiration time to set the correct cookie header
        access_expires_at = int((datetime.now(UTC) + access_token_expires).timestamp())
        refresh_expires_at = int((datetime.now(UTC) + refresh_token_expires).timestamp())

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "email": user.email,
            "token_type": "bearer",
            "access_expires_at": access_expires_at,
            "refresh_expires_at": refresh_expires_at
        }

    async def update_session(self, email: str, access_token: str, expires_in_seconds: int) -> None:
        """
        액세스 토큰 갱신 시 Redis의 세션 정보를 새 토큰으로 업데이트합니다.
        """
        await redis_client.setex(
            f"session:{email}",
            expires_in_seconds,
            access_token
        )

    # 이메일 중복 여부 확인
    async def check_email_exists(self, email: str | EmailStr) -> None:
        if await self.user_repo.get_by_email(email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 사용중인 이메일입니다.")

    # 휴대폰 번호 중복 여부 확인
    async def check_phone_number_exists(self, phone_number: str) -> None:
        if await self.user_repo.exists_by_phone_number(phone_number):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 사용중인 휴대폰 번호입니다.")

    # 주민번호 중복 여부 확인
    async def check_id_card_exists(self, id_card: str) -> None:
        if await self.user_repo.exists_by_id_card(id_card):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 등록된 주민번호입니다.")

    # 회원 정보 조회
    async def get_user(self, email: str) -> User:
        user = await self.user_repo.get_by_email(email=email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다.")
        return user

    # 회원 정보 수정
    async def update_user(self, user: User, data: UserUpdateRequest) -> User:
        update_data = data.model_dump(exclude_unset=True)

        if 'phone_number' in update_data:
            normalized_phone = normalize_phone_number(update_data['phone_number'])
            if normalized_phone != user.phone_number:
                await self.check_phone_number_exists(normalized_phone)
            update_data['phone_number'] = normalized_phone

        user.update_from_dict(update_data)
        await user.save()
        return user

    # 아이디 찾기 (이메일 찾기)
    async def find_email(self, name: str, phone_number: str) -> str:
        normalized_phone = normalize_phone_number(phone_number)
        user = await self.user_repo.find_email_by_info(name=name, phone_number=normalized_phone)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="일치하는 회원 정보가 없습니다.")
        return user.email

    # -------------------------------------------------------------------------
    # 패스워드 재설정을 위한 회원 확인 (비밀번호 찾기 전 단계)
    async def verify_user_for_reset(self, email: str, name: str, phone_number: str) -> User:
        normalized_phone = normalize_phone_number(phone_number)
        user = await self.user_repo.get_user_for_reset(email=email, name=name, phone_number=normalized_phone)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="입력하신 정보가 일치하지 않습니다.")
        return user

    # 패스워드 변경 (마이페이지/비밀번호 변경 기능)
    async def change_password(self, email: str, old_password: str, new_password: str) -> None:
        user = await self.user_repo.get_by_email(email=email)
        if not user or not verify_password(old_password, user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="기존 비밀번호가 일치하지 않습니다.")

        user.password = hash_password(new_password)
        await user.save()

    # 패스워드 재설정 (비밀번호 찾기 결과 단계)
    async def reset_password(self, email: str, new_password: str) -> None:
        user = await self.user_repo.get_by_email(email=email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다.")
        
        user.password = hash_password(new_password)
        await user.save()

    # 회원 탈퇴
    async def delete_user(self, email: str, password: str) -> None:
        user = await self.repo.get_by_email(email=email)
        if not user or not self.pwd_context.verify(password, user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="비밀번호가 일치하지 않습니다.")

        # Redis 세션 삭제
        await redis_client.delete(f"session:{email}")
        await user.delete()

    # 로그아웃
    async def logout(self, email: str) -> None:
        await redis_client.delete(f"session:{email}")

