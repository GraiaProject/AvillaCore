from __future__ import annotations

from graia.amnesia.message import Element, MessageChain
from telegram import Update

from avilla.core.event import AvillaEvent
from avilla.core.ryanvk.collector.application import ApplicationCollector
from avilla.standard.core.application.event import AvillaLifecycleEvent
from avilla.telegram.fragments import MessageFragment
from graia.ryanvk import Fn, PredicateOverload, SimpleOverload, TypeOverload


class TelegramCapability((m := ApplicationCollector())._):
    @Fn.complex({SimpleOverload(): ["event_type"]})
    async def event_callback(self, event_type: str, raw_event: Update) -> AvillaEvent | AvillaLifecycleEvent | None:
        ...

    @Fn.complex({PredicateOverload(lambda _, raw: raw["type"]): ["element"]})
    async def deserialize_element(self, element: MessageFragment) -> Element:  # type: ignore
        ...

    @Fn.complex({TypeOverload(): ["element"]})
    async def serialize_element(self, element: Any) -> MessageFragment:  # type: ignore
        ...

    async def deserialize(self, elements: list[MessageFragment]):
        _elements = []

        for raw_element in elements:
            _elements.append(await self.deserialize_element(raw_element))

        return MessageChain(_elements)

    async def serialize(self, message: MessageChain):
        chain = []

        for element in message:
            chain.append(await self.serialize_element(element))

        return chain

    async def handle_event(self, event_type: str, payload: Update):
        maybe_event = await self.event_callback(event_type, payload)

        if maybe_event is not None:
            self.avilla.event_record(maybe_event)
            self.avilla.broadcast.postEvent(maybe_event)
