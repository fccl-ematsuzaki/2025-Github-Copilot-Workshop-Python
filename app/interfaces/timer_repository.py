from abc import ABC, abstractmethod
from typing import Optional
from ..models.timer import Timer


class TimerRepository(ABC):
    @abstractmethod
    def save(self, timer: Timer) -> None:
        """タイマーの状態を保存する"""
        pass
    
    @abstractmethod
    def get(self, timer_id: str) -> Optional[Timer]:
        """タイマーの状態を取得する"""
        pass
