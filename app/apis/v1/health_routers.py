from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from app.dependencies.security import get_request_user
from app.models.user import User
from app.models.chronic_disease import ChronicDisease
from app.models.allergy import Allergy
from app.dtos.health import (
    ChronicDiseaseListResponse, ChronicDiseaseCreateRequest, ChronicDiseaseResponse,
    AllergyListResponse, AllergyCreateRequest, AllergyResponse
)

health_router = APIRouter(prefix="/health", tags=["health-profile"])

# --- Chronic Diseases ---

@health_router.get("/chronic-diseases", response_model=ChronicDiseaseListResponse)
async def get_chronic_diseases(
    user: Annotated[User, Depends(get_request_user)]
):
    """
    [PROFILE] 기저질환 목록 조회
    """
    diseases = await ChronicDisease.filter(user=user).all()
    return {"items": diseases}

@health_router.post("/chronic-diseases", response_model=ChronicDiseaseResponse, status_code=status.HTTP_201_CREATED)
async def create_chronic_disease(
    request: ChronicDiseaseCreateRequest,
    user: Annotated[User, Depends(get_request_user)]
):
    """
    [PROFILE] 기저질환 등록
    """
    disease = await ChronicDisease.create(user=user, disease_name=request.disease_name)
    return disease

@health_router.delete("/chronic-diseases/{id}")
async def delete_chronic_disease(
    id: int,
    user: Annotated[User, Depends(get_request_user)]
):
    """
    [PROFILE] 기저질환 삭제
    """
    disease = await ChronicDisease.get_or_none(id=id, user=user)
    if not disease:
        raise HTTPException(status_code=404, detail="질환 정보를 찾을 수 없습니다.")
    await disease.delete()
    return {"detail": "삭제되었습니다."}

# --- Allergies ---

@health_router.get("/allergies", response_model=AllergyListResponse)
async def get_allergies(
    user: Annotated[User, Depends(get_request_user)]
):
    """
    [PROFILE] 알러지 목록 조회
    """
    allergies = await Allergy.filter(user=user).all()
    return {"items": allergies}

@health_router.post("/allergies", response_model=AllergyResponse, status_code=status.HTTP_201_CREATED)
async def create_allergy(
    request: AllergyCreateRequest,
    user: Annotated[User, Depends(get_request_user)]
):
    """
    [PROFILE] 알러지 등록
    """
    allergy = await Allergy.create(user=user, allergy_name=request.allergy_name)
    return allergy

@health_router.delete("/allergies/{id}")
async def delete_allergy(
    id: int,
    user: Annotated[User, Depends(get_request_user)]
):
    """
    [PROFILE] 알러지 삭제
    """
    allergy = await Allergy.get_or_none(id=id, user=user)
    if not allergy:
        raise HTTPException(status_code=404, detail="알러지 정보를 찾을 수 없습니다.")
    await allergy.delete()
    return {"detail": "삭제되었습니다."}
