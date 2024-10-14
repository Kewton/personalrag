from app.models.key_value_store import KeyValueStore
from app.db.session import SessionLocal
import json
import datetime


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def set_key_value(key: str, value: dict):
    try:
        db = next(get_db())
        value_json = json.dumps(value)  # JSON形式の値を文字列に変換
        db_record = db.query(KeyValueStore).filter(KeyValueStore.key == key).first()
        
        if db_record:
            db_record.value = value_json
            db_record.updated_at = datetime.datetime.now()
        else:
            db_record = KeyValueStore(key=key, value=value_json)
            db.add(db_record)
        
        db.commit()
        return {"result": "success", "key": key}
    except Exception as e:
        print(e)
        return {"result": "failure"}


def get_value_by_key(key: str):
    db = next(get_db())
    db_record = db.query(KeyValueStore).filter(KeyValueStore.key == key).first()
    
    if db_record:
        return json.loads(db_record.value)  # JSON形式の文字列を辞書型に変換して返す
    else:
        return None


def delete_key_value(key: str):
    db = next(get_db())
    db_record = db.query(KeyValueStore).filter(KeyValueStore.key == key).first()
    
    if db_record:
        db.delete(db_record)
        db.commit()
        return True
    else:
        return False
