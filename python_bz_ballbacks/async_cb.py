import asyncio
from typing import Callable, Awaitable

from .interface import ICallbacks


class AsyncCallbacks(ICallbacks):
    """
    Asynchronous callbacks
    """

    def __init__(self, once=False, with_lock=False):
        self.lock = asyncio.Lock()
        self.callbacks = []
        self.fired = False
        self.once = once
        self.with_lock = with_lock

    async def add(self, callback: Callable[..., Awaitable]) -> None:
        async with self.lock:
            if not self.once or not self.fired:
                self.callbacks.append(callback)
            else:
                asyncio.create_task(callback())

    def is_empty(self) -> bool:
        return len(self.callbacks) == 0

    async def fire(self) -> None:
        if self.with_lock:
            async with self.lock:
                await self._fire()
        else:
            await self._fire()

    async def _fire(self) -> None:
        if self.once and self.fired:
            return

        self.fired = True
        if not self.is_empty():
            await asyncio.gather(*(callback() for callback in self.callbacks))

        if self.once:
            self.callbacks = []
