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
    SocialLoginRequest,
)
from app.models.user import User
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
    """
    일반 회원가입을 처리합니다.
    
    Args:
        request (SignUpRequest): 회원가입 요청 데이터
        auth_service (UserManageService): 사용자 관리 서비스
    
    Returns:
        Response: 성공 메시지
    """
    await auth_service.signup(request)
    return Response(content={"detail": "회원가입이 성공적으로 완료되었습니다."}, status_code=status.HTTP_201_CREATED)

# 로그인
@user_router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[UserManageService, Depends(UserManageService)],
    remember_me: Annotated[bool, Form()] = False,
) -> Response:
    """
    사용자 로그인을 처리하고 JWT 토큰을 발급합니다.
    
    Args:
        form_data (OAuth2PasswordRequestForm): 로그인 ID 및 비밀번호 정보
        auth_service (UserManageService): 사용자 관리 서비스
        remember_me (bool): 자동 로그인 유지 여부
    
    Returns:
        Response: 로그인 결과 및 토큰 정보
    """
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
    """
    리프레시 토큰을 사용하여 액세스 토큰을 갱신합니다.
    
    Args:
        refresh_token (str): 쿠키에서 추출한 리프레시 토큰
        auth_service (UserManageService): 사용자 관리 서비스
    
    Returns:
        Response: 새로운 액세스 토큰 정보
    """
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
    """
    아이디 중복 여부를 확인합니다.
    
    Args:
        id (str): 중복 확인을 요청한 아이디
        auth_service (UserManageService): 사용자 관리 서비스
    
    Returns:
        Response: 중복 여부 확인 결과 메시지
    """
    await auth_service.check_id_exists(id)
    return Response(content={"detail": "사용 가능한 아이디입니다."}, status_code=status.HTTP_200_OK)

# 아이디 찾기
@user_router.get("/find-id", status_code=status.HTTP_200_OK)
async def find_id(
    name: str,
    phone_number: str,
    auth_service: Annotated[UserManageService, Depends(UserManageService)]
) -> Response:
    """
    이름과 휴대폰 번호로 사용자 아이디를 찾습니다.
    
    Args:
        name (str): 사용자 이름
        phone_number (str): 사용자 휴대폰 번호
        auth_service (UserManageService): 사용자 관리 서비스
    
    Returns:
        Response: 찾은 아이디 정보
    """
    id = await auth_service.find_id(name, phone_number)
    return Response(content={"id": id}, status_code=status.HTTP_200_OK)

# 비밀번호 재설정 (비인증 상태)
@user_router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    data: dict, # id, code, name, phone_number, new_password
    auth_service: Annotated[UserManageService, Depends(UserManageService)],
    email_service: Annotated[Email, Depends(Email)]
) -> Response:
    """
    비밀번호를 분실한 경우 인증 절차를 거쳐 재설정합니다.
    
    Args:
        data (dict): 아이디, 인증코드, 이름, 휴대폰번호, 새 비밀번호 포함
        auth_service (UserManageService): 사용자 관리 서비스
        email_service (Email): 이메일/문자 인증 서비스
    
    Returns:
        Response: 비밀번호 변경 결과 메시지
    """
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
    """
    현재 로그인된 사용자의 프로필 정보를 조회합니다.
    
    Args:
        id (str): 조회를 요청한 사용자 아이디
        user (User): 인증된 현재 사용자 객체
    
    Returns:
        User: 사용자 프로필 정보
    """
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
    """
    사용자의 프로필 정보(닉네임, 연락처 등)를 업데이트합니다.
    
    Args:
        update_data (UserUpdateRequest): 수정할 프로필 데이터
        user (User): 인증된 현재 사용자 객체
        user_manage_service (UserManageService): 사용자 관리 서비스
    
    Returns:
        User: 업데이트된 사용자 정보
    """
    updated_user = await user_manage_service.update_user(user=user, data=update_data)
    return updated_user

# 비밀번호 변경 (인증 상태)
@user_router.post("/me/password", status_code=status.HTTP_200_OK)
async def change_password(
    password_data: dict, # old_password, new_password
    user: Annotated[User, Depends(get_request_user)],
    user_manage_service: Annotated[UserManageService, Depends(UserManageService)],
) -> Response:
    """
    로그인된 상태에서 기존 비밀번호를 확인한 후 새로운 비밀번호로 변경합니다.
    
    Args:
        password_data (dict): 기존 비밀번호 및 새 비밀번호
        user (User): 인증된 현재 사용자 객체
        user_manage_service (UserManageService): 사용자 관리 서비스
    
    Returns:
        Response: 비밀번호 변경 결과 메시지
    """
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
    """
    사용자의 계정을 삭제하고 회원을 탈퇴 처리합니다.
    
    Args:
        password_data (dict): 본인 확인을 위한 비밀번호
        user (User): 인증된 현재 사용자 객체
        user_manage_service (UserManageService): 사용자 관리 서비스
    
    Returns:
        Response: 성공 시 빈 응답 (204)
    """
    await user_manage_service.delete_user(id=user.id, password=password_data.get("password", ""))
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)

# 로그아웃
@user_router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    user: Annotated[User, Depends(get_request_user)],
    user_manage_service: Annotated[UserManageService, Depends(UserManageService)],
) -> Response:
    """
    로그아웃을 처리하고 세션 및 리프레시 토큰 쿠키를 무효화합니다.
    
    Args:
        user (User): 인증된 현재 사용자 객체
        user_manage_service (UserManageService): 사용자 관리 서비스
    
    Returns:
        Response: 로그아웃 처리 결과 메시지
    """
    await user_manage_service.logout(user.id)
    
    resp = Response(content={"detail": "로그아웃 되었습니다."}, status_code=status.HTTP_200_OK)
    # 리프레시 토큰 쿠키 삭제
    resp.delete_cookie(
        key="refresh_token",
        domain=config.COOKIE_DOMAIN or None,
    )
    return resp

# ==========================================
# [추가된 기능] REQ-USER-003: 네이버 소셜 로그인
# ==========================================
@user_router.get("/auth/naver")
async def naver_login_initiate():
    """
    네이버 로그인 페이지로 리다이렉트하여 인증 프로세스를 시작합니다.
    """
    naver_client_id = config.NAVER_CLIENT_ID
    redirect_uri = config.NAVER_REDIRECT_URI
    state = "random_state_string"
    auth_url = (
        f"https://nid.naver.com/oauth2.0/authorize?response_type=code"
        f"&client_id={naver_client_id}&redirect_uri={redirect_uri}&state={state}"
    )
    from fastapi.responses import RedirectResponse
    return RedirectResponse(auth_url)

@user_router.get("/auth/naver/callback")
async def naver_login_callback(
    code: str,
    state: str,
    auth_service: Annotated[UserManageService, Depends(UserManageService)],
) -> Response:
    """
    네이버 인증 콜백을 처리하고 소셜 로그인을 수행합니다.
    
    Args:
        code (str): 네이버에서 발급한 인증 코드
        state (str): 상태 확인 값
        auth_service (UserManageService): 사용자 관리 서비스
    
    Returns:
        Response: 로그인 결과 및 토큰 정보
    """
    # dummy data for router demonstration
    social_data = SocialLoginRequest(
        id="social_user@naver.com",
        name="네이버사용자",
        nickname="naver_user_123", # 난수 기반 고유값은 서비스 레이어에서 처리
        phone_number="01012345678",
        birthday="1990-01-01",
        gender="M",
        social_id="naver_unique_id_xyz",
        provider="naver"
    )
    tokens = await auth_service.social_login(social_data)
    
    resp = Response(
        content=LoginResponse(
            access_token=tokens["access_token"],
            token_type=tokens["token_type"],
            id=tokens["id"]
        ).model_dump(),
        status_code=status.HTTP_200_OK
    )

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

# ==========================================
# [추가된 기능] REQ-USER-003: 카카오 소셜 로그인
# ==========================================
@user_router.get("/auth/kakao")
async def kakao_login_initiate():
    """
    카카오 로그인 페이지로 리다이렉트하여 인증 프로세스를 시작합니다.
    """
    kakao_client_id = config.KAKAO_CLIENT_ID
    redirect_uri = config.KAKAO_REDIRECT_URI
    auth_url = (
        f"https://kauth.kakao.com/oauth/authorize?response_type=code"
        f"&client_id={kakao_client_id}&redirect_uri={redirect_uri}"
    )
    from fastapi.responses import RedirectResponse
    return RedirectResponse(auth_url)

@user_router.get("/auth/kakao/callback")
async def kakao_login_callback(
    code: str,
    auth_service: Annotated[UserManageService, Depends(UserManageService)],
) -> Response:
    """
    카카오 인증 콜백을 처리하고 소셜 로그인을 수행합니다.
    
    Args:
        code (str): 카카오에서 발급한 인증 코드
        auth_service (UserManageService): 사용자 관리 서비스
    
    Returns:
        Response: 로그인 결과 및 토큰 정보
    """
    # dummy data for router demonstration
    social_data = SocialLoginRequest(
        id="kakao_user@kakao.com",
        name="카카오사용자",
        nickname="kakao_user_456",
        phone_number="01098765432",
        birthday="1995-05-05",
        gender="F",
        social_id="kakao_unique_id_abc",
        provider="kakao"
    )
    tokens = await auth_service.social_login(social_data)
    
    resp = Response(
        content=LoginResponse(
            access_token=tokens["access_token"],
            token_type=tokens["token_type"],
            id=tokens["id"]
        ).model_dump(),
        status_code=status.HTTP_200_OK
    )

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
