from datetime import timedelta
from typing import Annotated

import jwt
from fastapi import APIRouter, Cookie, Depends, HTTPException, status, Form
from fastapi.responses import ORJSONResponse as Response
from fastapi.security import OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

from app.core import config
from app.core.config import Env
from app.dependencies.security import get_request_user
from app.dtos.users import (
    LoginRequest,
    LoginResponse,
    SignUpRequest,
    TokenRefreshResponse,
    UserInfoResponse,
    UserUpdateRequest,
)
from app.models.users import User
from app.services.users import UserManageService
from app.utils.security import create_access_token
from app.utils.common import Email

user_router = APIRouter(prefix="/users", tags=["users"])

# 회원가입
@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    request: SignUpRequest,
    auth_service: Annotated[UserManageService, Depends(UserManageService)],
) -> Response:
    await auth_service.signup(request)
    return Response(content={"detail": "회원가입이 성공적으로 완료되었습니다."}, status_code=status.HTTP_201_CREATED)

# 로그인
@user_router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[UserManageService, Depends(UserManageService)],
    remember_me: Annotated[bool, Form()] = False,
) -> Response:
    # OAuth2PasswordRequestForm expects 'username' (we use it as ID/email) and 'password'
    login_data = LoginRequest(id=form_data.username, password=form_data.password)
    tokens = await auth_service.login(login_data, remember_me=remember_me)

    resp = Response(
        content=LoginResponse(
            access_token=tokens["access_token"],
            token_type=tokens["token_type"],
            id=tokens["id"]
        ).model_dump(),
        status_code=status.HTTP_200_OK
    )

    # Set Refresh Token in HttpOnly cookie
    resp.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=True if config.ENV == Env.PROD else False,
        samesite="lax",
        domain=config.COOKIE_DOMAIN or None,
        expires=tokens["refresh_expires_at"],
    )
    return resp

# 토큰 갱신
@user_router.get("/token/refresh", response_model=TokenRefreshResponse, status_code=status.HTTP_200_OK)
async def token_refresh(
    refresh_token: Annotated[str | None, Cookie()] = None,
    auth_service: Annotated[UserManageService, Depends(UserManageService)] = None,
) -> Response:
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token is missing.")

    try:
        payload = jwt.decode(refresh_token, config.SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        user_id: str = payload.get("user_id")
        token_type: str = payload.get("type")

        if user_id is None or token_type != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token.")

        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = create_access_token(
            data={"user_id": user_id}, expires_delta=access_token_expires
        )
        
        # Redis 세션 업데이트
        await auth_service.update_session(
            id=user_id, 
            access_token=str(new_access_token), 
            expires_in_seconds=int(access_token_expires.total_seconds())
        )

    except InvalidTokenError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token.") from err

    return Response(
        content=TokenRefreshResponse(access_token=str(new_access_token)).model_dump(), status_code=status.HTTP_200_OK
    )

# ID 중복 체크
@user_router.get("/id-check", status_code=status.HTTP_200_OK)
async def id_check(
    id: str,
    auth_service: Annotated[UserManageService, Depends(UserManageService)]
) -> Response:
    await auth_service.check_id_exists(id)
    return Response(content={"detail": "사용 가능한 아이디입니다."}, status_code=status.HTTP_200_OK)
# 아이디 찾기
@user_router.get("/find-id", status_code=status.HTTP_200_OK)
async def find_id(
    name: str,
    phone_number: str,
    auth_service: Annotated[UserManageService, Depends(UserManageService)]
) -> Response:
    id = await auth_service.find_id(name, phone_number)
    return Response(content={"id": id}, status_code=status.HTTP_200_OK)

# 비밀번호 재설정 (비인증 상태)
@user_router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    data: dict, # id, code, name, phone_number, new_password
    auth_service: Annotated[UserManageService, Depends(UserManageService)],
    email_service: Annotated[Email, Depends(Email)]
) -> Response:
    # 1. 인증 코드 검증
    is_valid = await email_service.verify_code(data["id"], data["code"])
    if not is_valid:
        raise HTTPException(status_code=400, detail="인증 번호가 틀렸거나 만료되었습니다.")
    
    # 2. 사용자 정보 검증
    await auth_service.verify_user_for_reset(
        id=data["id"], 
        name=data["name"], 
        phone_number=data["phone_number"]
    )
    
    # 3. 비밀번호 재설정
    await auth_service.reset_password(data["id"], data["new_password"])
    
    return Response(content={"detail": "비밀번호가 성공적으로 변경되었습니다."}, status_code=status.HTTP_200_OK)

# 내 정보 조회
@user_router.get("/me", response_model=UserInfoResponse, status_code=status.HTTP_200_OK)
async def get_my_info(
    id: str,
    user: Annotated[User, Depends(get_request_user)],
) -> User:
    if user.id != id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="요청한 아이디와 로그인된 정보가 일치하지 않습니다."
        )
    return user

# 내 정보 수정
@user_router.patch("/me", response_model=UserInfoResponse, status_code=status.HTTP_200_OK)
async def update_user_me_info(
    update_data: UserUpdateRequest,
    user: Annotated[User, Depends(get_request_user)],
    user_manage_service: Annotated[UserManageService, Depends(UserManageService)],
) -> User:
    updated_user = await user_manage_service.update_user(user=user, data=update_data)
    return updated_user

# 비밀번호 변경 (인증 상태)
@user_router.post("/me/password", status_code=status.HTTP_200_OK)
async def change_password(
    password_data: dict, # old_password, new_password
    user: Annotated[User, Depends(get_request_user)],
    user_manage_service: Annotated[UserManageService, Depends(UserManageService)],
) -> Response:
    await user_manage_service.change_password(
        id=user.id,
        old_password=password_data.get("old_password", ""),
        new_password=password_data.get("new_password", "")
    )
    return Response(content={"detail": "비밀번호가 변경되었습니다."}, status_code=status.HTTP_200_OK)

# 회원탈퇴
@user_router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def withdraw_user(
    password_data: dict, # {"password": "..."} 형태
    user: Annotated[User, Depends(get_request_user)],
    user_manage_service: Annotated[UserManageService, Depends(UserManageService)],
) -> Response:
    await user_manage_service.delete_user(id=user.id, password=password_data.get("password", ""))
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)

# 로그아웃
@user_router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    user: Annotated[User, Depends(get_request_user)],
    user_manage_service: Annotated[UserManageService, Depends(UserManageService)],
) -> Response:
    await user_manage_service.logout(user.id)
    
    resp = Response(content={"detail": "로그아웃 되었습니다."}, status_code=status.HTTP_200_OK)
    # 리프레시 토큰 쿠키 삭제
    resp.delete_cookie(
        key="refresh_token",
        domain=config.COOKIE_DOMAIN or None,
    )
    return resp
