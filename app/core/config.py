import os
from dotenv import load_dotenv

# .envファイルをロード
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL', "sqlite:///./test.db")
INDEX_SAVE_DIR = os.path.join(os.getenv('PROJECT_ROOT_DIRECTORY', "./"), "storage")
MODEL_DOWNLOAD_DIR = os.path.join(os.getenv('PROJECT_ROOT_DIRECTORY', "./"), "vectordb")
DOC_DOWNLOAD_DIR = os.path.join(os.getenv('PROJECT_ROOT_DIRECTORY', "./"), "rag")

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["HF_HOME"] = os.path.join(os.getenv('PROJECT_ROOT_DIRECTORY', "./"), "cache")