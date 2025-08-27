import pytest
from app.repositories.timer_repository import InMemoryTimerRepository
from app.models.timer import Timer


@pytest.fixture
def repository():
    return InMemoryTimerRepository()


@pytest.fixture
def timer():
    return Timer()


def test_save_and_get_timer(repository, timer):
    # タイマーの保存
    repository.save("test", timer)
    
    # 保存したタイマーの取得
    saved_timer = repository.get("test")
    assert saved_timer is not None
    assert saved_timer.work_duration == timer.work_duration
    assert saved_timer.break_duration == timer.break_duration
    assert saved_timer.state == timer.state


def test_get_nonexistent_timer(repository):
    # 存在しないタイマーの取得
    timer = repository.get("nonexistent")
    assert timer is None


def test_update_timer(repository, timer):
    # タイマーの保存
    repository.save("test", timer)
    
    # タイマーの状態を変更
    timer.start()
    repository.save("test", timer)
    
    # 更新されたタイマーの取得
    updated_timer = repository.get("test")
    assert updated_timer is not None
    assert updated_timer.state == timer.state
