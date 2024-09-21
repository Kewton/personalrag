from app.db.base import Base
from sqlalchemy import Column, String, DateTime, Text
import datetime


class TaskResult(Base):
    __tablename__ = "task_results"

    # タスクID: 一意にタスクを識別するための識別子
    task_id = Column(String(50), primary_key=True, index=True, nullable=False)

    # タスク名: タスクの名称やタイトル
    task_name = Column(String(255), nullable=False)

    # ステータス: タスクの現在の状態
    status = Column(String(50), default="in_progress", nullable=False)

    # 結果: タスクの結果や成果物
    result = Column(Text, nullable=True)

    # 開始時刻: タスクの開始日時
    start_time = Column(DateTime, default=datetime.datetime.now, nullable=True)

    # 終了時刻: タスクの終了日時
    end_time = Column(DateTime, nullable=True)

    # 更新時刻: タスクの終了日時
    update_time = Column(DateTime, nullable=True)

    # 備考: タスクに関する追加情報やメモ
    remarks = Column(Text, nullable=True)

    def __repr__(self):
        return f"<TaskResult(task_id='{self.task_id}', task_name='{self.task_name}', status='{self.status}')>"