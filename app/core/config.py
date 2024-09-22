import os
from dotenv import load_dotenv


def ensure_directory_exists(db_path: str):
    # ディレクトリ部分を抽出
    directory = os.path.dirname(db_path.replace("sqlite:///", ""))
    
    # ディレクトリが存在しない場合は作成
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory {directory} created.")
    else:
        print(f"Directory {directory} already exists.")


# .envファイルをロード
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL', "sqlite:///./test.db")
ensure_directory_exists(SQLALCHEMY_DATABASE_URL)
INDEX_SAVE_DIR = os.path.join(os.getenv('PROJECT_ROOT_DIRECTORY', "./"), "storage")
MODEL_DOWNLOAD_DIR = os.path.join(os.getenv('PROJECT_ROOT_DIRECTORY', "./"), "vectordb")
DOC_DOWNLOAD_DIR = os.path.join(os.getenv('PROJECT_ROOT_DIRECTORY', "./"), "rag")
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', "")
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY', "")
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["HF_HOME"] = os.path.join(os.getenv('PROJECT_ROOT_DIRECTORY', "./"), "cache")
