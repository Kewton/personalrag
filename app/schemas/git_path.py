from pydantic import BaseModel

class GitPath(BaseModel):
    githuburl: str
