from fastapi import FastAPI
from app.api.v1 import vectorrag_endpoints
from app.api.v1 import localllm_endpoints
from app.api.v1 import common_endpoints
from app.api.v1 import graphrag_endpoints
from app.api.v1 import mail_endpoints
from app.api.v1 import websearch_endpoints
from app.api.v1 import drive_endpoints
from app.api.v1 import datastore_endpoints
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

app.include_router(common_endpoints.router, prefix="/v1")
app.include_router(vectorrag_endpoints.router, prefix="/v1")
app.include_router(localllm_endpoints.router, prefix="/v1")
app.include_router(graphrag_endpoints.router, prefix="/v1")
app.include_router(mail_endpoints.router, prefix="/v1")
app.include_router(websearch_endpoints.router, prefix="/v1")
app.include_router(drive_endpoints.router, prefix="/v1")
app.include_router(datastore_endpoints.router, prefix="/v1")


# テーブルが存在しない場合に作成
Base.metadata.create_all(bind=engine)
