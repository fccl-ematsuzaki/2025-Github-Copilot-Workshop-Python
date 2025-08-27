import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_timer_lifecycle(client):
    # タイマーの初期状態を確認
    response = client.get("/api/timer/status")
    assert response.status_code == 200
    assert response.json["state"] == "idle"
    
    # タイマーを開始
    response = client.post("/api/timer/start")
    assert response.status_code == 200
    assert response.json["status"] == "started"
    
    # タイマーの状態を確認
    response = client.get("/api/timer/status")
    assert response.status_code == 200
    assert response.json["state"] == "working"
    
    # タイマーを一時停止
    response = client.post("/api/timer/pause")
    assert response.status_code == 200
    assert response.json["status"] == "paused"
    
    # タイマーの状態を確認
    response = client.get("/api/timer/status")
    assert response.status_code == 200
    assert response.json["state"] == "paused"
    
    # タイマーをリセット
    response = client.post("/api/timer/reset")
    assert response.status_code == 200
    assert response.json["status"] == "reset"
    
    # タイマーの状態を確認
    response = client.get("/api/timer/status")
    assert response.status_code == 200
    assert response.json["state"] == "idle"
