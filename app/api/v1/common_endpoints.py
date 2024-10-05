from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Path
from app.utils.logger import declogger, writeinfolog, writedebuglog
from app.services.db.task_result import get_task_status, create_task


router = APIRouter()


@declogger
def hello():
    writedebuglog("logtest_debug")
    writeinfolog("logtest_info")
    return


@router.get("/",
            summary="hello world",
            description="hello worldです。疎通確認に使用してください。")
def home_hello_world():
    hello()
    return {"result": "hello world"}


@router.get("/check-task/{task_id}")
async def check_task(task_id: str = Path(..., description="Enter the task ID. Example: default_task_id")):
    return get_task_status(task_id)
