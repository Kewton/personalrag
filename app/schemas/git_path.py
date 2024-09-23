from pydantic import BaseModel, Field
from app.core.config import SAMPLE_GITHUB_URL

test = "aaaaa"

class GitPath(BaseModel):
    githuburl: str = Field(
        default=SAMPLE_GITHUB_URL,  # デフォルト値
        title="githuburl",
        description="GitHubのURL",
        example="https://github.com/example/repository"  # Swagger UIに表示されるサンプル値
    )
