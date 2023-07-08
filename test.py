import asyncio
from inspect import cleandoc

from yarl import URL
from creart import create
#from graia.amnesia.builtins.aiohttp import AiohttpClientService
from graia.broadcast import Broadcast
from launart import Launart

from avilla.core import Avilla, Context, MessageReceived, Selector
from avilla.core.account import AccountInfo
from avilla.core.platform import Platform, Land, Abstract, Branch, Version
from avilla.core.elements import Picture, Notice
from avilla.core.resource import LocalFileResource
from avilla.onebot.protocol import OneBot11Protocol
from avilla.onebot.service import OneBot11Service
from avilla.onebot.account import OneBot11Account
from avilla.onebot.net.ws_client import OneBot11WsClientConfig, OneBot11WsClientNetworking

from test_env import A60_ENDPOINT, A60_SECRET

# import richuru
# richuru.install()

broadcast = create(Broadcast)
launart = Launart()
protocol = OneBot11Protocol()
service = protocol.service
conn = OneBot11WsClientNetworking()
config = OneBot11WsClientConfig(URL(A60_ENDPOINT), A60_SECRET)
conn.config = config
service.connections.append(conn)

platform = Platform(
    Land("qq"), Abstract("onebot/v11")
)

avilla = Avilla(
    broadcast, launart, [protocol], message_cache_size=0
)
protocol.avilla = avilla
account = OneBot11Account(Selector().land("qq").account("2885842008"), protocol)
conn.accounts[2885842008] = account
conn.protocol = protocol
account.websocket_client = conn
avilla.accounts[account.route] = AccountInfo(
    account.route, account, protocol, platform
)


from devtools import debug
debug(protocol.isolate.artifacts)
#exit()

# TODO(Networking): 自动注册 Account

@broadcast.receiver(MessageReceived)
async def on_message_received(cx: Context, event: MessageReceived):
    debug(cx.artifacts.maps)
    if cx.client.follows("::group.member(1846913566)"):
        await cx.scene.send_message(["Hello, Avilla!", Notice(cx.scene.member("1846913566"))])


async def log():
    while True:
        await asyncio.sleep(5)
        print("i'm alive!")
        #print(await avilla.get_account("208924405").call("groupList", {"__method__": "fetch"}))


#t = broadcast.loop.create_task(log())

avilla.launch_manager.launch_blocking(loop=broadcast.loop)
