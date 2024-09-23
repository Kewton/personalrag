from pydantic import BaseModel

class ModelPath(BaseModel):
    modelurl: str = "https://huggingface.co/intfloat/multilingual-e5-large"