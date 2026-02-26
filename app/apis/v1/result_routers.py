from typing import Annotated
from fastapi import APIRouter, Depends, status
from app.dependencies.security import get_request_user
from app.models.user import User

result_router = APIRouter(tags=["results"])

@result_router.get("/prescriptions")
async def get_prescriptions(
    user: Annotated[User, Depends(get_request_user)]
):
    """
    [RESULT] 처방전 결과 목록 조회
    """
    return {"items": []}

@result_router.get("/prescriptions/{id}")
async def get_prescription_detail(
    id: int,
    user: Annotated[User, Depends(get_request_user)]
):
    """
    [RESULT] 처방전 상세 조회(약 목록 포함)
    """
    return {"id": id, "drugs": []}

@result_router.get("/pill-recognitions")
async def get_pill_recognitions(
    user: Annotated[User, Depends(get_request_user)]
):
    """
    [RESULT] 알약 인식 결과 목록 조회
    """
    return {"items": []}

@result_router.get("/pill-recognitions/{id}")
async def get_pill_recognition_detail(
    id: int,
    user: Annotated[User, Depends(get_request_user)]
):
    """
    [RESULT] 알약 인식 결과 상세 조회
    """
    return {"id": id, "pill_name": "아스피린"}