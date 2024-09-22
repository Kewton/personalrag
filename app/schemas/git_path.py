from pydantic import BaseModel, Field

class GitPath(BaseModel):
    githuburl: str = Field(..., title="githuburl", description="githubのURL")
