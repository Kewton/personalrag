from pydantic import BaseModel, Field


class KeyValueStore(BaseModel):
    key: str
    value: dict
