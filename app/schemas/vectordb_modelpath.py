from pydantic import BaseModel

class VectorDBModelPath(BaseModel):
    modelurl: str = "https://huggingface.co/intfloat/multilingual-e5-large"