from pydantic import BaseModel, Field


class OllamaChat(BaseModel):
    model: str = Field(
        default="elyza:jp8b",  # デフォルト値
        title="model",
        description="model",
        json_schema_extra={"example": "elyza:jp8b"}  # Swagger UIに表示されるサンプル値
    )
    stream: bool = Field(
        default=False,  # デフォルト値
        title="stream",
        description="stream",
        json_schema_extra={"example": "stream"}  # Swagger UIに表示されるサンプル値
    )
    messages: list[dict] = Field(
        default=[{"role": "user", "content": "why is the sky blue?"}],  # デフォルト値
        title="messages",
        description="messages",
        json_schema_extra={"example": "messages"}  # Swagger UIに表示されるサンプル値
    )