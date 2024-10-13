from pydantic import BaseModel, Field


class DownloadFile(BaseModel):
    name: str
    id: str
    mimeType: str
    path: str


class GetId(BaseModel):
    path: str


class UploadFile(BaseModel):
    name: str
    mimeType: str
    local_path: str
    upload_path: str