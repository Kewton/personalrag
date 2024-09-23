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

print(f"SQLALCHEMY_DATABASE_URL = {os.getenv('SQLALCHEMY_DATABASE_URL')}")
print(f"PROJECT_ROOT_DIRECTORY_1 = {os.getenv('PROJECT_ROOT_DIRECTORY')}")
print(f"PROJECT_ROOT_DIRECTORY_2 = {os.getenv('PROJECT_ROOT_DIRECTORY', './')}")
print(f"OPENAI_API_KEY = {os.getenv('OPENAI_API_KEY')}")
print(f"CLAUDE_API_KEY = {os.getenv('CLAUDE_API_KEY')}")


SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL', "sqlite:///./test.db")
ensure_directory_exists(SQLALCHEMY_DATABASE_URL)
INDEX_SAVE_DIR = os.path.join(os.getenv('PROJECT_ROOT_DIRECTORY', "./"), "storage")
MODEL_DOWNLOAD_DIR = os.path.join(os.getenv('PROJECT_ROOT_DIRECTORY', "./"), "vectordb")
DOC_DOWNLOAD_DIR = os.path.join(os.getenv('PROJECT_ROOT_DIRECTORY', "./"), "rag")
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', "")
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY', "")
SAMPLE_GITHUB_URL = os.getenv('SAMPLE_GITHUB_URL', "")
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["HF_HOME"] = os.path.join(os.getenv('PROJECT_ROOT_DIRECTORY', "./"), "cache")

print(f"SQLALCHEMY_DATABASE_URL={SQLALCHEMY_DATABASE_URL}")
print(f"INDEX_SAVE_DIR={INDEX_SAVE_DIR}")
print(f"MODEL_DOWNLOAD_DIR={MODEL_DOWNLOAD_DIR}")
print(f"DOC_DOWNLOAD_DIR={DOC_DOWNLOAD_DIR}")
print(f"OPENAI_API_KEY={OPENAI_API_KEY}")
print(f"CLAUDE_API_KEY={CLAUDE_API_KEY}")
