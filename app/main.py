from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.apis.v1 import v1_routers
from app.db.databases import initialize_tortoise

import logging

app = FastAPI(
    default_response_class=ORJSONResponse, docs_url="/api/docs", redoc_url="/api/redoc", openapi_url="/api/openapi.json"
)
initialize_tortoise(app)


# Tortoise-ORM의 SQL 로그를 활성화
# logging.basicConfig(level=logging.DEBUG)
# logging.getLogger("tortoise.db_client").setLevel(logging.DEBUG)

# [추가된 기능] 정적 파일 및 템플릿 설정
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/join", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("join.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/mypage", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("mypage.html", {"request": request})

@app.get("/find-id-pw", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("find_account.html", {"request": request})

app.include_router(v1_routers)
