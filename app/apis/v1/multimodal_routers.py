from typing import Annotated
from fastapi import APIRouter, Depends, status
from app.dependencies.security import get_request_user
from app.models.user import User

multimodal_router = APIRouter(tags=["multimodal"])

@multimodal_router.post("/multimodal/generate", status_code=status.HTTP_201_CREATED)
async def generate_multimodal_asset(
    source_table: str,
    source_id: int,
    asset_type: str,
    user: Annotated[User, Depends(get_request_user)]
):
    """
    [MULTIMODAL] 카드뉴스/음성 생성.
    """
    return {"id": 900, "asset_url": "https://.../assets/900.mp3"}

@multimodal_router.get("/assets")
async def get_assets(
    user: Annotated[User, Depends(get_request_user)],
    source_table: str | None = None,
    source_id: int | None = None,
):
    """
    [MULTIMODAL] 생성된 자산 조회(source_table/source_id로 필터)
    """
    return {"items": []}

