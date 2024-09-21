from pydantic import BaseModel

class SimilaritySearchRequest(BaseModel):
    query: str
    modelurl: str