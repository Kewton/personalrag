from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test__home_hello_world():
    response = client.get("/v1/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test__check_task():
    response = client.get("/v1/check-task/a")
    assert response.status_code == 200
    assert response.json() == {"task_id": "a", "status": "not_found"}
