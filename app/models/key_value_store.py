from app.db.base import Base
from sqlalchemy import Column, String, DateTime, Text
import datetime


class KeyValueStore(Base):
    __tablename__ = "key_value_store"

    # キー: 一意にデータを識別するための識別子
    key = Column(String(255), primary_key=True, index=True, nullable=False)

    # バリュー: JSON形式のデータ（文字列として保存）
    value = Column(Text, nullable=False)

    # 作成時刻: データの作成日時
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)

    # 更新時刻: データの更新日時
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, nullable=False)

    def __repr__(self):
        return f"<KeyValueStore(key='{self.key}', value='{self.value}')>"
