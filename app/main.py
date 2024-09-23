from fastapi import FastAPI
from app.api.v1 import endpoints
from app.db.session import engine
from app.db.base import Base
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

app = FastAPI(
    title="My API",
    description="APIドキュメント",
    version="1.0.0",
    root_path="/rag-api",
    swagger_ui_parameters={
        "docExpansion": "list",  # サイドバーにAPIリンクを表示
        "defaultModelsExpandDepth": -1  # モデルはサイドバーに表示しない
    }
)

app.include_router(endpoints.router)

# データベースのテーブルを作成
Base.metadata.create_all(bind=engine)

app.include_router(endpoints.router)
