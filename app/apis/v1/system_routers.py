from typing import List, Annotated
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from app.models.system_log import SystemLog

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
    전체 시스템 응답 속도 및 API 호출 로그를 모니터링합니다. (NFR-PERF-001 대응)
    
    Returns:
        list: 최근 100개의 시스템 로그 목록
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
    응답 시간이 5초(5000ms)를 초과한 느린 API 호출 로그를 필터링하여 조회합니다.
    
    Returns:
        list: 느린 응답 로그 목록
    """
    logs = await SystemLog.filter(response_ms__gte=5000).order_by("-created_at")
    return [LogResponse(
        id=log.id,
        api_path=log.api_path,
        method=log.method,
        response_ms=log.response_ms,
        created_at=log.created_at.isoformat()
    ) for log in logs]

@system_router.get("/logs/errors", response_model=List[LogResponse], status_code=status.HTTP_200_OK)
async def get_error_logs():
    """
    시스템에서 발생한 에러(ERROR 메서드 기록) 로그를 조회합니다. (NFR-MON-001 대응)
    
    Returns:
        list: 최근 50개의 에러 로그 목록
    """
    logs = await SystemLog.filter(method="ERROR").order_by("-created_at").limit(50)
    return [LogResponse(
        id=log.id,
        api_path=log.api_path,
        method=log.method,
        response_ms=log.response_ms,
        created_at=log.created_at.isoformat()
    ) for log in logs]

@system_router.get("/logs/user", status_code=status.HTTP_200_OK)
async def get_user_behavior_logs():
    """
    사용자의 주요 행동(로그인, 검색, 가이드 생성 등)에 대한 통계성 로그를 조회합니다.
    
    Returns:
        dict: 사용자 행위 분석 정보 (현재 수집 준비 중)
    """
    return {"detail": "사용자 행동 로그 수집 중입니다. (접속, 검색, 가이드 생성 등)"}
