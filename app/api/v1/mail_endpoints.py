from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Path
from app.schemas.mail.gmail import SendMail, ReadMail
from app.core.googleapis.gmail.send import send_email
from app.core.googleapis.gmail.readonly import get_emails_by_subject
from app.utils.logger import declogger, writeinfolog, writedebuglog, writeerrorlog


router = APIRouter()


@router.post("/sendmail")
def sendmail(request: SendMail):
    try:
        if send_email(request.to_email, request.subject, request.body):
            return {"result": "succcess"}
        else:
            raise HTTPException(status_code=500, detail=f"Request failed")
    except Exception as e:
        print(e)
        writeerrorlog(e)
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")


@router.post("/readmail")
def readmail(request: ReadMail):
    try:
        return {"result": get_emails_by_subject(request.subject_keyword)}
    except Exception as e:
        print(e)
        writeerrorlog(e)
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")