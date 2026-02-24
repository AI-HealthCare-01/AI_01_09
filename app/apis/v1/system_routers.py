from typing import List, Annotated
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from app.models.systemLog import SystemLog

system_router = APIRouter(prefix="/system", tags=["system"])

class LogResponse(BaseModel):
    id: int
    api_path: str
    method: str
    response_ms: int
    created_at: str

    class Config:
        from_attributes = True

@system_router.get("/logs", response_model=List[LogResponse], status_code=status.HTTP_200_OK)
async def get_system_logs():
    """
    시스템 응답 속도 및 로그를 모니터링합니다. (NFR-PERF-001)
    """
    logs = await SystemLog.all().order_by("-created_at").limit(100)
    return [LogResponse(
        id=log.id,
        api_path=log.api_path,
        method=log.method,
        response_ms=log.response_ms,
        created_at=log.created_at.isoformat()
    ) for log in logs]

@system_router.get("/logs/slow", response_model=List[LogResponse], status_code=status.HTTP_200_OK)
async def get_slow_logs():
    """
    5초(5000ms) 이상 소요된 느린 응답 로그를 모니터링합니다.
    """
    logs = await SystemLog.filter(response_ms__gte=5000).order_by("-created_at")
    return [LogResponse(
        id=log.id,
        api_path=log.api_path,
        method=log.method,
        response_ms=log.response_ms,
        created_at=log.created_at.isoformat()
    ) for log in logs]
