from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

from graia.amnesia.message import MessageChain

from avilla.core.metadata import Metadata
from avilla.core.platform import Land
from avilla.core.utilles.selector import Selector

if TYPE_CHECKING:
    from datetime import datetime


@dataclass
class Message(Metadata):
    id: str
    mainline: Selector
    sender: Selector
    content: MessageChain
    time: datetime
    reply: Selector | None = None

    @property
    def land(self):
        return Land(cast(str, self.mainline.pattern.get("land")))

    def to_selector(self) -> Selector:
        return self.mainline.copy().message(self.id)
