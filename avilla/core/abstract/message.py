from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

from graia.amnesia.message import MessageChain

from avilla.core.platform import Land
from avilla.core.utilles.selector import Selector

from ...spec.core.message.skeleton import MessageRevoke
from .metadata import Metadata

if TYPE_CHECKING:
    from datetime import datetime


@dataclass
class Message(Metadata):
    id: str
    scene: Selector
    time: datetime

    @property
    def land(self):
        return Land(cast(str, self.scene.pattern.get("land")))

    def to_selector(self) -> Selector:
        return self.scene.copy().message(self.id)

    def rev(self):
        return self.to_selector().rev()

    async def revoke(self):
        return await self.rev().wrap(MessageRevoke).revoke()


@dataclass
class ChatMessage(Message):
    sender: Selector
    content: MessageChain
    reply: Selector | None = None
