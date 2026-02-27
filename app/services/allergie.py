from app.models.allergy import Allergy
from app.repositories.allergie import AllergyRepository


class AllergyManageService:
    """
    User 모델에 대한 데이터베이스 접근 및 CRUD 연산을 담당하는 레포지토리 클래스입니다.
    """

    def __init__(self):
        self.allergy_repo = AllergyRepository()

    # 사용자에 해당하는 질병 가져오기
    async def get_by_user_id(self, user_id: str) -> Allergy | None:
        """
        사용자 아이디를 이용해 알러지를 조회합니다.

        Args:
            user_id (str): 조회할 사용자 아이디

        Returns:
            Allergy | None: 사용자 객체 또는 없음
        """
        allergy: Allergy | None = await self.allergy_repo.get_by_user_id(user_id=user_id)  # type: ignore[assignment]
        return allergy
