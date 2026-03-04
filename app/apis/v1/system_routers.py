from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies.security import get_request_user

system_router = APIRouter(prefix="/system", tags=["system"])


@system_router.get("/logs")
async def get_system_logs(
    user: Annotated[dict, Depends(get_request_user)],  # Should be admin check in real case
    page: int = 1,
    size: int = 50,
):
    """
    [SYSTEM] 시스템 로그 조회(운영/디버깅).
    """
    return {"items": []}
