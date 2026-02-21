from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from fastapi.responses import JSONResponse as Response

from app.core import config
from app.core.config import Env
from app.dtos.auth import LoginRequest, LoginResponse, SignUpRequest, TokenRefreshResponse, EmailRequest
from app.services.auth import AuthService
from app.services.jwt import JwtService
from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, EmailStr
from app.services.auth import AuthService

api_router = APIRouter(prefix="/api", tags=["api"])

