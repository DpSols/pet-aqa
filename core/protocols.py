from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class ConsumedMessage:
    topic: str
    partition: int
    offset: int
    key: bytes | None
    value: bytes


class MessageProducer(Protocol):
    def produce(
        self,
        topic: str,
        key: str | bytes,
        value: str | bytes | dict[str, Any],
    ) -> None:
        ...

    def flush(self, timeout: float = 10.0) -> None:
        ...


class MessageConsumer(Protocol):
    def subscribe(self, topics: list[str]) -> None:
        ...

    def consume(
        self,
        timeout: float = 1.0,
        max_records: int = 1,
    ) -> list[ConsumedMessage]:
        ...

    def close(self) -> None:
        ...


class StorageRepository(Protocol[T]):
    def save(self, entity: T) -> T:
        ...

    def find_by_id(self, id: str | int) -> T | None:
        ...

    def find_all(self, filters: dict[str, Any] | None = None) -> list[T]:
        ...

    def delete(self, id: str | int) -> bool:
        ...


