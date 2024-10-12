from pydantic import BaseModel, Field
from app.core.config import SAMPLE_GITHUB_URL


class GitPath(BaseModel):
    githuburl: str = Field(
        default=SAMPLE_GITHUB_URL,  # デフォルト値
        title="githuburl",
        description="GitHubのURL",
        json_schema_extra={"example": "https://github.com/example/repository"}  # Swagger UIに表示されるサンプル値
    )
