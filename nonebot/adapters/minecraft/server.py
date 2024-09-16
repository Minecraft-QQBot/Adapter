from typing import override

from nonebot import Bot as BaseBot
from nonebot.adapters import Adapter


class Server(BaseBot):
    @override
    def __init__(self, adapter: Adapter, name: str):
        BaseBot.__init__(self, adapter, name)

    @override
    async def handle_message(self, event: dict):
        pass
