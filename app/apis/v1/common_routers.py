from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.dtos.email import EmailCodeRequest, EmailRequest
from app.utils.common import Email

common_router = APIRouter(prefix="/common", tags=["common"])


# 이메일 인증 번호 발송
@common_router.post("/send-code", status_code=status.HTTP_200_OK)
async def send_verification_email(request: EmailRequest, email: Annotated[Email, Depends(Email)]):
    """
    이메일 인증 번호 발송 엔드포인트
    """
    try:
        print(request.id)
        success = await email.send_verification(request.id)
        if success:
            return {"message": "인증 번호가 발송되었습니다."}
    except Exception as e:
        # 이메일 발송 실패 시 (SMTP 설정 오류 등)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"이메일 발송 중 오류가 발생했습니다: {str(e)}"
        ) from e


# 이메일 인증 번호 검증
@common_router.post("/verify-code", status_code=status.HTTP_200_OK)
async def verify_email_code(request: EmailCodeRequest, email: Annotated[Email, Depends(Email)]):
    """
    발송된 인증 번호를 검증하는 엔드포인트 (프론트에서 즉시 확인용)
    """
    is_valid = await email.verify_code(request.id, request.code)
    if not is_valid:
        raise HTTPException(status_code=400, detail="인증 번호가 틀렸거나 만료되었습니다.")

    return {"message": "인증에 성공했습니다."}
