from pydantic import BaseModel


class Neo4jSchema(BaseModel):
    message: str
