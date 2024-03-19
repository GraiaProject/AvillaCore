from __future__ import annotations

from contextlib import nullcontext
from typing import TYPE_CHECKING, Any

from flywheel import CollectContext
from typing_extensions import Self

from avilla.core.event import AvillaEvent
from avilla.core.globals import AVILLA_CONTEXT_VAR, CONTEXT_CONTEXT_VAR, PROTOCOL_CONTEXT_VAR
from avilla.core.utilles import cachedstatic
from avilla.standard.core.application import AvillaLifecycleEvent

if TYPE_CHECKING:
    from avilla.core.application import Avilla
    from avilla.core.context import Context


class ProtocolConfig: ...


class BaseProtocol:
    avilla: Avilla

    @cachedstatic
    def artifacts():
        with CollectContext().collect_scope() as collect_context:
            ...

        return collect_context

    def ensure(self, avilla: Avilla) -> Any: ...

    def configure(self, config: ProtocolConfig) -> Self: ...

    def post_event(self, event: AvillaEvent | AvillaLifecycleEvent, context: Context | None = None):
        with (
            AVILLA_CONTEXT_VAR.use(self.avilla),
            PROTOCOL_CONTEXT_VAR.use(self),
            CONTEXT_CONTEXT_VAR.use(context) if context is not None else nullcontext(),
        ):
            self.avilla.event_record(event)
            return self.avilla.broadcast.postEvent(event)
