from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


class TimerState(Enum):
    IDLE = "idle"
    WORKING = "working"
    BREAK = "break"
    LONG_BREAK = "long_break"
    PAUSED = "paused"


@dataclass
class Timer:
    work_duration: int = 25  # minutes
    break_duration: int = 5  # minutes
    long_break_duration: int = 15  # minutes
    sessions_before_long_break: int = 4
    
    def __post_init__(self):
        self.state = TimerState.IDLE
        self.current_session = 0
        self.completed_sessions = 0
        self.remaining_time = timedelta(minutes=self.work_duration)
        self.last_tick = None
    
    def start(self) -> bool:
        """タイマーを開始する"""
        if self.state in [TimerState.IDLE, TimerState.PAUSED]:
            self.state = TimerState.WORKING
            self.last_tick = datetime.now()
            return True
        return False
    
    def pause(self) -> bool:
        """タイマーを一時停止する"""
        if self.state in [TimerState.WORKING, TimerState.BREAK, TimerState.LONG_BREAK]:
            self.state = TimerState.PAUSED
            self.last_tick = None
            return True
        return False
    
    def reset(self) -> bool:
        """タイマーをリセットする"""
        self.state = TimerState.IDLE
        self.remaining_time = timedelta(minutes=self.work_duration)
        self.last_tick = None
        return True
    
    def tick(self) -> bool:
        """タイマーを1秒進める (どんな状態でもremaining_timeが0以下なら必ず遷移)"""
        if self.state not in [TimerState.WORKING, TimerState.BREAK, TimerState.LONG_BREAK]:
            return False

        # どんな場合でもremaining_timeが0以下なら遷移
        if self.remaining_time.total_seconds() <= 0:
            self._handle_session_complete()
            return True

        current_time = datetime.now()
        if self.last_tick is None:
            self.last_tick = current_time
            return True

        elapsed = current_time - self.last_tick
        self.remaining_time -= elapsed
        self.last_tick = current_time

        if self.remaining_time.total_seconds() <= 0:
            self._handle_session_complete()

        return True
    
    def _handle_session_complete(self):
        """セッション完了時の処理 (状態が不整合でも正しく遷移するよう堅牢化)"""
        if self.state == TimerState.WORKING:
            # completed_sessions, current_sessionが手動で書き換えられても正しく遷移する
            next_completed = self.completed_sessions + 1
            if next_completed % self.sessions_before_long_break == 0:
                self.state = TimerState.LONG_BREAK
                self.remaining_time = timedelta(minutes=self.long_break_duration)
            else:
                self.state = TimerState.BREAK
                self.remaining_time = timedelta(minutes=self.break_duration)
            self.completed_sessions = next_completed
            self.current_session = next_completed
        elif self.state in [TimerState.BREAK, TimerState.LONG_BREAK]:
            self.state = TimerState.WORKING
            self.remaining_time = timedelta(minutes=self.work_duration)
        # どんな場合でもtick後はlast_tickをNoneに
        self.last_tick = None
