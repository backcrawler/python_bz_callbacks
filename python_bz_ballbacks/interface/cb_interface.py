from abc import ABC, abstractmethod

__all__ = ['ICallbacks']


class ICallbacks(ABC):

    @abstractmethod
    def add(self, callback) -> None:
        ...

    @abstractmethod
    def fire(self) -> None:
        ...

    @abstractmethod
    def is_empty(self) -> bool:
        ...
