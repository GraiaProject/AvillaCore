from __future__ import annotations

from typing import Any, Generic, TypeVar, overload
from typing_extensions import Self

from ..operators import instance_of

T = TypeVar("T")


class InstanceOf(Generic[T]):
    target: type[T]

    def __init__(self, target: type[T]) -> None:
        self.target = target

    @overload
    def __get__(self, instance: None, owner: type) -> Self:
        ...

    @overload
    def __get__(self, instance: Any, owner: type) -> T:
        ...

    def __get__(self, instance: Any, owner: type):
        if instance is None:
            return self

        return instance_of(self.target)
