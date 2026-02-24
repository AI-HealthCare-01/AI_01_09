
from app.models.users import User


class UserRepository:
    def __init__(self):
        self._model = User

    # 회원가입
    async def create_user(self, data: dict) -> User:
        # dict 언패킹(**)을 사용하여 간단하게 생성
        return await self._model.create(**data)

    # 이메일 찾기
    async def find_id_by_info(self, name: str, phone_number: str) -> User | None:
        return await self._model.get_or_none(name=name, phone_number=phone_number)

    # 비밀번호 찾기
    async def get_user_for_reset(self, id: str, name: str, phone_number: str) -> User | None:
        return await self._model.get_or_none(id=id, name=name, phone_number=phone_number)

    # 이메일 중복 확인
    async def get_by_id(self, id: str) -> User | None:
        return await self._model.get_or_none(id=id)

    # 전화번호 중복 확인
    async def exists_by_phone_number(self, phone_number: str) -> bool:
        return await self._model.filter(phone_number=phone_number).exists()

    # 주민번호 중복 확인
    async def exists_by_resident_registration_number(self, resident_registration_number: str) -> bool:
        return await self._model.filter(resident_registration_number=resident_registration_number).exists()
