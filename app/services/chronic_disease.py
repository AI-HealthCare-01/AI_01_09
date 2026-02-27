from app.models.chronic_disease import ChronicDisease
from app.repositories.chronic_disease import ChronicDiseaseRepository


class ChronicDiseaseManageService:
    """
    User 모델에 대한 데이터베이스 접근 및 CRUD 연산을 담당하는 레포지토리 클래스입니다.
    """

    def __init__(self):
        self.chronic_disease_repo = ChronicDiseaseRepository()

    # 사용자에 해당하는 질병 가져오기
    async def get_by_user_id(self, user_id: str) -> ChronicDisease | None:
        """
        사용자 아이디를 이용해 질병을 조회합니다.

        Args:
            user_id (str): 조회할 사용자 아이디

        Returns:
            ChronicDisease | None: 사용자 객체 또는 없음
        """
        chronic_disease: ChronicDisease | None = await self.chronic_disease_repo.get_by_user_id(user_id=user_id)  # type: ignore[assignment]
        return chronic_disease
