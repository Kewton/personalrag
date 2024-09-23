from pydantic import BaseModel

class SimilaritySearchRequest(BaseModel):
    query: str
    modelurl: str = "https://huggingface.co/intfloat/multilingual-e5-large"