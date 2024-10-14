from fastapi import APIRouter, Depends
from app.models.key_value_store import KeyValueStore
from app.db.session import SessionLocal
from app.services.db.key_value_store import set_key_value, get_value_by_key, delete_key_value
from app.schemas.datastore.datastore import KeyValueStore

router = APIRouter()


@router.post("/store")
def create_or_update_key_value(request: KeyValueStore):
    return set_key_value(request.key, request.value)


@router.get("/store/{key}")
def read_key_value(key: str):
    print("aaa")
    value = get_value_by_key(key)
    if value:
        return {"key": key, "value": value}
    else:
        return {"error": "Key not found"}


@router.delete("/store/{key}")
def remove_key_value(key: str):
    success = delete_key_value(key)
    if success:
        return {"message": "Key deleted successfully"}
    else:
        return {"error": "Key not found"}
