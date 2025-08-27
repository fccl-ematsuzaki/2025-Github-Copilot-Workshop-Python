from typing import Dict, Optional
from ..interfaces.timer_repository import TimerRepository
from ..models.timer import Timer


class InMemoryTimerRepository(TimerRepository):
    def __init__(self):
        self._timers: Dict[str, Timer] = {}
    
    def save(self, timer_id: str, timer: Timer) -> None:
        """タイマーの状態をメモリに保存する"""
        self._timers[timer_id] = timer
    
    def get(self, timer_id: str) -> Optional[Timer]:
        """タイマーの状態をメモリから取得する"""
        return self._timers.get(timer_id)
