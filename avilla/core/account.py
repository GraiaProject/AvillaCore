from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from avilla.core.platform import Land
from avilla.core.utilles.selector import Selector

if TYPE_CHECKING:
    from avilla.core.protocol import BaseProtocol
    from avilla.core.relationship import Context


@dataclass
class AbstractAccount(ABC):
    id: str
    land: Land
    protocol: BaseProtocol

    def __init__(self, id: str, protocol: BaseProtocol, land: Land | None = None):
        self.id = id
        self.land = land or protocol.land
        self.protocol = protocol

    @abstractmethod
    async def get_relationship(self, target: Selector, *, via: Selector | None = None) -> Context:
        ...

    @abstractmethod
    async def call(self, endpoint: str, params: dict[str, Any] | None = None) -> Any:
        ...

    def get_self_relationship(self):
        from avilla.core.relationship import Context

        return Context(
            self.protocol,
            self,
            self.to_selector(),
            self.to_selector(),
            Selector().land(self.land.name),
            self.to_selector(),
        )

    @property
    def available(self) -> bool:
        return True

    def to_selector(self) -> Selector:
        return Selector().land(self.land.name).account(self.id)

    def is_anonymous(self) -> bool:
        return self.id == "anonymous"

    def __eq__(self, other: AbstractAccount):
        return (
            self.__class__ is other.__class__
            and self.id == other.id
            and self.land == other.land
            and self.protocol == other.protocol
        )
