from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import SQLALCHEMY_DATABASE_URL
from app.utils.logger import setup_logging, writedebuglog, writeinfolog, writeerrorlog, declogger
import os

setup_logging()

@declogger
def create_engine_with_fallback(db_url):
    try:
        # エンジンの作成
        engine = create_engine(db_url, connect_args={"check_same_thread": False})
        # 実際に接続を試みてエラーを確認
        with engine.connect() as connection:
            pass
        writeinfolog(f"データベースに正常に接続しました: {db_url}")
        return engine
    except Exception as e:
        writeerrorlog(f"エンジンの作成に失敗しました: {e}")
        # SQLiteのURLか確認
        if db_url.startswith("sqlite:///"):
            # 元のファイルパスを取得
            original_db_path = db_url.replace("sqlite:///", "")
            base, ext = os.path.splitext(original_db_path)
            # 新しいファイル名を作成
            new_db_path = f"{base}_backup{ext}"
            new_db_url = f"sqlite:///{new_db_path}"
            writeinfolog(f"新しいデータベースファイルを作成します: {new_db_path}")
            try:
                # 新しいエンジンを作成
                engine = create_engine(new_db_url, connect_args={"check_same_thread": False})
                # 必要に応じてテーブルの作成などを行う
                # 例: Base.metadata.create_all(engine)
                writeinfolog(f"新しいデータベースに接続しました: {new_db_url}")
                return engine
            except Exception as e2:
                writeerrorlog(f"新しいデータベースの作成にも失敗しました: {e2}")
                raise e2
        else:
            # SQLite以外のデータベースの場合の処理
            writeerrorlog("SQLite以外のデータベースに対するエラーハンドリングが必要です。")
            raise e


engine = create_engine_with_fallback(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
