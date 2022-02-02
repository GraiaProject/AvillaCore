from base64 import b64encode
from typing import TYPE_CHECKING, cast

from avilla.core.elements import Audio, Image, Notice, NoticeAll, Text, Video
from avilla.core.stream import Stream
from avilla.core.transformers import u8_string
from avilla.core.utilles import Registrar
from avilla.core.utilles.message import MessageSerializer
from avilla.onebot.elements import *

if TYPE_CHECKING:
    from .protocol import OnebotProtocol

registrar = Registrar()


@registrar.decorate("serializers")  # this allow you to register into other class
class OnebotMessageSerializer(MessageSerializer["OnebotProtocol"]):
    @staticmethod
    @registrar.register(Text)
    async def text(protocol: "OnebotProtocol", element: Text):
        return {
            "type": "text",
            "data": {
                "text": element.text,
            },
        }

    @staticmethod
    @registrar.register(Notice)
    async def notice(protocol: "OnebotProtocol", element: Notice):
        return {
            "type": "at",
            "data": {
                "qq": element.target.last()[1],
            },
        }

    @staticmethod
    @registrar.register(NoticeAll)
    async def notice_all(protocol: "OnebotProtocol", element: NoticeAll):
        return {"type": "at", "data": {"qq": "all"}}

    @staticmethod
    @registrar.register(Image)
    async def image(protocol: "OnebotProtocol", element: Image):
        avilla = protocol.avilla
        # 暂时还是 base64 吧。
        status, stream = await avilla.fetch_resource(element.source)
        if not status.available:
            raise RuntimeError(f"Image resource not available: {element.source} - {status.description}")
        stream = cast(Stream[bytes], stream)
        b64 = await stream.transform(b64encode).transform(u8_string).unwrap()
        return {
            "type": "image",
            "data": {
                "file": "base64://" + b64,
            },
        }

    @staticmethod
    @registrar.register(FlashImage)
    async def flash_image(protocol: "OnebotProtocol", element: FlashImage):
        avilla = protocol.avilla
        status, stream = await avilla.fetch_resource(element.source)
        if not status.available:
            raise RuntimeError(f"FlashImage resource not available: {element.source} - {status.description}")
        stream = cast(Stream[bytes], stream)
        b64 = await stream.transform(b64encode).transform(u8_string).unwrap()
        return {
            "type": "image",
            "data": {
                "file": "base64://" + b64,
                "type": "flash",
            },
        }

    @staticmethod
    @registrar.register(Audio)
    async def voice(protocol: "OnebotProtocol", element: Audio):
        avilla = protocol.avilla
        status, stream = await avilla.fetch_resource(element.source)
        if not status.available:
            raise RuntimeError(f"Image resource not available: {element.source} - {status.description}")
        stream = cast(Stream[bytes], stream)
        b64 = await stream.transform(b64encode).transform(u8_string).unwrap()
        return {
            "type": "record",
            "data": {
                "file": "base64://" + b64,
            },
        }

    @staticmethod
    @registrar.register(Video)
    async def video(protocol: "OnebotProtocol", element: Video):
        avilla = protocol.avilla
        status, stream = await avilla.fetch_resource(element.source)
        if not status.available:
            raise RuntimeError(f"Image resource not available: {element.source} - {status.description}")
        stream = cast(Stream[bytes], stream)
        b64 = await stream.transform(b64encode).transform(u8_string).unwrap()
        return {
            "type": "video",
            "data": {
                "file": "base64://" + b64,
            },
        }

    @staticmethod
    @registrar.register(Face)
    async def face(protocol: "OnebotProtocol", element: Face):
        return {
            "type": "face",
            "data": {
                "id": element.id,
            },
        }
