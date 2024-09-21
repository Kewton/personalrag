from sqlalchemy.orm import Session
from app.db.session import engine
from app.db.base import Base


def reset_database():
    # すべてのテーブルを削除
    Base.metadata.drop_all(bind=engine)
    # テーブルを再作成
    Base.metadata.create_all(bind=engine)
    print("Database has been reset.")
