import typing
from contextvars import Token
from datetime import datetime
from types import TracebackType
from typing import Dict, Optional

from graia.broadcast.entities.dispatcher import BaseDispatcher
from graia.broadcast.entities.event import Dispatchable
from graia.broadcast.interfaces.dispatcher import DispatcherInterface

from avilla.core.relationship import Relationship
from avilla.core.selectors import entity as entity_selector

from ..context import ctx_protocol, ctx_relationship


class AvillaEvent(Dispatchable):
    ctx: entity_selector

    self: entity_selector
    time: datetime

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}: {' '.join([f'{k}={v.__repr__()}' for k, v in vars(self).items()])}>"
        )

    @classmethod
    def get_ability_id(cls) -> str:
        return f"event::{cls.__name__}"


_Dispatcher_Tokens: "Dict[int, Token[Relationship]]" = {}


class RelationshipDispatcher(BaseDispatcher):  # Avilla 将自动注入...哦, 看起来没这个必要.
    @staticmethod
    async def beforeExecution(interface: "DispatcherInterface[AvillaEvent]"):
        rs = await ctx_protocol.get().get_relationship(interface.event.ctx)
        token = ctx_relationship.set(rs)
        _Dispatcher_Tokens[id(interface.event)] = token

    @staticmethod
    async def afterExecution(
        interface: "DispatcherInterface",
        exception: Optional[Exception],
        tb: Optional[TracebackType],
    ):
        ctx_relationship.reset(_Dispatcher_Tokens[id(interface.event)])
        del _Dispatcher_Tokens[id(interface.event)]

    @staticmethod
    async def catch(interface: "DispatcherInterface"):
        if typing.get_origin(interface.annotation) is Relationship or interface.annotation is Relationship:
            return ctx_relationship.get()
