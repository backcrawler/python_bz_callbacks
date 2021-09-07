import threading
from typing import Callable, Any, List, Tuple

from .interface import ICallbacks


class SyncCallbacks(ICallbacks):
    """
    Synchronous callbacks
    """

    def __init__(self, once=False):
        self.lock = threading.Lock()
        self.callbacks = []
        self.fired = False
        self.once = once

    def add(self, callback: Callable[..., Any], order_importance_key: str = '') -> None:
        with self.lock:
            if not self.once or not self.fired:
                self.callbacks.append((order_importance_key, callback))
            else:
                self.__invoke_callback(callback)

    def is_empty(self) -> bool:
        return len(self.callbacks) == 0

    def _retrieve_tasks(self) -> List[Tuple[str, Callable]]:
        return sorted(self.callbacks)

    def fire(self) -> None:
        with self.lock:
            if self.once and self.fired:
                return
            self.fired = True
            if not self.is_empty():
                for key, cb in self._retrieve_tasks():
                    self.__invoke_callback(cb)
            if self.once:
                self.callbacks = []

    @staticmethod
    def __invoke_callback(callback: Callable[..., Any]) -> None:
        callback()
