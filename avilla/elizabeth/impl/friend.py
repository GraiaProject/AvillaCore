from __future__ import annotations

from typing import TYPE_CHECKING

from avilla.core.message import Message, MessageTrait
from avilla.core.traitof.context import prefix, raise_for_no_namespace, scope
from avilla.core.traitof.recorder import default_target, impl, pull
from avilla.core.utilles.selector import Selector

if TYPE_CHECKING:
    from graia.amnesia.message import MessageChain

    from avilla.core.relationship import Relationship


raise_for_no_namespace()

with scope("friend"), prefix("friend"):

    @default_target(None, MessageTrait.send)
    @default_target(Message, MessageTrait.send)
    def send_friend_message_default_target(rs: Relationship):
        return rs.ctx

    @impl(None, MessageTrait.send)
    @impl(Message, MessageTrait.send)
    async def send_friend_message(
        rs: Relationship, target: Selector, message: MessageChain, *, reply: Selector | None = None
    ) -> Selector:
        serialized_msg = await rs.protocol.serialize_message(message)
        result = await rs.account.call(
            "sendFriendMessage",
            {
                "__method__": "post",
                "target": int(target.pattern["friend"]),
                "messageChain": serialized_msg,
                **({"quote": reply.pattern["message"]} if reply is not None else {}),
            },
        )
        return Selector().land(rs.land).group(target.pattern["friend"]).message(result["messageId"])

    @impl(None, MessageTrait.revoke)
    @impl(Message, MessageTrait.revoke)
    async def revoke_friend_message(rs: Relationship, message: Selector):
        await rs.account.call(
            "recall",
            {
                "__method__": "post",
                "messageId": int(message.pattern["message"]),
                "target": int(message.pattern["friend"]),
            },
        )
