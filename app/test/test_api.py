import pytest
from fastapi.testclient import TestClient
from main import app
from core.database import get_db

api_url = '/v1/tasks'


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client  # testing happens here


@pytest.fixture(scope='function')
def db_session():
    session = get_db()
    try:
        yield session
    finally:
        session.close()


def test_create_task(test_app):
    request_data = {
        "title": "New Task",
        "level": 1,
        "describe": "Do something"
    }
    response = test_app.post(f"{api_url}/create", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert 'id' in data


def test_update_task(test_app):
    # 先创建一个任务用于后续更新
    create_response = test_app.post(f"{api_url}/create", json={"title": "To be updated", "level": 1, "describe": "Initial"})
    task_id = create_response.json().get('id')

    update_data = {"title": "Updated Task", "level": 2, "describe": "Updated description"}
    response = test_app.post(f"{api_url}/update?task_id={task_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data['msg'] == '更新成功'


def test_delete_task(test_app):
    # 创建一个新任务以供删除测试
    create_response = test_app.post(f"{api_url}/create", json={"title": "Task to delete", "level": 1, "describe": "For deletion"})
    task_id = create_response.json().get('id')

    response = test_app.post(f"{api_url}/del?task_id={task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data['msg'] == '删除成功'


def test_get_task_info(test_app):
    # 创建一个新任务以供查询
    create_response = test_app.post(f"{api_url}/create", json={"title": "Task to query", "level": 1, "describe": "For querying"})
    task_id = create_response.json().get('id')

    response = test_app.get(f"{api_url}/info?task_id={task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == task_id


def test_list_tasks(test_app):
    response = test_app.get(f"{api_url}/list?page=1&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)