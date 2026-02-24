from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.dtos.email import EmailCodeRequest, EmailRequest
from app.utils.common import Email

email_router = APIRouter(prefix="/email", tags=["email"])

# 이메일 인증 번호 발송
@email_router.post("/send-code", status_code=status.HTTP_200_OK)
async def send_verification_email(
    request: EmailRequest,
    email: Annotated[Email, Depends(Email)]
):
    """
    본인 확인을 위해 지정된 이메일 주소로 인증 번호를 발송합니다.
    
    Args:
        request (EmailRequest): 인증을 요청할 이메일 ID
        email (Email): 이메일 발송 유틸리티
        
    Returns:
        dict: 발송 성공 메시지
    """
    try:
        success = await email.send_verification(request.id)
        if success:
            return {"message": "인증 번호가 발송되었습니다."}
    except Exception as e:
        # 이메일 발송 실패 시 (SMTP 설정 오류 등)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"이메일 발송 중 오류가 발생했습니다: {str(e)}"
        ) from e

# 이메일 인증 번호 검증
@email_router.post("/verify-code", status_code=status.HTTP_200_OK)
async def verify_email_code(
    request: EmailCodeRequest,
    email: Annotated[Email, Depends(Email)]
):
    """
    사용자가 입력한 이메일 인증 번호를 검증합니다.
    
    Args:
        request (EmailCodeRequest): 인증을 요청한 이메일 ID 및 입력한 인증 코드
        email (Email): 인증 번호 검증 유틸리티
        
    Returns:
        dict: 인증 성공 메시지
    """
    is_valid = await email.verify_code(request.id, request.code)
    if not is_valid:
        raise HTTPException(status_code=400, detail="인증 번호가 틀렸거나 만료되었습니다.")

    return {"message": "인증에 성공했습니다."}
