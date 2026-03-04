from typing import cast

from app.models.current_med import CurrentMed


class CurrentMedRepository:
    """
    User 모델에 대한 데이터베이스 접근 및 CRUD 연산을 담당하는 레포지토리 클래스입니다.
    """

    def __init__(self):
        self._model = CurrentMed

    # 사용자에 해당하는 현재 복용 약물 목록 가져오기
    async def get_by_user_id(self, user_id: str) -> list[CurrentMed]:
        """
        사용자 아이디를 이용해 현재 복용 약물을 조회합니다.

        Args:
            user_id (str): 조회할 사용자 아이디

        Returns:
            list[CurrentMed]: 현재 복용 약물 리스트
        """
        return cast(list[CurrentMed], await self._model.filter(user_id=user_id).all())

    async def delete_by_user_id(self, user_id: str):
        """
        사용자 아이디에 해당하는 모든 복용 약물 정보를 삭제합니다.
        """
        await self._model.filter(user_id=user_id).delete()

    async def create_many(self, user_id: str, medications: list[dict]):
        """
        여러 개의 복용 약물 정보를 한꺼번에 생성합니다.
        """
        objs = [self._model(user_id=user_id, **data) for data in medications]
        await self._model.bulk_create(objs)
