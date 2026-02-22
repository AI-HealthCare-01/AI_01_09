from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from app.core import config
from app.models.users import User
from app.repositories.user_repository import UserRepository
from app.utils.common import redis_client

# OAuth2PasswordBearer specifies that the client must send the token in an Authorization header with Bearer scheme.
# The tokenUrl points to the login endpoint (relative to the API root).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


async def get_request_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="로그인이 필요하거나 세션이 만료되었습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        user_email: str = payload.get("user_id")
        token_type: str = payload.get("type")

        if user_email is None or token_type != "access":
            raise credentials_exception

        # Redis 세션 확인
        stored_token = await redis_client.get(f"session:{user_email}")
        if stored_token != token:
            raise credentials_exception

    except InvalidTokenError as err:
        raise credentials_exception from err

    user = await UserRepository().get_by_email(user_email)
    if user is None:
        raise credentials_exception

    return user
