import os
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile, status

from app.dependencies.security import get_request_user
from app.models.upload import Upload
from app.models.user import User

upload_router = APIRouter(prefix="/uploads", tags=["upload"])


@upload_router.post("", status_code=status.HTTP_201_CREATED)
async def upload_file(
    user: Annotated[User, Depends(get_request_user)],
    file: Annotated[UploadFile, File()],
):
    """
    [UPLOAD] 이미지 업로드(처방전/알약 앞/뒤). 업로드 결과(upload_id)로 분석 API 호출
    """
    # Simple upload simulation
    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = f"app/static/uploads/{unique_filename}"

    # Normally we save the file here

    upload_record = await Upload.create(
        user=user, original_name=file.filename, file_path=file_path, file_type=file.content_type or "image/jpeg"
    )

    return {"upload_id": upload_record.id, "file_url": f"/static/uploads/{unique_filename}"}
