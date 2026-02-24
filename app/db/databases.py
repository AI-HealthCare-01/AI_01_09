from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from app.core import config
from app.core.config import Env

TORTOISE_APP_MODELS = [
    "aerich.models",
    "app.models.users",
    "app.models.alarm",
    "app.models.alarmHistory",
    "app.models.allergy",
    "app.models.chatMessage",
    "app.models.chronicDisease",
    "app.models.currentMed",
    "app.models.llmLifeGuide",
    "app.models.multimodalAsset",
    "app.models.prescription",
    "app.models.prescriptionDrug",
    "app.models.pillRecognition",
    "app.models.systemLog",
    "app.models.upload",
    "app.models.ocrHistory",
    "app.models.cnnHistory",
]

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",
            "dialect": "asyncmy",
            "credentials": {
                "host": config.DB_HOST,
                "port": config.DB_PORT,
                "user": config.DB_USER,
                "password": config.DB_PASSWORD,
                "database": config.DB_NAME,
                "connect_timeout": config.DB_CONNECT_TIMEOUT,
                "maxsize": config.DB_CONNECTION_POOL_MAXSIZE,
            },
        },
    },
    "apps": {
        "models": {
            "models": TORTOISE_APP_MODELS,
        },
    },
    "timezone": "Asia/Seoul",
}


def initialize_tortoise(app: FastAPI) -> None:
    Tortoise.init_models(TORTOISE_APP_MODELS, "models")
    
    # 여기서 generate_schemas=False로 두고, startup에서만 제어합니다.
    register_tortoise(
        app, 
        config=TORTOISE_ORM, 
        generate_schemas=False, 
        add_exception_handlers=True
    )

    @app.on_event("startup")
    async def on_startup():
        if config.ENV == Env.LOCAL:
            print(f"Current Environment: {config.ENV}. Resetting database...")
            
            # 1. DB 연결 객체 가져오기
            conn = Tortoise.get_connection("default")
            
            # 2. 외래 키 체크 비활성화 (MySQL에서 테이블을 순서 상관없이 지우기 위해 필수)
            await conn.execute_query("SET FOREIGN_KEY_CHECKS = 0;")
            
            try:
                # 3. Tortoise에 등록된 모든 모델의 테이블을 순회하며 DROP
                # Tortoise.apps 딕셔너리에는 모든 앱과 모델 정보가 들어있습니다.
                for app_name, models in Tortoise.apps.items():
                    for model_name, model_obj in models.items():
                        table_name = model_obj._meta.db_table
                        print(f"Dropping table: {table_name}")
                        await conn.execute_query(f"DROP TABLE IF EXISTS `{table_name}`;")
                
                # 4. Aerich 마이그레이션 테이블도 명시적으로 삭제
                await conn.execute_query("DROP TABLE IF EXISTS `aerich`;")
                
                print("All tables dropped. Re-generating schemas...")
                
                # 5. 스키마 새로 생성 (이제 테이블이 없으므로 safe=False도 에러 안 남)
                await Tortoise.generate_schemas(safe=False)
                print("Database schemas re-generated successfully.")
                
            finally:
                # 6. 외래 키 체크 다시 활성화
                await conn.execute_query("SET FOREIGN_KEY_CHECKS = 1;")