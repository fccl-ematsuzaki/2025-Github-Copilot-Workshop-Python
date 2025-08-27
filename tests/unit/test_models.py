import pytest
from datetime import timedelta
from app.models.timer import Timer, TimerState


@pytest.fixture
def timer():
    return Timer()


def test_timer_initialization(timer):
    assert timer.work_duration == 25
    assert timer.break_duration == 5
    assert timer.long_break_duration == 15
    assert timer.sessions_before_long_break == 4
    assert timer.state == TimerState.IDLE
    assert timer.current_session == 0
    assert timer.completed_sessions == 0
    assert timer.remaining_time == timedelta(minutes=25)
    assert timer.last_tick is None


def test_timer_start(timer):
    # 初期状態からの開始
    assert timer.start() == True
    assert timer.state == TimerState.WORKING
    assert timer.last_tick is not None

    # 一時停止からの開始
    timer.pause()
    assert timer.start() == True
    assert timer.state == TimerState.WORKING

    # すでに開始している状態での開始
    assert timer.start() == False


def test_timer_pause(timer):
    # 開始していない状態での一時停止
    assert timer.pause() == False
    assert timer.state == TimerState.IDLE

    # 作業中の一時停止
    timer.start()
    assert timer.pause() == True
    assert timer.state == TimerState.PAUSED
    assert timer.last_tick is None

    # すでに一時停止している状態での一時停止
    assert timer.pause() == False


def test_timer_reset(timer):
    # タイマー開始後のリセット
    timer.start()
    timer.remaining_time = timedelta(minutes=10)
    assert timer.reset() == True
    assert timer.state == TimerState.IDLE
    assert timer.remaining_time == timedelta(minutes=25)
    assert timer.last_tick is None

    # 初期状態でのリセット
    assert timer.reset() == True
    assert timer.state == TimerState.IDLE


def test_timer_session_completion(timer):
    # 作業セッションの完了
    timer.start()
    timer.remaining_time = timedelta(seconds=0)
    timer.tick()
    assert timer.state == TimerState.BREAK
    assert timer.completed_sessions == 1
    assert timer.remaining_time == timedelta(minutes=5)

    # 4セッション目の完了（長い休憩）
    timer.state = TimerState.WORKING
    timer.completed_sessions = 3  # 次のセッションが4セッション目
    timer.current_session = 3  # 現在のセッションも3に設定
    timer.remaining_time = timedelta(seconds=0)
    timer.tick()
    assert timer.state == TimerState.LONG_BREAK
    assert timer.completed_sessions == 4
    assert timer.remaining_time == timedelta(minutes=15)  # 休憩の完了
    timer.state = TimerState.BREAK
    timer.remaining_time = timedelta(seconds=0)
    timer.tick()
    assert timer.state == TimerState.WORKING
    assert timer.remaining_time == timedelta(minutes=25)
