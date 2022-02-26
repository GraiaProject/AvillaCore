import fnmatch
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Dict, Optional

from avilla.core.event import (
    MetadataChanged,
    RelationshipCreated,
    RelationshipDestroyed,
    ResourceAvailable,
)
from avilla.core.event.message import MessageReceived, MessageRevoked
from avilla.core.message import Message
from avilla.core.selectors import entity as entity_selector
from avilla.core.selectors import mainline as mainline_selector
from avilla.core.selectors import message as message_selector
from avilla.core.utilles import Registrar
from avilla.core.utilles.event import AbstractEventParser
from avilla.onebot.elements import Reply
from avilla.onebot.event_parse import OnebotEventTypeKey, OnebotEventParser

if TYPE_CHECKING:
    from avilla.miraigo.protocol import MiraigoProtocol


registrar = Registrar()


@registrar.decorate("parsers")
class MiraigoEventParser(OnebotEventParser):
    @staticmethod
    @registrar.register(OnebotEventTypeKey(post="notice", notice="group_recall"))
    async def group_recall(protocol: "MiraigoProtocol", data: Dict):
        # TODO: no self_id
        ...

    @staticmethod
    @registrar.register(OnebotEventTypeKey(post="notice", notice="friend_recall"))
    async def friend_recall(protocol: "MiraigoProtocol", data: Dict):
        # TODO: no self_id
        ...

    @staticmethod
    @registrar.register(OnebotEventTypeKey(post="notice", notice="notify", sub="poke"))
    async def notify_poke(protocol: "MiraigoProtocol", data: Dict):
        # TODO: 群内戳一戳 + 好友戳一戳. 等待Onebot实现.
        # TODO: 群内戳一戳 no self_id
        ...

    @staticmethod
    @registrar.register(OnebotEventTypeKey(post="notice", notice="notify", sub="lucky_king"))
    async def notify_lucky_king(protocol: "MiraigoProtocol", data: Dict):
        # TODO
        ...

    @staticmethod
    @registrar.register(OnebotEventTypeKey(post="notice", notice="notify", sub="honor"))
    async def notify_honor(protocol: "MiraigoProtocol", data: Dict):
        # TODO
        ...

    @staticmethod
    @registrar.register(OnebotEventTypeKey(post="notice", notice="group_card"))
    async def group_card(protocol: "MiraigoProtocol", data: Dict):
        # TODO
        ...

    @staticmethod
    @registrar.register(OnebotEventTypeKey(post="notice", notice="notify"))
    async def title_changed(protocol: "MiraigoProtocol", data: Dict):
        # TODO
        ...

    @staticmethod
    @registrar.register(OnebotEventTypeKey(post="notice", notice="offline_file"))
    async def offline_file(protocol: "MiraigoProtocol", data: Dict):
        # TODO
        ...

    @staticmethod
    @registrar.register(OnebotEventTypeKey(post="notice", notice="client_status"))
    async def client_status(protocol: "MiraigoProtocol", data: Dict):
        # TODO
        ...

    @staticmethod
    @registrar.register(OnebotEventTypeKey(post="notice", notice="essence"))
    async def essence(protocol: "MiraigoProtocol", data: Dict):
        # TODO
        ...
