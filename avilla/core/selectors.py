from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from avilla.core.platform import Base
from avilla.core.utilles.selector import DepthSelector, Selector, SelectorKey


class entity(Selector[Literal["entity"]]):
    scope = "entity"

    if TYPE_CHECKING:
        mainline: SelectorKey["entity", mainline]
        account: SelectorKey["entity", str]
        friend: SelectorKey["entity", str]
        member: SelectorKey["entity", str]
        channel: SelectorKey["entity", str]  # 可以发消息的 channel, 类似 tg.
        anonymous: SelectorKey["entity", str]  # 匿名用户

        group: SelectorKey["entity", Any]  # 于 mainline.group 不同，这里是拿来 “根据其他字段” 进行 multi config 的，因此这里可以随便填值。

    def get_mainline(self) -> mainline:
        if "account" in self.path:
            return mainline._["$avilla:account"]
        return self.path["mainline"]

    def get_entity_type(self) -> str:
        return list(self.without_group().path.keys())[-1]

    def get_entity_value(self) -> Any:
        return list(self.without_group().path.values())[-1]

    def without_group(self):
        return entity({k: v for k, v in self.path.items() if k != "group"})

    def __hash__(self) -> int:
        return hash(tuple(self.path.items()))

    @property
    def profile_name(self) -> str:
        return list(self.path.keys())[-1]


class mainline(DepthSelector[Literal["mainline"]]):
    _keypath_excludes = frozenset(["platform"])
    scope = "mainline"

    if TYPE_CHECKING:
        platform: SelectorKey["mainline", Base]
        group: SelectorKey["mainline", str]
        channel: SelectorKey["mainline", str]
        guild: SelectorKey["mainline", str]
        friend: SelectorKey["mainline", str]
        member: SelectorKey["mainline", str]

        _: SelectorKey["mainline", Any]


class message(Selector[Literal["message"]]):
    scope = "message"

    if TYPE_CHECKING:
        mainline: SelectorKey["message", mainline]
        _: SelectorKey["message", str]

    def get_mainline(self) -> mainline:
        return self.path["mainline"]


class request(Selector[Literal["request"]]):
    scope = "request"

    if TYPE_CHECKING:
        mainline: SelectorKey["request", mainline]
        via: SelectorKey["request", entity]
        _: SelectorKey["request", str]
        # 示例: request.mainline[mainline.group[123]]._[""]

    def get_mainline(self) -> "mainline":
        return self.path["mainline"]

    def get_via(self) -> entity | None:
        return self.path.get("via")
