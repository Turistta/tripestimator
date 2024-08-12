from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class BaseFetcher(ABC, Generic[T]):
    def __init__(self):
        self._source_url: str = ""

    @abstractmethod
    def fetch(self, *args: Any, **kwargs: Any) -> str:
        pass

    @property
    @abstractmethod
    def BASE_URL(self) -> str:
        raise NotImplementedError

    @property
    def source_url(self) -> str:
        return self._source_url

    @source_url.setter
    def source_url(self, value: str):
        self._source_url = value
