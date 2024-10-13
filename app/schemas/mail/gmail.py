from pydantic import BaseModel, Field


class SendMail(BaseModel):
    to_email: str
    subject: str
    body: str


class ReadMail(BaseModel):
    subject_keyword: str
