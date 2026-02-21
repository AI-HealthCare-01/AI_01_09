from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from fastapi.responses import JSONResponse as Response

from app.core import config
from app.core.config import Env
from app.dtos.auth import LoginRequest, LoginResponse, SignUpRequest, TokenRefreshResponse, EmailRequest, EmailCodeRequest
from app.services.auth import AuthService
from app.services.jwt import JwtService
from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, EmailStr
from app.utils.common import Email

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    request: SignUpRequest,
    auth_service: Annotated[AuthService, Depends(AuthService)],
) -> Response:
    await auth_service.signup(request)
    return Response(content={"detail": "회원가입이 성공적으로 완료되었습니다."}, status_code=status.HTTP_201_CREATED)


@auth_router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(
    request: LoginRequest,
    auth_service: Annotated[AuthService, Depends(AuthService)],
) -> Response:
    user = await auth_service.authenticate(request)
    tokens = await auth_service.login(user)
    resp = Response(
        content=LoginResponse(access_token=str(tokens["access_token"])).model_dump(), status_code=status.HTTP_200_OK
    )
    resp.set_cookie(
        key="refresh_token",
        value=str(tokens["refresh_token"]),
        httponly=True,
        secure=True if config.ENV == Env.PROD else False,
        domain=config.COOKIE_DOMAIN or None,
        expires=tokens["access_token"].payload["exp"],
    )
    return resp


@auth_router.get("/token/refresh", response_model=TokenRefreshResponse, status_code=status.HTTP_200_OK)
async def token_refresh(
    jwt_service: Annotated[JwtService, Depends(JwtService)],
    refresh_token: Annotated[str | None, Cookie()] = None,
) -> Response:
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token is missing.")
    access_token = jwt_service.refresh_jwt(refresh_token)
    return Response(
        content=TokenRefreshResponse(access_token=str(access_token)).model_dump(), status_code=status.HTTP_200_OK
    )


@auth_router.post("/send-code", status_code=status.HTTP_200_OK)
async def send_verification_email(
    request: EmailRequest,
    email: Annotated[Email, Depends(Email)]
):
    """
    이메일 인증 번호 발송 엔드포인트
    """
    try:
        success = await email.send_verification(request.email)
        if success:
            return {"message": "인증 번호가 발송되었습니다."}
    except Exception as e:
        # 이메일 발송 실패 시 (SMTP 설정 오류 등)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"이메일 발송 중 오류가 발생했습니다: {str(e)}"
        )

@auth_router.post("/verify-code", status_code=status.HTTP_200_OK)
async def verify_email_code(
    request: EmailCodeRequest,
    email: Annotated[Email, Depends(Email)]
):
    """
    발송된 인증 번호를 검증하는 엔드포인트 (프론트에서 즉시 확인용)
    """
    is_valid = await email.verify_code(request.email, request.code)
    if not is_valid:
        raise HTTPException(status_code=400, detail="인증 번호가 틀렸거나 만료되었습니다.")
    
    return {"message": "인증에 성공했습니다."}