from pydantic import BaseModel, Field


class DdgsText(BaseModel):
    keywords: str
    region: str = "jp-jp"
    max_results: int = 4


class Response2md(BaseModel):
    url: str
