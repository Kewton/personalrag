from pydantic import BaseModel


class Neo4jMessage(BaseModel):
    message: str
