from app.models.task_result import TaskResult
from app.db.session import SessionLocal
import datetime


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_task(task_id: str, task_name: str):
    db = next(get_db())
    db_task = TaskResult(task_id=task_id, task_name=task_name)
    db.add(db_task)
    db.commit()


def update_task(_task_id, _remarks):
    db = next(get_db())
    db_task = db.query(TaskResult).filter(TaskResult.task_id == _task_id).first()
    if db_task:
        db_task.remarks = _remarks
        db_task.update_time = datetime.datetime.now()
        db.commit()


def close_task(_task_id, _result, _remarks):
    db = next(get_db())
    db_task = db.query(TaskResult).filter(TaskResult.task_id == _task_id).first()
    if db_task:
        db_task.status = "end"
        db_task.result = _result
        db_task.remarks = _remarks
        db_task.end_time = datetime.datetime.now()
        db_task.update_time = datetime.datetime.now()
        db.commit()


def get_task_status(task_id: str):
    db = next(get_db())
    db_task = db.query(TaskResult).filter(TaskResult.task_id == task_id).first()
    if db_task:
        return {
            "task_id": task_id,
            "task_name": db_task.task_name,
            "status": db_task.status,
            "result": db_task.result,
            "remarks": db_task.remarks,
            "start_time": db_task.start_time,
            "end_time": db_task.end_time,
            "update_time": db_task.update_time,
        }
    else:
        return {"task_id": task_id, "status": "not_found"}