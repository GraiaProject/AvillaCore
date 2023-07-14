from __future__ import annotations

from typing import TYPE_CHECKING

from avilla.standard.core.profile import Summary, Nick
from avilla.core.ryanvk.collector.account import AccountCollector
from avilla.core.selector import Selector

if TYPE_CHECKING:
    from ...account import ConsoleAccount  # noqa
    from ...protocol import ConsoleProtocol  # noqa


class ConsoleProfileActionPerform((m := AccountCollector["ConsoleProtocol", "ConsoleAccount"]())._):
    m.post_applying = True

    @m.pull("lang.console", Nick)
    async def get_console_nick(self, target: Selector) -> Nick:
        console = self.account.client.storage.current_user
        return Nick(console.nickname, console.nickname, "")

    @m.pull("lang.console", Summary)
    async def get_summary(self, target: Selector) -> Summary:
        console = self.account.client.storage.current_user
        return Summary(
            console.nickname, console.nickname
        )
