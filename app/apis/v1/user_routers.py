from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import ORJSONResponse as Response

from app.dependencies.security import get_request_user
from app.dtos.users import UserInfoResponse, UserUpdateRequest
from app.models.users import User
from app.services.users import UserManageService
from app.services.auth import AuthService
from app.dtos.auth import LoginRequest, LoginResponse, SignUpRequest, TokenRefreshResponse, EmailRequest

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.get("/eamil-check")
async def eamil_check(
    email: str,
    auth_service: Annotated[AuthService, Depends(AuthService)]
):
    await auth_service.check_email_exists(email)
    return {"detail": "사용 가능한 이메일입니다."}

@user_router.get("/me")
async def get_my_info(
    email: str,
    auth_service: Annotated[AuthService, Depends(AuthService)]
) -> Response:
    return await auth_service.get_user(email)

@user_router.get("/me")
async def get_my_info(
    email: str,
    auth_service: Annotated[AuthService, Depends(AuthService)]
) -> Response:
    return await auth_service.get_user(email)

@user_router.patch("/me", status_code=status.HTTP_200_OK)
async def update_user_me_info(
    update_data: UserUpdateRequest,
    user: Annotated[User, Depends(get_request_user)],
    user_manage_service: Annotated[UserManageService, Depends(UserManageService)],
) -> Response:
    updated_user = await user_manage_service.update_user(user=user, data=update_data)
    return Response(UserInfoResponse.model_validate(updated_user).model_dump(), status_code=status.HTTP_200_OK)

@user_router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def withdraw_user(
    password_data: dict, # {"password": "..."} 형태
    user: Annotated[User, Depends(get_request_user)],
    user_manage_service: Annotated[UserManageService, Depends(UserManageService)],
) -> Response:
    success = await user_manage_service.delete_user(email=user.email, password=password_data.get("password"))
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="비밀번호가 일치하지 않습니다.")
    
    return Response(None, status_code=status.HTTP_204_NO_CONTENT)