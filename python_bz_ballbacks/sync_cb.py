import threading
from queue import PriorityQueue
from typing import Callable, Any

from .interface import ICallbacks


class SyncCallbacks(ICallbacks):
    """
    Synchronous callbacks
    """

    def __init__(self, once=False):
        self.lock = threading.Lock()
        self.callbacks = PriorityQueue()
        self.fired = False
        self.once = once

    def add(self, callback: Callable[..., Any], order_importance_key: str = '') -> None:
        with self.lock:
            if not self.once or not self.fired:
                self.callbacks.put((order_importance_key, callback))
            else:
                self.__invoke_callback(callback)

    def is_empty(self) -> bool:
        return self.callbacks.empty()

    def fire(self) -> None:
        with self.lock:
            if self.once and self.fired:
                return
            self.fired = True
            while not self.is_empty():
                key, cb = self.callbacks.get()
                self.__invoke_callback(cb)
            if self.once:
                self.callbacks = []

    @staticmethod
    def __invoke_callback(callback: Callable[..., Any]) -> None:
        callback()
