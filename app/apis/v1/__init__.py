from fastapi import APIRouter

from app.apis.v1.auth_routers import auth_router
from app.apis.v1.user_routers import user_router

# [추가된 기능] 라우터 모듈 import
from app.apis.v1.guide_routers import guide_router
from app.apis.v1.chat_routers import chat_router
from app.apis.v1.ocr_routers import ocr_router
from app.apis.v1.media_routers import media_router
from app.apis.v1.notification_routers import notification_router

v1_routers = APIRouter(prefix="/api/v1")
v1_routers.include_router(auth_router)
v1_routers.include_router(user_router)

# [추가된 기능] 라우터 엔드포인트 등록
v1_routers.include_router(guide_router)
v1_routers.include_router(chat_router)
v1_routers.include_router(ocr_router)
v1_routers.include_router(media_router)
v1_routers.include_router(notification_router)
