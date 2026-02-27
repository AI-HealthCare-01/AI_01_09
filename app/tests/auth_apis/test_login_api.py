from httpx import ASGITransport, AsyncClient  # type: ignore[import-untyped, import-not-found]
from starlette import status
from tortoise.contrib.test import TestCase

from app.main import app


class TestLoginAPI(TestCase):
    async def test_login_success(self):
        # 먼저 사용자 등록
        signup_data = {
            "id": "login_test@example.com",
            "password": "Password123!",
            "name": "로그인테스터",
            "nickname": "Tester",
            "phone_number": "01011112222",
            "resident_registration_number": "900101-1234567",
            "is_terms_agreed": True,
            "is_privacy_agreed": True,
        }
        login_data = {"username": "login_test@example.com", "password": "Password123!", "remember_me": False}

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            await client.post("/api/v1/users/signup", json=signup_data)

            # 로그인 시도 (Form data)
            response = await client.post("/api/v1/users/login", data=login_data)
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        # 쿠키 검증 대신 응답 헤더 확인
        assert any("refresh_token" in header for header in response.headers.get_list("set-cookie"))

    async def test_login_invalid_credentials(self):
        login_data = {"username": "nonexistent@example.com", "password": "WrongPassword123!", "remember_me": False}
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post("/api/v1/users/login", data=login_data)

        # 401 Unauthorized expected for invalid credentials in new implementation
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
